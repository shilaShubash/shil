"""
OT Mentor AI - Streamlit Frontend

Main application interface for the OT Expert Mentor system.
"""

import streamlit as st
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.conversation_manager import ConversationManager
from backend.config import get_config


# Page configuration
st.set_page_config(
    page_title="OT Mentor AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "conversation_manager" not in st.session_state:
        st.session_state.conversation_manager = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "retrieved_scenarios" not in st.session_state:
        st.session_state.retrieved_scenarios = None


def render_sidebar():
    """Render the sidebar with session info and controls."""
    with st.sidebar:
        st.title("🧠 OT Mentor AI")
        st.markdown("---")

        # Model info (locked)
        config = get_config()
        st.markdown("### Model")
        st.info(f"**{config.model_config.ui_name}** (locked)")

        st.markdown("---")

        # Session info
        if st.session_state.conversation_manager:
            st.markdown("### Session Info")
            session_id = st.session_state.conversation_manager.get_session_id()
            st.code(session_id[:8], language=None)

            st.markdown("### Phase")
            phase = st.session_state.conversation_manager.phase
            if phase == "INTAKE":
                st.success("📝 Context Gathering")
            else:
                st.success("💬 Reflective Mentoring")

            # Template status
            from backend.tools import evaluate_context
            status = evaluate_context(st.session_state.conversation_manager.template)
            st.markdown("### Template Status")

            # Show transition readiness
            if status['phase'] == 'MENTORING':
                st.success("✅ Ready for transition")

            st.metric(
                "Fields Filled",
                f"{status['filled']}/{status['total']}"
            )
            st.metric(
                "Critical Fields",
                f"{status['filled_critical']}/{status['total_critical']}"
            )

            # Retrieved scenarios
            if st.session_state.retrieved_scenarios:
                st.markdown("### Retrieved Scenarios")
                for scenario in st.session_state.retrieved_scenarios:
                    st.markdown(f"**{scenario['id']}: {scenario['title']}**")
                    st.caption(f"Similarity: {scenario['similarity_score']:.2f}")

        st.markdown("---")

        # New session button
        if st.button("🔄 New Session", use_container_width=True):
            st.session_state.conversation_manager = None
            st.session_state.chat_history = []
            st.session_state.retrieved_scenarios = None
            st.rerun()


def render_chat_interface():
    """Render the main chat interface."""
    st.title("OT Expert Mentor")

    # Initialize conversation manager if needed
    if st.session_state.conversation_manager is None:
        with st.spinner("Initializing session..."):
            try:
                st.session_state.conversation_manager = ConversationManager()
                st.success("Session initialized! You can start the conversation.")
            except Exception as e:
                st.error(f"Failed to initialize: {str(e)}")
                st.stop()

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show scenario notification if present
            if "scenarios" in message and message["scenarios"]:
                with st.expander("📚 Retrieved Scenarios"):
                    for scenario in message["scenarios"]:
                        st.markdown(f"**{scenario['title']}**")
                        st.caption(f"Similarity Score: {scenario['similarity_score']:.2f}")

    # Chat input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Add to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.conversation_manager.send_message(user_input)

                    # Display response
                    st.markdown(result["response"])

                    # Add to history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": result["response"]
                    })

                    # Handle phase transition (scenarios only exist after transitioning to MENTORING)
                    if result["phase"] == "MENTORING" and result["scenarios"]:
                        st.session_state.retrieved_scenarios = result["scenarios"]
                        st.success("✨ Context gathering complete! Transitioning to mentoring phase...")
                        st.rerun()

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.exception(e)


def render_welcome_screen():
    """Render welcome screen if no conversation started."""
    if not st.session_state.chat_history:
        st.markdown("""
        ## Welcome to the OT Expert Mentor System

        This AI mentor will guide you through professional reasoning in occupational therapy practice.

        ### How it works:

        1. **Context Gathering**: I'll ask questions to understand your case (patient, setting, difficulty)
        2. **Scenario Matching**: The system will find similar cases to reference
        3. **Reflective Mentoring**: I'll guide you through professional reasoning using the Socratic method

        ### Remember:

        - I ask **one question at a time** to give you space to think
        - I **don't provide direct solutions** - instead, I guide you to reason through the case
        - I work across **five types of professional reasoning**: Scientific, Narrative, Pragmatic, Ethical, Interactive

        **Ready to begin? Type your first message below!**
        """)


def main():
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()

    # Render sidebar
    render_sidebar()

    # Render main interface
    render_welcome_screen()
    render_chat_interface()


if __name__ == "__main__":
    main()
