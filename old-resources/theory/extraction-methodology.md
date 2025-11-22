# Theory Paper Extraction Methodology

## Overview

This document explains the extraction and processing methodology applied to the four theory papers that form the knowledge base for the mentor system. Each paper was analyzed to identify content relevant to the mentor's role as defined in the Hebrew system prompt.

## Extraction Principles

Content was evaluated based on three criteria:
1. **Relevance to mentor function** - Does this help the mentor guide trainees effectively?
2. **Operational utility** - Can the mentor use this content to ask better questions or provide better feedback?
3. **Vocabulary and framework alignment** - Does this establish terminology or mental models the mentor needs?

## Theory Paper 1 - Cognitive Strategies

### Source Information
- Focus: Cognitive strategies in clinical education
- Total pages: 12

### Extraction Table

| Page(s) | Section Title / Content | Status | Rationale |
|---------|------------------------|--------|-----------|
| 1 | Title, Authors, Abstract (Eng/Fr), Intro | Partial | Included the Intro/Abstract definitions as they establish the Mentor's vocabulary. Excluded author bios/French text. |
| 2-3 | What are Strategies? / What is a Cognitive Strategy? | Included | Critical for the Mentor to define the core subject matter when guiding the trainee. |
| 3-4 | Types of Cognitive Strategies (Taxonomy) + Table 1 | Included | Essential. The Mentor needs this list to recognize what the trainee is describing or failing to describe. |
| 5 | Table 2 (Purpose Matrix) | Included | The matrix mapping strategies to purposes (Learning vs. Performance) is crucial for the Mentor to ask precision questions. |
| 5-6 | Dimensions / Framework 1: Attributes | Included | This is the core "mental model" the Mentor must use to challenge the trainee (e.g., asking about "Visibility" or "Permanence"). |
| 7-8 | Table 3 (Clinical Application/Examples) | Added | Re-thinking: Originally summarized. Now including full text as the Hebrew prompt asks for "examples" and "scenarios" to deepen understanding. Provides the "If-Then" logic the Mentor needs. |
| 8-9 | Framework 2: Strategy Use / Table 4 | Included | This is the "Clinical Reasoning Tool." It is the exact script the Mentor needs to evaluate the trainee's case (e.g., checking "Prerequisites"). |
| 10-11 | Discussion / Conclusion / Key Messages | Partial | Included "Key Messages" as high-level guardrails. Excluded general academic discussion. |
| 11-12 | References | Excluded | Not relevant for the System Prompt instructions. |

### Key Elements Extracted
- Core definitions and taxonomy of cognitive strategies
- Strategy attributes framework (Visibility, Permanence, etc.)
- Clinical reasoning tool for strategy evaluation
- Purpose matrix (Learning vs. Performance contexts)
- Clinical application examples and scenarios

---

## Theory Paper 2 - OT Supervision Guidelines

### Source Information
- Focus: Supervision of occupational therapists and assistants
- Total pages: 6

### Extraction Table

| Page(s) | Section Title / Content | Status | Rationale |
|---------|------------------------|--------|-----------|
| 1 | General Supervision | Included | Defines supervision/mentoring as a "cooperative process" to "foster professional competence." This aligns perfectly with the Hebrew prompt's definition of the AI's persona. |
| 1-2 | Supervision of OTs & OTAs / General Principles | Included | Essential for the AI to understand the scope of practice of the user (OT vs OTA). The "General Principles" (collaborative plan, client complexity) provide criteria for the AI to assess if the therapist is acting responsibly. |
| 2-3 | Roles and Responsibilities (Overview) | Included | Defines the domain of OT. The Hebrew prompt asks the AI to "guide reflective thinking" on the process. This section defines that process. |
| 3-4 | Evaluation / Intervention / Outcomes | Included | Critical. The Hebrew prompt requires the AI to correct the therapist if they are "acting improperly." These sections provide the objective rules (e.g., "The OT directs the evaluation") the AI needs to identify improper behavior. |
| 4 | Service Delivery Outside Settings | Included | Relevant for context if the user describes a non-traditional setting. |
| 4-5 | Supervision of Aides | Included | Included to ensure the AI knows the absolute floor of delegation (what cannot be done by skilled staff). |
| 5-6 | Summary / References / Authors | Partial | Included Summary for high-level alignment. Excluded References/Authors/Copyright boilerplate. |

