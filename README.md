# Custom Local AI Agent Framework

A lightweight, zero-framework Python engine for autonomous AI agents powered by local LLMs via Ollama. Built from scratch without LangChain or LlamaIndex.

## Key Features
- **Zero Heavy Dependencies:** Core logic built using pure Python, `ollama`, and `pydantic`.
- **Automatic Schema Generation:** Decorator-based function inspection to convert standard Python type hints into LLM tool schemas.
- **Robust ReAct Loop:** Handles iterative reasoning, multi-step tool execution, and error self-correction.
- **Local & Private:** Runs completely offline using open-weights models (`qwen2.5` / `llama3.1`).

## Project Structure
- `agent/tools.py`: Tool registry and schema extractor.
- `agent/memory.py`: Message history and context management.
- `agent/core.py`: Main agent ReAct loop and execution engine.
- `main.py`: Interactive CLI entry point.
