"""
Scenario Ingestion Script

Reads scenario markdown files from /scenarios directory and ingests them into ChromaDB
with Gemini Embedding 001 embeddings for RAG retrieval.
"""

import os
import sys
from pathlib import Path
import re

# Add app backend to path
app_dir = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_dir))

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from backend.config import get_config


def extract_scenario_title(content: str) -> str:
    """
    Extract scenario title from markdown heading.

    Args:
        content: Markdown file content

    Returns:
        Scenario title, or "Untitled" if not found
    """
    # Look for first heading (# Scenario XX: Title)
    match = re.search(r'^#\s+Scenario\s+\d+:\s*(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Fallback: look for any first-level heading
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    return "Untitled Scenario"


def ingest_scenarios():
    """Main ingestion function."""
    print("🚀 Starting scenario ingestion...\n")

    # Get configuration
    config = get_config()
    config.validate()

    # Initialize embedding model
    print(f"📊 Initializing embedding model: {config.embedding_model}")
    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.embedding_model,
        google_api_key=config.google_api_key
    )

    # Initialize ChromaDB
    print(f"💾 Initializing ChromaDB at: {config.chroma_db_path}")
    vector_store = Chroma(
        collection_name=config.chroma_collection_name,
        embedding_function=embeddings,
        persist_directory=config.chroma_db_path
    )

    # Find scenario files
    scenarios_dir = Path(__file__).parent.parent / "scenarios"
    if not scenarios_dir.exists():
        print(f"❌ Scenarios directory not found: {scenarios_dir}")
        sys.exit(1)

    scenario_files = sorted(scenarios_dir.glob("scenario-*.md"))

    if not scenario_files:
        print(f"❌ No scenario files found in: {scenarios_dir}")
        sys.exit(1)

    print(f"📁 Found {len(scenario_files)} scenario files\n")

    # Ingest each scenario
    documents = []

    for i, file_path in enumerate(scenario_files, 1):
        print(f"[{i}/{len(scenario_files)}] Processing: {file_path.name}")

        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract metadata
            scenario_id = file_path.stem  # e.g., "scenario-01"
            title = extract_scenario_title(content)

            print(f"  ├─ ID: {scenario_id}")
            print(f"  ├─ Title: {title}")
            print(f"  └─ Content length: {len(content)} chars")

            # Create document
            doc = Document(
                page_content=content,
                metadata={
                    "id": scenario_id,
                    "title": title,
                    "source": file_path.name
                }
            )

            documents.append(doc)

        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            continue

    if not documents:
        print("\n❌ No documents to ingest")
        sys.exit(1)

    # Add documents to vector store
    print(f"\n🔄 Embedding and storing {len(documents)} documents...")
    try:
        ids = vector_store.add_documents(documents=documents)
        print(f"✅ Successfully ingested {len(ids)} scenarios")

        # Verify
        collection = vector_store._collection
        count = collection.count()
        print(f"📊 ChromaDB collection '{config.chroma_collection_name}' now contains {count} documents")

    except Exception as e:
        print(f"\n❌ Ingestion failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n✨ Ingestion complete!")


if __name__ == "__main__":
    ingest_scenarios()
