"""
Conversation Manager - orchestrates the OT Mentor conversation flow.

Manages phase transitions, LLM interactions, RAG retrieval, and session persistence.
"""

from typing import List, Dict, Any, Literal, Optional
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from backend.config import get_config
from backend.prompts import (
    BASE_SYSTEM_PROMPT,
    PHASE_1_INSTRUCTIONS,
    PHASE_2_INSTRUCTIONS,
    SCENARIO_USAGE_INSTRUCTIONS,
    create_scenario_context_message
)
from backend.tools import (
    Template,
    evaluate_context,
    generate_conversation_summary
)
from backend.rag_retriever import ScenarioRetriever
from backend.session_manager import SessionManager


Phase = Literal["INTAKE", "MENTORING"]


class ConversationManager:
    """
    Orchestrates the OT Mentor conversation across phases.
    """

    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize conversation manager.

        Args:
            session_id: Optional existing session ID for resuming
        """
        config = get_config()

        # Initialize components
        self.session_manager = SessionManager(session_id)
        self.retriever = ScenarioRetriever()

        # Initialize LLM
        self.model = ChatGoogleGenerativeAI(
            model=config.model_config.technical_name,
            google_api_key=config.google_api_key,
            temperature=0.7
        )

        # Load or initialize state
        self.template = self.session_manager.load_template()
        self.phase: Phase = "INTAKE"  # Always start in INTAKE
        self.messages: List[Any] = []  # LangChain message objects
        self.retrieved_scenarios: Optional[List[Dict[str, Any]]] = None

        # Check if this is a resumed session
        conv_data = self.session_manager.load_conversation()
        if conv_data["messages"]:
            self._restore_from_conversation(conv_data)
        else:
            self._initialize_new_conversation()

    def _initialize_new_conversation(self) -> None:
        """Initialize a new conversation with base prompts."""
        self.messages = [
            SystemMessage(content=BASE_SYSTEM_PROMPT),
            SystemMessage(content=PHASE_1_INSTRUCTIONS)
        ]

    def _restore_from_conversation(self, conv_data: Dict[str, Any]) -> None:
        """
        Restore conversation state from saved data.

        Args:
            conv_data: Loaded conversation data
        """
        # Reconstruct messages
        for msg_dict in conv_data["messages"]:
            role = msg_dict["role"]
            content = msg_dict["content"]

            if role == "system":
                self.messages.append(SystemMessage(content=content))
            elif role == "user":
                self.messages.append(HumanMessage(content=content))
            elif role == "assistant":
                self.messages.append(AIMessage(content=content))

        # Determine phase
        if conv_data.get("phase_transition_at"):
            self.phase = "MENTORING"
            self.retrieved_scenarios = self.session_manager.load_retrieved_scenarios()

    def send_message(self, user_message: str) -> Dict[str, Any]:
        """
        Process user message and generate response.

        Args:
            user_message: User's input message

        Returns:
            Dictionary with:
                - response: AI response text
                - phase: Current phase
                - phase_changed: Whether phase transitioned
                - scenarios: Retrieved scenarios if phase just transitioned
                - template_status: Template completion status
        """
        # Add user message
        self.messages.append(HumanMessage(content=user_message))

        # Get AI response
        ai_response = self.model.invoke(self.messages)
        self.messages.append(AIMessage(content=ai_response.content))

        # Check for phase transition (only in INTAKE phase)
        phase_changed = False
        scenarios = None

        if self.phase == "INTAKE":
            # Update template (simple extraction from conversation)
            # Note: In a more sophisticated implementation, we might use an LLM
            # or structured output to extract template fields. For now, we rely
            # on the conversation manager to track when enough context is gathered.

            # Check if context is sufficient
            should_transition, status_msg = evaluate_context(self.template)

            if should_transition:
                # Perform phase transition
                phase_changed = True
                scenarios = self._execute_phase_transition()

        # Save conversation
        self._save_state()

        return {
            "response": ai_response.content,
            "phase": self.phase,
            "phase_changed": phase_changed,
            "scenarios": scenarios,
            "template_status": self._get_template_status()
        }

    def _execute_phase_transition(self) -> List[Dict[str, Any]]:
        """
        Execute transition from INTAKE to MENTORING phase.

        Returns:
            List of retrieved scenarios
        """
        # Generate conversation summary from template
        summary = generate_conversation_summary(self.template)

        # Retrieve scenarios
        scenarios = self.retriever.retrieve_scenarios(summary)
        self.retrieved_scenarios = scenarios

        # Add Phase 2 instructions and scenarios to messages
        self.messages.append(SystemMessage(content=PHASE_2_INSTRUCTIONS))
        self.messages.append(
            SystemMessage(content=create_scenario_context_message(scenarios))
        )
        self.messages.append(SystemMessage(content=SCENARIO_USAGE_INSTRUCTIONS))

        # Update phase
        self.phase = "MENTORING"

        # Save scenario metadata
        self.session_manager.save_retrieved_scenarios(scenarios)
        self.session_manager.mark_phase_transition()

        return scenarios

    def update_template_field(self, field: str, value: str) -> Dict[str, Any]:
        """
        Manually update a template field.

        Args:
            field: Template field name
            value: Field value

        Returns:
            Dictionary with evaluation results
        """
        if hasattr(self.template, field):
            setattr(self.template, field, value)
            self.session_manager.save_template(self.template)

            should_transition, status_msg = evaluate_context(self.template)

            return {
                "success": True,
                "should_transition": should_transition,
                "status_message": status_msg
            }

        return {
            "success": False,
            "error": f"Unknown field: {field}"
        }

    def _save_state(self) -> None:
        """Save current conversation state to disk."""
        # Convert messages to serializable format
        msg_dicts = []
        for msg in self.messages:
            if isinstance(msg, SystemMessage):
                msg_dicts.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                msg_dicts.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                msg_dicts.append({"role": "assistant", "content": msg.content})

        # Save conversation
        config = get_config()
        phase_transition_at = (
            self.session_manager.get_phase_transition_timestamp()
            if self.phase == "MENTORING"
            else None
        )

        self.session_manager.save_conversation(
            messages=msg_dicts,
            model=config.model_config.technical_name,
            phase_transition_at=phase_transition_at
        )

        # Save template
        self.session_manager.save_template(self.template)

    def _get_template_status(self) -> Dict[str, Any]:
        """
        Get current template completion status.

        Returns:
            Dictionary with template statistics
        """
        should_transition, status_msg = evaluate_context(self.template)

        return {
            "filled_count": self.template.get_filled_count(),
            "critical_filled": self.template.get_critical_filled_count(),
            "additional_filled": self.template.get_additional_filled_count(),
            "should_transition": should_transition,
            "status_message": status_msg
        }

    def get_session_id(self) -> str:
        """Get the current session ID."""
        return self.session_manager.session_id
