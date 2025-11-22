"""
Session Manager for file-based persistence.

Handles saving and loading session artifacts:
- template.json: The 18-field template
- retrieved_scenarios.json: Retrieved scenarios metadata
- conversation.json: Full conversation history
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from uuid import uuid4

from backend.config import get_config
from backend.tools import Template


class SessionManager:
    """Manages session persistence to filesystem."""

    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize session manager.

        Args:
            session_id: Optional existing session ID, or creates new one
        """
        self.session_id = session_id or str(uuid4())
        config = get_config()

        # Create session directory
        self.session_dir = Path(config.sessions_dir) / self.session_id
        self.session_dir.mkdir(parents=True, exist_ok=True)

        # File paths
        self.template_path = self.session_dir / "template.json"
        self.scenarios_path = self.session_dir / "retrieved_scenarios.json"
        self.conversation_path = self.session_dir / "conversation.json"

        # Initialize empty files if new session
        if not self.template_path.exists():
            self._init_empty_template()

        if not self.conversation_path.exists():
            self._init_empty_conversation()

    def _init_empty_template(self) -> None:
        """Create empty template file."""
        empty_template = Template().to_dict()
        with open(self.template_path, 'w', encoding='utf-8') as f:
            json.dump(empty_template, f, indent=2, ensure_ascii=False)

    def _init_empty_conversation(self) -> None:
        """Create empty conversation file."""
        conversation_data = {
            "session_id": self.session_id,
            "created_at": datetime.now().isoformat(),
            "phase_transition_at": None,
            "model": None,
            "messages": []
        }
        with open(self.conversation_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)

    def save_template(self, template: Template) -> None:
        """
        Save template to file.

        Args:
            template: Template object to save
        """
        with open(self.template_path, 'w', encoding='utf-8') as f:
            json.dump(template.to_dict(), f, indent=2, ensure_ascii=False)

    def load_template(self) -> Template:
        """
        Load template from file.

        Returns:
            Template object
        """
        template = Template()
        if self.template_path.exists():
            with open(self.template_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                template.update_from_dict(data)
        return template

    def save_retrieved_scenarios(self, scenarios: List[Dict[str, Any]]) -> None:
        """
        Save retrieved scenarios metadata to file.

        Args:
            scenarios: List of scenario dictionaries
        """
        # Save only metadata (id, title, score) - not full content
        metadata = [
            {
                "id": s["id"],
                "title": s["title"],
                "similarity_score": s["similarity_score"]
            }
            for s in scenarios
        ]

        with open(self.scenarios_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def load_retrieved_scenarios(self) -> Optional[List[Dict[str, Any]]]:
        """
        Load retrieved scenarios metadata from file.

        Returns:
            List of scenario metadata dictionaries, or None if not yet retrieved
        """
        if not self.scenarios_path.exists():
            return None

        with open(self.scenarios_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_conversation(
        self,
        messages: List[Dict[str, str]],
        model: str,
        phase_transition_at: Optional[str] = None
    ) -> None:
        """
        Save conversation history to file.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model name being used
            phase_transition_at: ISO timestamp of phase transition, if occurred
        """
        conversation_data = {
            "session_id": self.session_id,
            "created_at": self._get_created_at(),
            "phase_transition_at": phase_transition_at,
            "model": model,
            "messages": messages
        }

        with open(self.conversation_path, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)

    def load_conversation(self) -> Dict[str, Any]:
        """
        Load conversation history from file.

        Returns:
            Conversation data dictionary
        """
        if not self.conversation_path.exists():
            return {
                "session_id": self.session_id,
                "created_at": datetime.now().isoformat(),
                "phase_transition_at": None,
                "model": None,
                "messages": []
            }

        with open(self.conversation_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_created_at(self) -> str:
        """Get creation timestamp from existing conversation file."""
        if self.conversation_path.exists():
            with open(self.conversation_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("created_at", datetime.now().isoformat())
        return datetime.now().isoformat()

    def get_phase_transition_timestamp(self) -> Optional[str]:
        """
        Get the timestamp when phase transition occurred.

        Returns:
            ISO format timestamp string, or None if not yet transitioned
        """
        conv_data = self.load_conversation()
        return conv_data.get("phase_transition_at")

    def mark_phase_transition(self) -> None:
        """Mark the current time as phase transition timestamp."""
        conv_data = self.load_conversation()
        conv_data["phase_transition_at"] = datetime.now().isoformat()

        with open(self.conversation_path, 'w', encoding='utf-8') as f:
            json.dump(conv_data, f, indent=2, ensure_ascii=False)
