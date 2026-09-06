"""Create the project virtual environment and install dependencies.

    python3.12 create_venv.py

Python 3.12+ is required: src/ingest.py uses f-strings with nested same-type
quotes, which is a syntax error on 3.11 and below.
"""

import os
import subprocess
import sys
import venv

VENV_DIR = "venv"
MIN_PYTHON = (3, 12)


def main():
    if sys.version_info < MIN_PYTHON:
        sys.exit(
            f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required, "
            f"but this is {sys.version.split()[0]}. Try: python3.12 create_venv.py"
        )

    if os.path.isdir(VENV_DIR):
        print(f"{VENV_DIR}/ already exists - reusing it.")
    else:
        print(f"Creating {VENV_DIR}/ ...")
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)

    bin_dir = "Scripts" if os.name == "nt" else "bin"
    python = os.path.join(VENV_DIR, bin_dir, "python")

    print("Installing dependencies from requirements.txt ...")
    subprocess.check_call([python, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([python, "-m", "pip", "install", "-r", "requirements.txt"])

    if not os.path.exists(".env"):
        print("\nNo .env found. Copy .env.example to .env and add your OPENAI_API_KEY.")

    print("\nDone. Next:")
    print(f"  {python} demo.py            # end-to-end demo")
    print(f"  {python} src/rag_chat.py    # interactive chat")


if __name__ == "__main__":
    main()
