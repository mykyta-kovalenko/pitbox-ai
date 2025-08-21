# Code Formatting

This project uses **ruff** for automatic code formatting and linting.

## VS Code Setup (Recommended)

1. Install the **Ruff extension**: `charliermarsh.ruff`
2. Reload VS Code window after installation
3. Ensure Python interpreter points to `.venv/bin/python`
4. Verify `.vscode/settings.json` contains:

```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "ruff.path": ["./.venv/bin/ruff"]
}
```

Then formatting happens automatically:
- ✅ Format on save (`Cmd+S`)
- ✅ Real-time linting with error highlights
- ✅ Auto-organize imports

## Manual Commands

```bash
# Check code quality
make quality

# Auto-fix issues  
make lint-fix

# Format files
make format

# Watch files and auto-format on changes
make watch
```

## Before Committing

Always run:
```bash
make quality
```

## Style Rules

- **88 character** line limit
- **Automatic** import sorting
- **Black-compatible** formatting