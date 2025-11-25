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
- ingest_scenarios.py - One-time scenario ingestion into ChromaDB

**app/** - Current implementation (Streamlit + LangChain)
- app.py - Streamlit frontend
- backend/ - Core logic (conversation_manager, prompts, tools, rag_retriever, session_manager, config)
- data/chroma_db/ - ChromaDB vector store (created after ingestion)
- sessions/ - Runtime session files (template.json, conversation.json, retrieved_scenarios.json)
- README.md - Setup and usage instructions

**Root files:**
- CLAUDE.md - This file (context and tasks)
- PROJECT-DESIGN.md - Academic documentation and design decisions
- TECHNICAL-DESIGN.md - System architecture and technical specifications
- system-prompt-analysis.md - System prompt comparison and final prompt

## Current Status

**Phase 2 In Progress:** System implementation complete with core functionality working

**Recent Refactoring (2025-11-25):**
- Fixed phase transition timing and logic
- Removed redundant code and temporary message patterns
- Cleaned up evaluate_context return structure
- Added LLM thinking process filtering
- Updated prompts to rely on permanent message history

## Known Issues

**Issue 1: Double message rendering**
- Messages appear twice (grayed out) before disappearing in UI
- Cause: Messages displayed immediately with st.markdown() AND added to history, then st.rerun() causes duplicate
- Impact: Visual glitch during message display
- Status: Pending fix