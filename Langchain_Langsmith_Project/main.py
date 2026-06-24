from pathlib import Path
import os
import sys

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent


def load_environment() -> None:
    """Load API keys and tracing settings from .env files."""
    load_dotenv(PROJECT_ROOT / ".env")
    load_dotenv(BASE_DIR / ".env", override=True)

    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGSMITH_PROJECT", "simple-rag-app")

    required_vars = ["OPENAI_API_KEY", "LANGSMITH_API_KEY"]
    missing_vars = [name for name in required_vars if not os.getenv(name)]

    if missing_vars:
        missing = ", ".join(missing_vars)
        raise RuntimeError(f"Missing required environment variable(s): {missing}")


def build_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Answer clearly and concisely.",
            ),
            ("human", "{question}"),
        ]
    )

    model = ChatOpenAI(model="gpt-4o-mini")
    output_parser = StrOutputParser()

    return prompt | model | output_parser


def main() -> None:
    load_environment()

    question = " ".join(sys.argv[1:]).strip()
    if not question:
        question = input("Enter your prompt: ").strip()

    if not question:
        raise RuntimeError("Prompt cannot be empty.")

    chain = build_chain()
    response = chain.invoke({"question": question})

    print("\nModel response:\n")
    print(response)
    print(f"\nLangSmith project: {os.getenv('LANGSMITH_PROJECT')}")


if __name__ == "__main__":
    main()
