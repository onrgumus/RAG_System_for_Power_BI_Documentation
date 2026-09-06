# Power BI RAG Documentation Assistant

> Forked from [B-xD/RAG_System_for_Power_BI_Documentation](https://github.com/B-xD/RAG_System_for_Power_BI_Documentation).
> The original RAG pipeline and notebooks are their work; this fork fixes several
> bugs and adds citations, a demo, and packaging — see
> [Attribution](#attribution) below.

Ask questions about the Power BI documentation in natural language and get
answers grounded in the source, with page citations.

```
Q: How do I access the Query Editor in Power BI Desktop?
A: To access the Query Editor in Power BI Desktop, click on the "Edit Queries"
   option on the Home tab of the Power BI Desktop ribbon (p.161).

Q: What is the average house price in Istanbul?
A: I could not find this information in the documentation.
```

## Overview

A Retrieval-Augmented Generation (RAG) system that enables users to query
Power BI documentation using natural language and receive accurate,
citation-grounded answers.

## Business Problem

Power BI is one of the most widely used business intelligence platforms for data
analysis and reporting. Despite its power, analysts often struggle to fully
utilize its capabilities due to the size, complexity, and fragmentation of the
official documentation. Important concepts such as Power Query, DAX functions,
data modeling, and report design are scattered across hundreds of pages, making
it difficult to quickly locate precise answers.

As a result:

* Analysts waste time searching documentation
* Features are misunderstood or underutilized
* Decision-making is delayed
* Business value from Power BI investments is reduced

**Solution:** a RAG system that indexes the documentation, retrieves the most
relevant passages by vector similarity, and generates answers strictly grounded
in those passages — with page-level citations for every answer.

## Quickstart

Requires **Python 3.12+** and an OpenAI API key.

```bash
# 1. Environment + dependencies
python3.12 create_venv.py

# 2. API key
cp .env.example .env
#    then edit .env and set OPENAI_API_KEY

# 3. End-to-end demo (builds the vector store on first run)
./venv/bin/python demo.py

# 4. Interactive chat
./venv/bin/python src/rag_chat.py
```

Run all commands from the project root — `PDF_PATH` and `VECTOR_DB_DIR` in
`src/config.py` are relative paths.

To rebuild the vector store from scratch, delete `vector_db/` and re-run either
script.

## Project Structure

```text
RAG_System_for_Power_BI_Documentation/
├── data/
│   └── Introducing_Power_BI.pdf   # the indexed source document
├── vector_db/
│   └── powerBI_db/                # generated, git-ignored
├── src/
│   ├── config.py                  # models, paths, chunking & retrieval settings
│   ├── ingest.py                  # PDF loading + chunking
│   ├── embeddings.py              # vector DB creation
│   ├── retriever.py               # similarity search
│   ├── prompts.py                 # prompts + context/history formatting
│   └── rag_chat.py                # CLI chatbot
├── notebooks/
│   ├── 1 - Building a _(RAG)_System_for_Power_BI_Documentation.ipynb
│   └── 2- Evaluating_(RAG)_System_for_Power_BI_Documentation.ipynb
├── demo.py                        # non-interactive end-to-end demo
├── create_venv.py                 # environment bootstrap
├── requirements.txt
└── .env.example
```

## RAG Pipeline

| Stage | Module | Description |
|---|---|---|
| Indexing | `ingest.py`, `embeddings.py` | Chunking (512 tokens, 16 overlap) → embedding → vector storage |
| Retrieval | `retriever.py` | Cosine similarity search, top 5 chunks |
| Generation | `rag_chat.py`, `prompts.py` | `gpt-4o-mini` at `temperature=0`, grounded in retrieved context |

The source document produces **407 chunks**.

## Grounding and Citations

Retrieved passages are passed to the model with their page numbers attached:

```text
[Source 2 | Introducing_Power_BI.pdf p.161]
<passage text>
```

The system prompt requires an inline `(p.N)` citation for every claim, and
instructs the model to reply `"I could not find this information in the
documentation."` rather than answer from outside knowledge. `demo.py` includes
a deliberately out-of-scope question to exercise that guardrail.

## Configuration

All settings live in `src/config.py`:

| Setting | Default |
|---|---|
| `EMBEDDING_MODEL` | `text-embedding-3-small` |
| `CHAT_MODEL` | `gpt-4o-mini` |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | 512 / 16 tokens |
| `TOP_K` | 5 |

`.env` holds `OPENAI_API_KEY`, and optionally `base_url` for an OpenAI-compatible
endpoint. Leave `base_url` commented out to use the default OpenAI endpoint —
setting it to an empty string will break the client.

## Attribution

The original project — the RAG pipeline (`ingest.py`, `embeddings.py`,
`retriever.py`), both notebooks, and the business framing — was created by
[**B-xD**](https://github.com/B-xD) in
[RAG_System_for_Power_BI_Documentation](https://github.com/B-xD/RAG_System_for_Power_BI_Documentation).
This fork builds on that work.

### Changes in this fork

Bug fixes:

- **Conversation history never reached the model.** `rag_chat.py` passed
  `chat_history` to `.format()`, but `USER_PROMPT_TEMPLATE` had no
  `{chat_history}` placeholder, so it was silently discarded. History is now
  stored as (question, answer) pairs and rendered into the prompt.
- **Citations could not be produced.** The system prompt asked for page numbers,
  but only `page_content` was sent as context — `metadata['page_label']` was
  never used. Retrieved passages now carry `[Source N | file p.X]` headers and
  answers cite inline.
- **Importing `rag_chat` started the chat loop**, because `main()` and
  `get_retriever()` ran at module level. Now behind an `if __name__` guard, with
  the logic split into reusable `answer()` / `cite()` functions.
- **An empty `base_url` broke the OpenAI client.** `os.getenv` returns `""`
  rather than `None`, which the client treats as a real endpoint. Normalised in
  `config.py`.
- **ChromaDB telemetry noise** on every query, silenced via client settings.

Additions:

- `demo.py` — non-interactive end-to-end demo, builds the vector store on first
  run and includes an out-of-scope question that exercises the grounding
  guardrail.
- `create_venv.py` — was an empty file; now a working bootstrap with a Python
  3.12 version check.
- `requirements.txt` — was empty; populated from the actual imports.
- `.env.example`, expanded README, `.DS_Store` cleanup.

## Technologies Used

- OpenAI (`gpt-4o-mini`, `text-embedding-3-small`)
- LangChain
- ChromaDB
- Python 3.12
