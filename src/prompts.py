# prompts.py

SYSTEM_PROMPT = """
You are a Power BI documentation assistant.

Rules:
- Answer ONLY using the provided context.
- Every excerpt in the context is prefixed with its source and page, like
  [Source 2 | Introducing_Power_BI.pdf p.143]. When you use an excerpt, cite it
  inline as (p.143). Cite every claim you make.
- If the answer is not in the context, say exactly:
  "I could not find this information in the documentation."
  Do not fall back on outside knowledge and do not guess.
- Be concise and accurate.
- Previous turns are provided for pronoun/follow-up resolution only. Never treat
  them as a source of facts; facts come only from the context.
"""

USER_PROMPT_TEMPLATE = """
Previous conversation:
{chat_history}

Context:
{context}

Question:
{question}

Answer:
"""

NO_HISTORY = "(no previous turns)"


def format_context(documents):
    """Render retrieved documents as a numbered, citable context block."""
    blocks = []
    for i, doc in enumerate(documents, 1):
        meta = doc.metadata or {}
        source = str(meta.get("source", "unknown")).split("/")[-1]
        page = meta.get("page_label") or meta.get("page")
        header = f"[Source {i} | {source}"
        if page is not None:
            header += f" p.{page}"
        header += "]"
        blocks.append(f"{header}\n{doc.page_content}")
    return "\n\n".join(blocks)


def format_history(history, max_turns=3):
    """Render the last few Q/A pairs; history is a list of (question, answer)."""
    if not history:
        return NO_HISTORY
    lines = []
    for question, answer in history[-max_turns:]:
        lines.append(f"User: {question}")
        lines.append(f"Assistant: {answer}")
    return "\n".join(lines)
