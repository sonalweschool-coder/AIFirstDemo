# AIFirstDemo

A small mathematical calculator agent.

## What it does

- Takes user input
- Understands the mathematical task
- Chooses the calculator tool
- Executes the calculation
- Returns the answer

Example:

```text
User: calculate 20% of 8500
Agent: I need percentage calculation
Answer: 1700
Tool: calculator
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload --port 8001
```

Open http://localhost:8001 in your browser.

On Windows PowerShell, activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Test

```bash
python -m pytest
```
