"""End-to-end demo of the Power BI RAG assistant.

Runs a fixed set of questions through the full pipeline (retrieve -> generate)
and prints each answer with its page citations. Non-interactive, so it doubles
as a smoke test.

    python demo.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from config import OPENAI_API_KEY, VECTOR_DB_DIR  # noqa: E402
from rag_chat import answer, build_client, cite  # noqa: E402
from retriever import get_retriever  # noqa: E402

QUESTIONS = [
    "How do I access the Query Editor in Power BI Desktop?",
    "What is a dashboard and how does it differ from a report?",
    "How do I share a dashboard with a colleague?",
    # Deliberately outside the documentation: shows the grounding guardrail.
    "What is the average house price in Istanbul?",
]


def ensure_vector_db():
    """Build the vector store on first run so the demo works from a fresh clone."""
    if os.path.isdir(VECTOR_DB_DIR) and os.listdir(VECTOR_DB_DIR):
        return
    print(f"Vector store not found at {VECTOR_DB_DIR!r} - building it once...\n")
    from embeddings import create_vector_db

    create_vector_db()
    print("\nVector store ready.\n")


def main():
    if not OPENAI_API_KEY:
        sys.exit("OPENAI_API_KEY is not set. Copy .env.example to .env and fill it in.")

    ensure_vector_db()

    retriever = get_retriever()
    client = build_client()
    history = []

    print("=" * 72)
    print("POWER BI RAG ASSISTANT - DEMO")
    print("=" * 72)

    for i, question in enumerate(QUESTIONS, 1):
        print(f"\n[{i}/{len(QUESTIONS)}] Q: {question}")
        print("-" * 72)

        text, documents = answer(question, retriever, client, history)
        print(f"A: {text}")

        sources = cite(documents)
        print(f"\nRetrieved pages: {sources or '(none)'}")

        history.append((question, text))

    print("\n" + "=" * 72)
    print("Demo complete. For the interactive chat run: python src/rag_chat.py")
    print("=" * 72)


if __name__ == "__main__":
    main()
