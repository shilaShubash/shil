# Project Context

MSc thesis project building and evaluating an AI expert mentor system for occupational therapy trainees using LLMs.

## File Organization

**old-resources/** - Baseline materials from previous attempts
- **prompts/** - System prompt iterations (original → enhanced → enhanced_2) + Hebrew requirement docs
- **theory/** - 4 theory papers (PDFs + extracted MD files + extraction-methodology.md)
- **scenarios/** - 18 scenario documents (docx + pdf)
- **app/** - Previous Python implementation (reference only, not actively used)

**scenarios/** - Working scenario files (18 scenarios, numbered 1-4, 5-18)

**scripts/** - Utility scripts
- calculate-pdf-tokens.py - PDF token estimation utility
- calculate-scenario-tokens.py - Scenario markdown token estimation utility

**Root files:**
- CLAUDE.md - This file (context and tasks)
- PROJECT-DESIGN.md - Academic documentation and design decisions
- TECHNICAL-DESIGN.md - System architecture and technical specifications
- system-prompt-analysis.md - System prompt comparison and final prompt

## Current Status

**Phase 1 Complete:** Foundation building, system prompt development, technical design finalized

**Current Tasks:**
- [ ] Begin Phase 2 implementation
- [ ] Scenario ingestion script
- [ ] Conversation manager implementation

## notes

- the retrieved scenarios are lacking the scenario number
- when we transition into phase 2, the llm stopped responding. meaning, we answered כדורגל and it didnt continue
- all of these dont even show:
  - with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.conversation_manager.send_message(user_input)

                    # Display response
                    st.markdown(result["response"])

                    # Handle phase transition
                    if result["phase_changed"]:
                        st.success("✨ Context gathering complete! Transitioning to mentoring phase...")
                        st.session_state.current_phase = result["phase"]
                        st.session_state.retrieved_scenarios = result["scenarios"]

                        # Show retrieved scenarios
                        if result["scenarios"]:
                            with st.expander("📚 Retrieved Scenarios", expanded=True):
                                st.markdown("I've found similar cases to reference:")
                                for scenario in result["scenarios"]:
                                    st.markdown(f"- **{scenario['title']}**")