# config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Chroma phones home by default and spams stderr when the call fails.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

# Load environment variables from .env
load_dotenv()

# ========= OpenAI =========
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Empty string is not a valid endpoint - fall back to the default OpenAI URL.
BASE_URL = os.getenv("base_url") or None

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

ENCODING_NAME = "cl100k_base"
# ========= Paths =========
PDF_PATH = "data/"
VECTOR_DB_DIR = "vector_db/powerBI_db"

# ========= Chunking =========
CHUNK_SIZE = 512 
CHUNK_OVERLAP = 16

# ========= Retrieval =========
TOP_K = 5