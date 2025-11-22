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