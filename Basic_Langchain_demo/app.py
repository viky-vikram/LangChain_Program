import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import APIConnectionError, AuthenticationError, OpenAIError, RateLimitError


load_dotenv()


DEFAULT_MODEL = "gpt-4.1-mini"
MODEL_NAME = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Provide clear, accurate, well-structured, "
    "and beginner-friendly answers. You specialize in career interview preparation, "
    "including mock interview questions, answer feedback, resume bullet improvements, "
    "and role-specific preparation tips."
)


st.set_page_config(
    page_title="Career Advancement AI",
    page_icon="AI",
    layout="centered",
)


def has_api_key() -> bool:
    """Check whether the required OpenAI API key is configured."""
    return bool(os.getenv("OPENAI_API_KEY"))


@st.cache_resource(show_spinner=False)
def get_response_chain(model_name: str):
    """Create and cache the LangChain prompt, model, parser, and pipeline."""
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{user_question}"),
        ]
    )

    model = ChatOpenAI(
        model=model_name,
        temperature=0.3,
    )
    output_parser = StrOutputParser()

    return prompt_template | model | output_parser


def generate_response(user_question: str) -> str:
    """Validate the prompt, run the LangChain pipeline, and return the answer."""
    cleaned_question = user_question.strip()

    if not cleaned_question:
        raise ValueError("Please enter a question or prompt before generating a response.")

    if not has_api_key():
        raise EnvironmentError(
            "OPENAI_API_KEY is missing. Add it to your environment or .env file first."
        )

    try:
        chain = get_response_chain(MODEL_NAME)
        response = chain.invoke({"user_question": cleaned_question})
        return response.strip()
    except AuthenticationError as exc:
        raise RuntimeError(
            "Authentication failed. Please check that your OpenAI API key is valid."
        ) from exc
    except RateLimitError as exc:
        raise RuntimeError(
            "The request was rate limited. Please wait a moment and try again."
        ) from exc
    except APIConnectionError as exc:
        raise RuntimeError(
            "Could not connect to the OpenAI API. Your API key is configured, so please "
            "check your internet connection, VPN/proxy settings, firewall rules, or "
            "whether https://api.openai.com is reachable from this network."
        ) from exc
    except OpenAIError as exc:
        raise RuntimeError(
            "The OpenAI API returned an error. Please try again later."
        ) from exc
    except Exception as exc:
        raise RuntimeError(
            "Something went wrong while generating the response. Please try again."
        ) from exc


def clear_form() -> None:
    """Reset the prompt and generated response in Streamlit session state."""
    st.session_state.user_prompt = ""
    st.session_state.generated_response = ""


if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

if "generated_response" not in st.session_state:
    st.session_state.generated_response = ""


with st.sidebar:
    st.header("Configuration")
    st.write(f"**Model:** `{MODEL_NAME}`")

    if has_api_key():
        st.success("OpenAI API key detected.")
    else:
        st.error("OpenAI API key not found.")
        st.info("Create a `.env` file and add `OPENAI_API_KEY=your_api_key_here`.")

    st.caption(
        "If generation shows a connection error, confirm this machine can access "
        "`https://api.openai.com`."
    )

    st.divider()
    st.write("Try prompts such as:")
    st.caption("Generate 5 behavioral interview questions for a data analyst role.")
    st.caption("Review my answer using the STAR method.")
    st.caption("Improve this resume bullet for a Python developer role.")


st.title("Career Advancement AI")
st.write(
    "A simple LangChain and Streamlit app for career interview preparation. "
    "Ask for mock interview questions, answer feedback, resume bullet improvements, "
    "or role-specific preparation tips."
)

st.text_area(
    "Enter your interview-prep question or prompt",
    key="user_prompt",
    height=180,
    placeholder="Example: Give me 8 interview questions for a junior Python developer role.",
)

generate_button, clear_button = st.columns(2)

with generate_button:
    should_generate = st.button(
        "Generate Response",
        type="primary",
        disabled=not has_api_key(),
        use_container_width=True,
    )

with clear_button:
    st.button("Clear", on_click=clear_form, use_container_width=True)

if should_generate:
    try:
        with st.spinner("Generating response..."):
            st.session_state.generated_response = generate_response(
                st.session_state.user_prompt
            )
    except ValueError as exc:
        st.warning(str(exc))
    except EnvironmentError as exc:
        st.error(str(exc))
    except RuntimeError as exc:
        st.error(str(exc))

st.subheader("Generated Response")

if st.session_state.generated_response:
    st.markdown(st.session_state.generated_response)
else:
    st.info("Your generated response will appear here.")

st.divider()
st.caption(
    "Security note: API keys are read from environment variables and are never shown "
    "in the app interface."
)
