# AI Prompt Assistant

## Project Overview

AI Prompt Assistant is a beginner-friendly Generative AI web application built with Python, Streamlit, LangChain, and an OpenAI chat model.

This version is focused on career interview preparation. Users can ask for mock interview questions, improve interview answers, polish resume bullets, and get role-specific preparation guidance.

## Features

- Simple Streamlit web interface
- Prompt text area for user questions
- Generate Response button
- Clear button to reset the prompt and answer
- OpenAI chat model access through LangChain
- LangChain Expression Language pipeline
- Environment-variable based API key handling
- Configurable model using `OPENAI_MODEL`
- Helpful error messages for common API issues

## Folder Structure

```text
Basic_Langchain_demo/
|-- app.py
|-- requirements.txt
|-- README.md
|-- .env.example
|-- .gitignore
```

## Prerequisites

- Python 3.10 or newer
- An OpenAI API key
- Basic terminal or command-line knowledge

## Setup Instructions

Open a terminal and move into the project folder:

```bash
cd Basic_Langchain_demo
```

## Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

### Windows PowerShell

```powershell
pip install -r requirements.txt
```

### macOS/Linux

```bash
pip install -r requirements.txt
```

## Environment Variable Setup

Copy `.env.example` to a new file named `.env`.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS/Linux

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder value with your real OpenAI API key:

```env
OPENAI_API_KEY=your_real_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
```

If `OPENAI_MODEL` is not set, the app automatically uses `gpt-4.1-mini`.

## Run the Application

Use this command from inside the `Basic_Langchain_demo` folder:

```bash
streamlit run app.py
```

## Basic Usage

1. Start the Streamlit app.
2. Enter an interview-prep prompt in the text area.
3. Click Generate Response.
4. Read the generated answer.
5. Click Clear to reset both the prompt and the response.

Example prompts:

- Generate 5 behavioral interview questions for a data analyst role.
- Review my answer using the STAR method.
- Improve this resume bullet for a Python developer role.
- Give me a 7-day interview preparation plan for a software engineering role.

## Troubleshooting

### OpenAI API key not found

Make sure the `.env` file exists and contains:

```env
OPENAI_API_KEY=your_real_openai_api_key
```

Restart Streamlit after changing environment variables.

### Authentication failed

Check that your OpenAI API key is correct and active.

### Rate limit error

Wait a short time and try again. You may need to check your OpenAI usage limits.

### Connection error

Check your internet connection and try again.

### Module not found

Make sure your virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

## Security Note

Never commit your `.env` file to Git. It may contain private API keys or sensitive configuration values. This project includes `.env` in `.gitignore` to help prevent accidental commits.
