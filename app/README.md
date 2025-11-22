# OT Mentor AI System

An AI-powered expert mentor for Occupational Therapy trainees, built as part of an MSc thesis project. The system uses Large Language Models and RAG (Retrieval-Augmented Generation) to guide OT students through professional reasoning.

## Overview

The system operates in two phases:

1. **Context Gathering (INTAKE)**: Conversationally collects information about the trainee, patient, and clinical scenario
2. **Reflective Mentoring (MENTORING)**: Uses retrieved scenarios and professional reasoning frameworks to guide the trainee through case analysis

## Architecture

- **Frontend**: Streamlit web interface
- **Backend**: Python with LangChain framework
- **LLM**: Gemini Flash 2.5 (Google AI)
- **Embeddings**: Gemini Embedding 001
- **Vector Store**: ChromaDB (local)
- **Persistence**: File-based session storage (JSON)

## Project Structure

```
app/
├── app.py                          # Streamlit frontend
├── backend/
│   ├── config.py                   # Configuration and settings
│   ├── prompts.py                  # System prompts and instructions
│   ├── tools.py                    # Template and context evaluator
│   ├── rag_retriever.py            # Scenario retrieval with ChromaDB
│   ├── session_manager.py          # File-based persistence
│   └── conversation_manager.py     # Main orchestration logic
├── data/
│   └── chroma_db/                  # ChromaDB vector store (created after ingestion)
├── sessions/                       # Session files (created at runtime)
│   └── <session-id>/
│       ├── template.json           # 18-field context template
│       ├── retrieved_scenarios.json # Retrieved scenario metadata
│       └── conversation.json       # Full conversation history
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
└── README.md                       # This file
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Google AI API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

Navigate to the app directory:
```bash
cd app
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your Google AI API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### Scenario Ingestion

Before running the app, you must ingest the scenario files into ChromaDB:

```bash
cd ..
python scripts/ingest_scenarios.py
```

This will:
- Read all scenario markdown files from `/scenarios`
- Generate embeddings using Gemini Embedding 001
- Store them in ChromaDB at `app/data/chroma_db`

Expected output:
```
🚀 Starting scenario ingestion...
📊 Initializing embedding model: models/embedding-001
💾 Initializing ChromaDB at: ./app/data/chroma_db
📁 Found 18 scenario files
...
✅ Successfully ingested 18 scenarios
✨ Ingestion complete!
```

### Running the Application