### Key Elements Extracted
- Definition of supervision as cooperative process
- Scope of practice distinctions (OT vs OTA)
- Rules for proper professional behavior and delegation
- Evaluation and intervention responsibilities
- Service delivery context parameters

---

## Theory Paper 3 - Professional Standards

### Source Information
- Focus: OT professional standards and practice definitions
- Total pages: 7

### Extraction Table

| Page(s) | Section Title / Content | Status | Rationale |
|---------|------------------------|--------|-----------|
| 1-2 | Professional Standards Intro / Education & Licensure | Partial | Included the definition of OT "practice" and "Standards". Excluded the detailed U.S.-specific educational requirements (ACOTE accreditation, etc.) as the AI Mentor's role is clinical guidance, not HR credential verification. |
| 2-3 | Definitions (Activities, Client, Evaluation, etc.) | Included | High Value. The AI Mentor must use accurate terminology. The Hebrew prompt asks the AI to be "professional" and "authoritative"; using these exact definitions ensures that. |
| 3 | Standard I: Professional Standing and Responsibility | Included | Sets the baseline for professional behavior (e.g., "cultural humility," "advocacy," "evidence-informed practice"). Essential for the AI to assess the trainee's mindset. |
| 4 | Standard II: Service Delivery | Included | Defines "Direct" vs "Indirect" service. Relevant if the trainee asks about non-clinical roles (consulting). |
| 4 | Standard III: Screening, Evaluation, and Reevaluation | Included | Provides the rules of engagement for the evaluation phase. The AI needs this to catch procedural errors (e.g., if an OTA is doing something only an OT should do). |
| 5 | Standard IV: Intervention Process | Included | Defines the "Plan of Care" requirements. The Hebrew prompt mentions "filling a template"; these standards tell the AI what must be in that plan. |
| 5-6 | Standard V: Outcomes, Transition, and Discontinuation | Included | Critical for the "end-game" of therapy. The AI must know when it is appropriate to stop treatment or transition a client. |
| 6-7 | References / Authors / Citation | Excluded | Boilerplate academic data. |

### Key Elements Extracted
- Core OT practice and professional standards definitions
- Accurate clinical terminology for professional communication
- Professional behavior and responsibility baseline
- Service delivery models (direct vs indirect)
- Evaluation and screening procedures
- Intervention planning requirements (Plan of Care)
- Outcomes assessment and discontinuation criteria

---

## Theory Paper 4 - Professional Reasoning

### Source Information
- Focus: Clinical reasoning frameworks and intervention approaches
- Total pages: 7

### Extraction Table

| Page(s) | Section Title / Content | Status | Rationale |
|---------|------------------------|--------|-----------|
| 1 | Definition of Professional Reasoning / Types of Reasoning | Included | Critical. This defines the core mental model the Mentor must use (Scientific, Narrative, Pragmatic, Ethical, Interactive, Conditional). The Hebrew prompt explicitly asks for "reflective guidance," and these are the reflection categories. |
| 2-3 | Application Table (Reasoning x Intervention Stage) | Included | This table maps the reasoning types to specific actions (e.g., "Scientific reasoning" -> "Collecting data"). This provides the Mentor with the "If-Then" logic to guide the trainee. |
| 4 | Examples of Clinical Reasoning Questions | Included | Gold Mine. These are literal questions the Mentor can ask the trainee (e.g., "How is the difficulty perceived by the student?"). Direct inclusion is mandatory for the System Prompt. |
| 5 | Intervention Approaches (Health Promotion, Remediation, etc.) | Included | Defines the types of solutions the Mentor should help the trainee explore. Essential for the "Intervention Planning" phase. |
| 6-7 | Position Papers (Referenced) | Partial | List the titles of the position papers as they provide context on what is considered "standard practice" in Israel (e.g., OT in education, Learning Disabilities, Accessibility), but will not invent content for them as only the titles/links are provided. |

### Key Elements Extracted
- Professional reasoning types framework (Scientific, Narrative, Pragmatic, Ethical, Interactive, Conditional)
- Reasoning-to-action mapping across intervention stages
- Explicit clinical reasoning questions for mentor use
- Intervention approaches taxonomy (Health Promotion, Remediation, etc.)
- Israeli standard practice context through position paper references
