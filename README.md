# Cleaning Robot Customer Service Assistant Agent

An intelligent customer service assistant for cleaning robots built with Streamlit, LangChain, RAG, and DashScope models.

## Features

- Conversational customer service interface based on `Streamlit`
- RAG knowledge retrieval over product FAQs, troubleshooting guides, and buying advice
- Tool-enabled agent workflow for weather lookup, user location, and external usage data
- Dynamic prompt switching for report-generation scenarios
- Local Chroma vector store for knowledge indexing

## Project Structure

```text
.
+-- app.py                  # Streamlit entry point
+-- react_agent.py          # Agent assembly and streaming execution
+-- model/                  # Model factory and API key resolution
+-- rag/                    # Retrieval and vector store logic
+-- tools/                  # Agent tools and middleware
+-- utils/                  # Config, logging, file loading, weather helpers
+-- config/                 # YAML configuration
+-- prompts/                # Prompt templates
+-- data/                   # Knowledge base files and external CSV data
```

## Requirements

- Python 3.11 or newer recommended
- A valid DashScope API key

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the API key:

```bash
copy .env.example .env
```

Set `DASHSCOPE_API_KEY` in your shell or `.env` loading workflow. The repository does not store a real key.

4. Build or refresh the vector database if needed:

```bash
python rag/vector_store.py
```

5. Start the app:

```bash
streamlit run app.py
```

## Configuration

- `config/rag.yml`: model names and DashScope key fallback
- `config/chroma.yml`: Chroma persistence path, retrieval count, chunking
- `config/agent.yml`: external CSV data path
- `config/prompts.yml`: prompt file locations

## Security Notes

- Do not commit `.env`, logs, or local vector databases
- Prefer `DASHSCOPE_API_KEY` from the environment
- Replace any local test keys before sharing the repository

## Current Knowledge Sources

- Product FAQ text files under `data/`
- Troubleshooting and maintenance documents
- PDF and TXT knowledge documents supported by the loader
- External usage records in `data/external/records.csv`

## License

Add a license file if you plan to open-source or redistribute the project.
