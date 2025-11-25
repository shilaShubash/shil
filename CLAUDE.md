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

**Phase 2 In Progress:** System implementation underway, initial deployment with issues

## Current Issues

**Issue 1: Retrieved scenarios missing scenario numbers**
- When scenarios are retrieved and displayed, they show titles but not scenario numbers
- Expected: "Scenario 03: Dependency & Decision Making"
- Actual: "Dependency & Decision Making"
- Location: RAG retrieval system and/or scenario metadata

**Issue 2: LLM stops responding after phase transition**
- After transitioning from INTAKE to MENTORING phase, LLM provides one response then stops
- Example: User answered "כדורגל" (football) and received no follow-up questionyou
- Expected: LLM should continue with mentoring questions using Professional Reasoning Framework
- Suspected: Phase 2 system messages may not be correctly added to conversation flow

**Issue 3: Phase transition UI elements not displaying**
- The transition success message and retrieved scenarios expander are not showing in the UI
- The following code block in app.py (lines 145-156) is not executing/rendering:
  ```python
  if result["phase_changed"]:
      st.success("✨ Context gathering complete! Transitioning to mentoring phase...")
      # ... scenario display code
  ```
- Suspected: Either `phase_changed` is not being set correctly or Streamlit rerun is clearing the UI before it displays