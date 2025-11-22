# AI Expert Mentor System for Occupational Therapy Trainees

## Project Overview

### Research Context

This MSc thesis project addresses a critical gap in occupational therapy (OT) education: the scarcity of expert mentors for trainees. The project combines applied system development with empirical evaluation.

**Research Question:** Can Large Language Models effectively serve as virtual expert mentors for OT students and trainees?

**Approach:**
1. Develop conversational AI mentoring system grounded in OT professional standards
2. Deploy with real OT trainees in practical training scenarios
3. Evaluate effectiveness through structured user assessment

### Stakeholders

- **Researcher/Developer:** Shila (MSc candidate)
- **Domain Experts:** Practicing occupational therapists (requirements providers, validators)
- **End Users:** OT students and trainees (system users, evaluation participants)
- **Academic Advisors:** [TBD]

### Project Phases

**Phase 1: Foundation Building** (Current)
- Collection of baseline materials
- Theory extraction and documentation
- System prompt development

**Phase 2: System Implementation** (Planned)
- RAG system design
- Integration of scenarios and theory
- Technical deployment

**Phase 3: Evaluation** (Planned)
- User testing protocol
- Data collection
- Analysis and thesis writing

---

## Initial Materials Received

### Hebrew Requirements Document

**Source:** OT practitioners (non-technical domain experts)
**Format:** Word documents (prompt-1.docx, prompt-2-with-notes.docx, prompt-3-simple.docx)
**Nature:** Requirements and expectations written by practitioners, not technical specifications

**Key Characteristics:**
- Written in Hebrew
- Descriptive rather than prescriptive
- Expressed what they wanted the AI to do, not how to build it
- Mix of functional requirements and behavioral expectations

**Status:** Treated as "customer requirements" - necessary input but requiring professional translation into technical system design

### Theory Papers

Four academic/professional papers establishing OT knowledge standards:

**Paper 1: Cognitive Strategies** (12 pages, `/old-resources/theory/theory-1.pdf`)
- Core definitions and taxonomy of cognitive strategies
- Strategy attributes framework (Visibility, Permanence, Target)
- Clinical application examples and reasoning tool
- Purpose matrix (Learning vs Performance contexts)

**Paper 2: OT Supervision Guidelines** (6 pages, `/old-resources/theory/theory-2.pdf`)
- Definition of supervision as cooperative process
- Scope of practice distinctions (OT vs OTA vs Aide)
- General principles for collaborative plans
- Rules for proper professional behavior

**Paper 3: Professional Standards** (7 pages, `/old-resources/theory/theory-3.pdf`)
- OT practice and professional standards definitions
- Accurate clinical terminology requirements
- Five professional standards:
  - Standard I: Professional Standing and Responsibility
  - Standard II: Service Delivery
  - Standard III: Screening, Evaluation, and Reevaluation
  - Standard IV: Intervention Process
  - Standard V: Outcomes, Transition, and Discontinuation

