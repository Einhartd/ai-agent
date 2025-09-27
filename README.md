# ai-agent

A simple Python AI agent framework built to experiment with Gemini-style agents, function calling, and modular tools.

This project was created as a hands-on learning exercise to better understand LLM-based agents and Python tooling.

---

## Features

- Gemini-style prompt-response loop
- Supports function/tool calling (e.g., calculator)
- Modular structure for adding new tools
- `--verbose` flag for detailed logs (token usage, API calls, etc.)
- Fast dependency management with [`uv`](https://github.com/astral-sh/uv)

---

## Setup

### Requirements

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) installed (`pip install uv`)
- API key for Gemini or OpenAI-compatible model

### Installation

```bash
git clone https://github.com/Einhartd/ai-agent.git
cd ai-agent
uv venv
uv pip install -r requirements.txt
```

### API key
Set your API key in a .env file or as an environment variable:
```python
API_KEY=your_api_key_here
```

## Basic Usage

### Basic prompt interaction
```python
uv run main.py "I think that calculator/pkg/calculator.py has bug in it 3+7*2 returns 20 instead of 17"
```

### Use `--verbose` for detailed input
```python
uv run main.py --verbose "how does the calculator render results to the console?"
```

```python
- Calling function: get_files_info
Calling function: get_files_info({})
- Calling function: get_file_content
Calling function: get_file_content({'file_path': 'main.py'})
- Calling function: get_file_content
Calling function: get_file_content({'file_path': 'pkg/render.py'})

User prompt: how does the calculator render results to the console?
Prompt tokens: 986
Response tokens: 63
Final response:
As suspected, the `format_json_output` function formats the result and the expression into a JSON string using `json.dumps()`. The `main.py` script then prints this JSON string to the console using the `print()` function. This is how the calculator renders results to the console.
```





