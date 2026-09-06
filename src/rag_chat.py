# rag_chat.py

from openai import OpenAI

from config import CHAT_MODEL, OPENAI_API_KEY, BASE_URL
from prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    format_context,
    format_history,
)
from retriever import get_retriever


def build_client():
    """OpenAI client. BASE_URL is optional; empty means 'use the default endpoint'."""
    return OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL or None)


def answer(question, retriever, client, history=None):
    """Answer one question from the documentation.

    Returns (answer_text, source_documents) so callers can show citations.
    """
    documents = retriever.invoke(question)

    prompt = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(
                context=format_context(documents),
                question=question,
                chat_history=format_history(history or []),
            ),
        },
    ]

    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=prompt,
            temperature=0,
        )
        return response.choices[0].message.content.strip(), documents
    except Exception as e:
        return f"Sorry, I encountered the following error:\n{e}", []


def cite(documents):
    """One-line list of the pages an answer was grounded in."""
    pages = []
    for doc in documents:
        meta = doc.metadata or {}
        page = meta.get("page_label") or meta.get("page")
        if page is not None and page not in pages:
            pages.append(page)
    return ", ".join(f"p.{p}" for p in pages)


def main():
    """Interactive CLI: ask questions until the user types 'q'."""
    retriever = get_retriever()
    client = build_client()
    history = []

    print("Hello! I am your Power BI assistant.")
    print("Ask a question, or type 'q' to exit.\n")

    while True:
        try:
            question = input("USER: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSee you later!")
            break

        if not question:
            continue
        if question.lower() == "q":
            print("See you later!")
            break

        text, documents = answer(question, retriever, client, history)
        print(f"\nPOWER BI ASSISTANT: {text}")

        sources = cite(documents)
        if sources:
            print(f"Sources: {sources}")
        print()

        history.append((question, text))


if __name__ == "__main__":
    main()