Start the Streamlit app:
```bash
cd app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Starting a Session

1. Open the app in your browser
2. Read the welcome message
3. Type your first message to begin

### Context Gathering Phase

The system will conversationally gather information about:
- **Therapist Profile**: Role, experience, specialization, setting
- **Patient Profile**: Age, gender, diagnosis, cultural background, family structure
- **Treatment Context**: Setting, duration, treatment type
- **The Dilemma**: Main difficulty, behaviors, impact on function

The system asks natural questions and accepts "I don't know" responses. Critical fields are marked with (*) in the internal template.

### Phase Transition

Once sufficient context is gathered (all 5 critical fields + 7 additional fields = 12/18 minimum), the system:
1. Generates a summary of the case
2. Retrieves 2 most relevant scenarios from ChromaDB
3. Transitions to mentoring phase
4. Shows you which scenarios were matched

### Mentoring Phase

The system guides you through **Professional Reasoning**:

1. **Scientific Reasoning**: Evidence-based decisions, diagnosis understanding
2. **Narrative Reasoning**: Patient's story, family perspective, therapeutic history
3. **Pragmatic Reasoning**: Resources, equipment, time, institutional constraints
4. **Ethical Reasoning**: Confidentiality, dignity, competence, scope of practice
5. **Interactive Reasoning**: Collaboration, team communication, rapport building

The mentor:
- Asks **ONE question at a time**
- Never provides direct solutions
- Identifies gaps in your reasoning
- References professional knowledge (scope of practice, intervention approaches, cognitive strategies)

## Session Management

### Session Persistence

Each session creates a folder in `app/sessions/<session-id>/` with:
- `template.json`: Filled context template
- `retrieved_scenarios.json`: Metadata of matched scenarios
- `conversation.json`: Complete conversation history

Sessions are saved incrementally (after each message).

### Starting a New Session

Click "🔄 New Session" in the sidebar to reset and start fresh.

## Technical Details

### Phase Transition Criteria

Transition from INTAKE to MENTORING when:
- **ALL** of these critical fields are filled:
  - therapist_role
  - years_experience
  - therapist_setting
  - patient_age
  - diagnosis
  - cultural_background
  - marital_status
  - treatment_setting
  - main_difficulty
  - impact_daily_function
- **AND** at least 7 additional fields are filled
- **Total minimum**: 12/18 fields

### RAG Strategy

1. Generate natural language summary from filled template
2. Embed summary with Gemini Embedding 001
3. Query ChromaDB with cosine similarity
4. Retrieve top-K=2 scenarios
5. Append scenarios to conversation context
6. Mentor uses scenarios internally (does not quote them)

### Conversation Flow

Messages are accumulative:
1. Start: `[BASE_SYSTEM_PROMPT, PHASE_1_INSTRUCTIONS]`
2. Phase 1: Add user/assistant messages
3. Transition: Append `[PHASE_2_INSTRUCTIONS, SCENARIOS, USAGE_INSTRUCTIONS]`
4. Phase 2: Continue conversation with full context

No messages are replaced - full history is preserved.

## Configuration

### Model Configuration

Located in `backend/config.py`:

```python
ModelConfig(
    technical_name="gemini-2.0-flash-exp",  # LangChain identifier
    provider_api="google",
    ui_name="Gemini Flash 2.5",
    ui_locked=True  # Model selection locked in UI
)
```

### Application Settings

```python
class AppConfig:
    embedding_model = "models/embedding-001"
    top_k_scenarios = 2
    chroma_db_path = "./app/data/chroma_db"
    chroma_collection_name = "ot_scenarios"
    sessions_dir = "./app/sessions"
```

## Troubleshooting

### "GOOGLE_API_KEY environment variable not set"
- Ensure `.env` file exists in `app/` directory
- Verify it contains `GOOGLE_API_KEY=your_key`

### "ChromaDB collection contains 0 documents"
- Run the ingestion script: `python scripts/ingest_scenarios.py`
- Verify scenario files exist in `/scenarios` directory

### "Import error: langchain_chroma"
- Install dependencies: `pip install -r requirements.txt`

### Streamlit shows "waiting for rerun"
- Check terminal for errors
- Verify all imports resolve correctly

## Development

### Adding New Scenarios

1. Add scenario markdown file to `/scenarios` directory
2. Name it `scenario-XX.md` (sequential numbering)
3. Re-run ingestion: `python scripts/ingest_scenarios.py`

### Modifying System Prompts

Edit `backend/prompts.py`:
- `BASE_SYSTEM_PROMPT`: Core mentor identity and reasoning frameworks
- `PHASE_1_INSTRUCTIONS`: Context gathering instructions
- `PHASE_2_INSTRUCTIONS`: Mentoring workflow
- `SCENARIO_USAGE_INSTRUCTIONS`: How to use retrieved scenarios

### Adjusting Phase Transition

Modify in `backend/config.py`:
```python
critical_fields_count = 5  # Must have all
additional_fields_count = 7  # Plus at least this many
min_total_fields = 12  # Total minimum
```

## Academic Context

This system is part of an MSc thesis project evaluating the effectiveness of LLM-based mentoring for occupational therapy trainees. The design focuses on:

- **Professional Reasoning**: Based on OT literature and practice standards
- **Socratic Method**: Guiding rather than prescribing
- **Context-Aware**: Using RAG to match similar cases
- **Scope of Practice**: Ensuring professional boundaries
- **Empowerment**: Building autonomous clinical reasoning skills

## References

- System prompt design: `../system-prompt-analysis.md`
- Technical architecture: `../TECHNICAL-DESIGN.md`
- Project overview: `../PROJECT-DESIGN.md`

## License

Academic use only. Part of MSc thesis research project.

## Contact

For questions about this implementation, refer to project documentation or thesis advisor.
