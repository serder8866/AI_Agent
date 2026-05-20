# AI Agent with Tool Use

A command-line AI agent built in Python using Google's Gemini API. The agent accepts a natural language prompt and iteratively reasons toward a solution by calling tools — reading files, writing files, listing directories, and executing Python code — until it produces a final answer or reaches a maximum iteration limit.

This was built as a structured exercise in LLM agent architecture. The same agentic loop pattern (system prompt → model call → tool dispatch → result → repeat) underpins real-world AI coding assistants like GitHub Copilot Agent and Claude Code.

---

## What it does

Given a prompt like *"Fix the bug in calculator/main.py"*, the agent will:

1. Call the Gemini API with a system prompt and available tool definitions
2. Receive a function call from the model (e.g. `get_file_content("calculator/main.py")`)
3. Execute the function locally and return the result to the model
4. Repeat until the model produces a final text response — or `MAX_ITERS` is reached

```bash
python main.py "Fix the bug in the calculator" --verbose
```

---

## Architecture

```
main.py          — Entry point; argument parsing, agent loop (bounded by MAX_ITERS)
prompts.py       — System prompt defining the agent's behaviour and constraints
call_function.py — Dispatcher: maps model function calls to local Python functions
functions/       — Tool implementations (file read/write, directory list, Python execution)
calculator/      — Sample buggy codebase used as a test target for the agent
config.py        — Constants (MAX_ITERS, model settings)
```

The agent loop in `main.py` follows a standard pattern:

```
User prompt → [Model call → Function call? → Execute tool → Feed result back] × N → Final response
```

---

## Key concepts demonstrated

- **Tool use / function calling** — Defining tools as structured schemas and dispatching model-requested calls
- **Agentic loops** — Iterative reasoning with a bounded step limit to prevent runaway execution
- **Prompt engineering** — System prompt design to constrain agent behaviour
- **Error handling** — Graceful handling of missing API responses, null function results, and iteration limits
- **Unit testing** — Separate test files for each tool function

---

## Setup

```bash
git clone https://github.com/serder8866/AI_Agent.git
cd AI_Agent
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install google-genai python-dotenv
```

Create a `.env` file with your Gemini API key:

```
GEMINI_API_KEY=your_key_here
```

Then run:

```bash
python main.py "your prompt here"
python main.py "your prompt here" --verbose   # shows token counts and tool call results
```

---

## What I'd extend next

- **Memory** — Persisting conversation history across sessions so the agent can resume work
- **More tools** — Web search, API calls, or domain-specific tools (e.g. running NLP pipelines)
- **Streaming output** — Real-time token streaming for a more responsive CLI experience
- **Sandboxed execution** — Running the Python execution tool in an isolated environment for safety

---

## Built with

- [Google Gemini API](https://ai.google.dev/) (`gemini-2.5-flash`)
- [`google-genai`](https://pypi.org/project/google-genai/) Python SDK
- [`python-dotenv`](https://pypi.org/project/python-dotenv/)