**Paper 4: Professional Reasoning** (7 pages, `/old-resources/theory/theory-4.pdf`)
- Professional reasoning types framework:
  - Scientific Reasoning (evidence-based)
  - Narrative Reasoning (patient's story)
  - Pragmatic Reasoning (resources/constraints)
  - Ethical Reasoning (values/rights)
  - Interactive Reasoning (communication)
  - Conditional Reasoning (holistic integration)
- Reasoning-to-action mapping across intervention stages
- Explicit clinical reasoning questions
- Intervention approaches taxonomy (OTPF framework)

### Scenario Collection

**Source:** Previous project attempts
**Quantity:** 18 scenarios (scenario-01 through scenario-19, missing scenario-05)
**Formats:** Word documents (docx) and PDF exports
**Location:** `/old-resources/scenarios/`

**Purpose:** Training examples and reference cases for context-specific guidance through RAG retrieval

---

## Methodology

### Theory Paper Extraction Process

**Objective:** Extract relevant professional knowledge while maintaining academic integrity

**Principles:**
1. **Verbatim extraction** - Selected sections extracted in full (no summarization)
2. **Relevance filtering** - Content evaluated for operational utility to AI mentor
3. **Academic integrity** - Complete sections preserved for auditing and reference
4. **Exclusion criteria** - Remove references, author bios, boilerplate, non-operational content

**Evaluation Criteria:**
- Does this help the mentor guide trainees effectively?
- Can the mentor use this to ask better questions or provide better feedback?
- Does this establish necessary terminology or mental models?

**Documentation:** Full extraction decisions documented in `/old-resources/theory/extraction-methodology.md`

**Extraction Rates:**
- Theory 1: ~80% (9.6 of 12 pages)
- Theory 2: ~90% (5.4 of 6 pages)
- Theory 3: ~85% (6 of 7 pages)
- Theory 4: ~70% (5 of 7 pages)

### System Prompt Development Strategy

**Architectural Principle:** Treat Hebrew requirements as "customer specifications" requiring professional architectural translation

**Analogy:** Like an architect receiving a design document from a lay-person client:
- Cannot ignore the document (contains real requirements)
- Cannot use it as-is (lacks technical rigor)
- Must extract intent and rebuild professionally

**Iterative Refinement Approach:** Three versions, each building on previous

---

## Work Completed - Phase 1

### Collection and Organization (2025-11-21)

**Actions:**
- Collected all materials from Google Drive
- Organized into `old-resources/` structure
- Renamed files to consistent kebab-case format
- Separated by type: prompts, theory, scenarios, app

**Results:**
- Clean baseline established
- All source materials preserved
- Ready for extraction and development

### Theory Extraction (2025-11-22)

**Actions:**
- Read all four theory papers
- Identified relevant sections per extraction principles
- Documented extraction decisions in methodology document
- Created extracted markdown files for each paper

**Results:**
- `/old-resources/theory/theory_[1-4]_extracted.md` - Verbatim extracted content
- `/old-resources/theory/extraction-methodology.md` - Extraction rationale and decisions

### System Prompt Development

#### Version 1: Original (`system_prompt_original.md`)

**Goal:** Transform Hebrew requirements into professional system prompt structure

**Key Changes:**
- Translated Hebrew requirements to English
- Established clear persona: "Mentor for Occupational Therapists"
- Defined interaction constraints:
  - One Question Rule (no overwhelming)
  - Reflective Guidance (no direct solutions)
  - Empowerment focus
- Created 3-phase workflow:
  - Phase 1: Context Gathering (Template)
  - Phase 2: Scenario Retrieval (Transition)
  - Phase 3: Reflective Mentoring
- Defined tone: calm, empathetic, with corrective capability

**Source:** Hebrew requirements documents

**Rationale:** Needed to establish professional structure while preserving client requirements

#### Version 2: Enhanced (`system_prompt_enhanced.md`)

**Goal:** Integrate professional knowledge from theory papers

**Key Additions:**
- Clinical Reasoning Framework (5 types from theory papers):
  - Scientific Reasoning (evidence & pathology)
  - Narrative Reasoning (patient's story)
  - Pragmatic Reasoning (resources & constraints)
  - Ethical Reasoning (values & rights)
  - Interactive Reasoning (communication)
- Professional Knowledge Base section:
  - Scope of Practice rules (OT vs OTA vs Aide)
  - Cognitive Strategy Attributes
  - Intervention Approaches (OTPF)
- Safety & Ethics guardrails
- More structured context template with critical fields marked

**Source:** Extraction from theory papers 1-4

**Rationale:** System needed grounding in professional standards to function as credible mentor

#### Version 3: Enhanced 2 (`system_prompt_enhanced_2.md`) - Current

**Goal:** Refine to Professional Reasoning Framework with explicit implementation guidance

**Key Changes:**
- Renamed to "Professional Reasoning" (vs "Clinical Reasoning")
  - Rationale: Better aligns with educational/reflective model rather than medical model
- Added explicit guiding questions for each reasoning type
  - Example: Scientific - "What is known about the diagnosis in the literature?"
  - Example: Narrative - "How is the difficulty perceived by the student and family?"
- Simplified structure:
  - Removed some technical enforcement
  - More focused on trainee empowerment
  - Cleaner workflow description
- Emphasized that questions come from framework, not ad-hoc

**Source:** Refinement based on theory paper 4 emphasis on Professional Reasoning

**Rationale:** Mentor needs explicit questions to ask, not just reasoning categories to think about

#### Final System Prompt & Technical Design (2025-11-22)

**Completed:** System prompt synthesis and technical architecture finalized

**Deliverables:**
- Final system prompt (documented in `system-prompt-analysis.md`)
- Complete technical specification (documented in `TECHNICAL-DESIGN.md`)

**Process:** Analyzed all three prompt versions, consulted Anthropic documentation, designed RAG approach, finalized conversation flow and persistence strategy.

---

## Key Design Decisions

### Why Three System Prompt Iterations?

**Progressive refinement approach:**

1. **V1:** Structure - Establish professional format and workflow
2. **V2:** Content - Integrate professional knowledge and frameworks
3. **V3:** Implementation - Provide explicit operational guidance

Each iteration validated previous work while adding new layer.

### Why Professional Reasoning Framework?

**Evolution:** Clinical Reasoning → Professional Reasoning

**Rationale:**
- "Clinical" implies medical diagnostic model
- "Professional" better captures educational/reflective mentoring role
- Aligns with OT literature emphasis on reflective practice
- Less prescriptive, more developmental

### Why One-Question Constraint?

**Rationale:**
- Prevents overwhelming trainees with multiple complex questions
- Forces AI to prioritize and focus
- Mirrors real mentor behavior (space for thinking)
- Creates natural conversational flow
- Allows time for reflection before next question

### Why No Direct Solutions?

**Pedagogical Foundation:**
- Socratic method: learning through guided questioning
- Empowerment: trainees develop own reasoning capability
- Sustainability: trainees can't become dependent on AI giving answers
- Professional development: OT requires autonomous clinical reasoning

**Implementation:** Explicit prohibition in system prompt with example rephrasing

### What Content to Extract vs Exclude from Papers?

**Included:**
- Definitions and terminology
- Frameworks and taxonomies
- Tables and structured content
- Examples and scenarios
- Professional standards and rules
- Question templates

**Excluded:**
- Academic references
- Author biographies
- Detailed U.S.-specific regulatory information
- General discussion sections
- Copyright boilerplate

**Rationale:** Maximize operational utility while maintaining academic integrity for auditing

### Why Verbatim Extraction?

**Decision:** Extract complete sections, not summarized

**Rationale:**
- Academic integrity - allows auditing of source material
- Prevents interpretation errors
- Maintains context and nuance
- Supports future thesis writing with proper citations

---

## Artifacts Produced

### Documentation

- `/old-resources/theory/extraction-methodology.md` - Complete extraction decisions and rationale
- `/CLAUDE.md` - Minimal context and task management
- `/PROJECT-DESIGN.md` - This document (academic project documentation)
- `/TECHNICAL-DESIGN.md` - System architecture and technical specifications
- `/system-prompt-analysis.md` - System prompt comparison, analysis, and final prompt

### System Prompts

- `/old-resources/prompts/system_prompt_original.md` - v1 (Hebrew requirements translated)
- `/old-resources/prompts/system_prompt_enhanced.md` - v2 (theory integration)
- `/old-resources/prompts/system_prompt_enhanced_2.md` - v3 (refined questions)
- **Final prompt:** See system-prompt-analysis.md (synthesizes all versions with improvements)

### Theory Extractions

- `/old-resources/theory/theory_1_extracted.md` - Cognitive Strategies
- `/old-resources/theory/theory_2_extracted.md` - Supervision Guidelines
- `/old-resources/theory/theory_3_extracted.md` - Professional Standards
- `/old-resources/theory/theory_4_extracted.md` - Professional Reasoning

### Scenario Files

- `/scenarios/scenario-{1-4,5-18}.md` - 18 working scenario files (converted from PDFs)

### Utilities

- `/calculate-pdf-tokens.py` - Token estimation tool for PDF content

---

## Technical Context

### Token Analysis

Total estimated tokens across all PDFs: **~45,500 tokens**

**Breakdown:**
- Theory papers: ~23,368 tokens (32 pages)
  - Theory 1: ~13,040 tokens (12 pages)
  - Theory 2: ~3,580 tokens (6 pages)
  - Theory 3: ~4,150 tokens (7 pages)
  - Theory 4: ~2,598 tokens (7 pages)
- Scenarios: ~21,174 tokens (58 pages across 18 scenarios)

**Implications:**
- Fits within context windows of modern LLMs
- Suitable for RAG implementation
- May require chunking strategy for scenario retrieval

### Previous Implementation Attempt

**Location:** `/old-resources/app/`

**Components:**
- Python application (app.py, app-version-2.py, app-old.py)
- ChromaDB database attempt
- Requirements file

**Status:** Reference only, not actively used in current project

**Note:** Documents previous technical approach but not detailed in thesis unless relevant to methodology discussion

---

## Open Questions and Next Steps

### Evaluation Methodology

**Questions:**
- What specific criteria will trainees use to score the system?
- How many evaluation sessions per trainee?
- What metrics define "effectiveness"?
  - Satisfaction scores?
  - Learning outcomes?
  - Confidence improvements?
  - Reasoning depth assessment?

### System Implementation

**Questions:**
- Is system prompt v3 final or continue refining?
- How to implement RAG for scenario retrieval?
  - Vector database selection
  - Chunking strategy
  - Retrieval threshold
- What LLM backend to use for deployment?
- How to handle Hebrew language requirements?

### Testing Protocol

**Questions:**
- Pilot testing approach?
- How many trainees for pilot vs full evaluation?
- What scenarios to use in testing?
- How to control for scenario difficulty?

### Thesis Structure

**Questions:**
- Literature review scope?
- Methodology chapter structure?
- How to present iterative design process?
- Evaluation results presentation?

---

## Timeline

**Phase 1 Completed (Foundation Building):**
- 2024-11-21: Material collection and organization
- 2024-11-22: Theory extraction, system prompt iterations, final synthesis, RAG strategy design, technical architecture finalization, scenario file preparation

**Key Deliverables:**
- System prompt (final version in `system-prompt-analysis.md`)
- Technical architecture (`TECHNICAL-DESIGN.md`)
- 18 processed scenario files
- Token analysis (scenarios: 21K tokens total, avg 1,181 per scenario)

**Next Steps:**
- Phase 2: System implementation (RAG, conversation manager, UI)
- Phase 3: Evaluation methodology design
- Pilot testing
- Full evaluation
- Analysis and thesis writing

---

## Document Maintenance

**Last Updated:** 2025-11-22

**Revision History:**
- 2025-11-22: Initial creation, Phase 1 completion documented
