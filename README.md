# AI Work Project

A comprehensive Python project with AI capabilities, featuring virtual environment management, testing, logging, and configuration management.

## Features

- 🐍 **Python 3.9+** with virtual environment
- ✅ **pytest** testing framework with coverage
- 📝 **Comprehensive logging** with configurable levels
- 🔧 **Environment variables** support via `.env` files  
- 🤖 **AI Configuration** via YAML files (prompts, models, etc.)
- 📁 **Clean project structure** with src layout
- 🔍 **Code quality tools** (black, flake8, mypy)
- 📊 **Development tools** and utilities

## Project Structure

```
aiwork601/
├── .github/
│   └── copilot-instructions.md
├── src/
│   └── aiwork/
│       ├── __init__.py
│       ├── config/
│       │   ├── __init__.py
│       │   ├── settings.py
│       │   └── logging_config.py
│       ├── ai/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── prompts.py
│       └── utils/
│           ├── __init__.py
│           └── logger.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_config.py
│   └── test_ai.py
├── config/
│   ├── ai_config.yaml
│   └── logging.yaml
├── .env.example
├── .env
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── pytest.ini
└── README.md
```

## Quick Start

### 1. Set up virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements-dev.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run tests
```bash
pytest
```

### 5. Start development
```bash
python -m src.aiwork
```

## Configuration

### Environment Variables (.env)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `AI_API_KEY`: Your AI service API key
- `AI_MODEL`: Default AI model to use
- `DATABASE_URL`: Database connection string (if needed)

### AI Configuration (config/ai_config.yaml)
Configure AI models, prompts, and behavior settings in the YAML file.

### Logging (config/logging.yaml)
Centralized logging configuration with multiple handlers and formatters.

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_config.py
```

### Code Quality
```bash
# Format code
black src tests

# Lint code
flake8 src tests

# Type checking
mypy src
```

## Contributing

1. Create virtual environment and install dev dependencies
2. Write tests for new features
3. Ensure all tests pass and code quality checks pass
4. Update documentation as needed

## License

This project is licensed under the MIT License.