# Contributing to Workflow Automation Dashboard

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](../../issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)
   - Screenshots if applicable

### Suggesting Features

1. Check [existing feature requests](../../issues?q=is%3Aissue+label%3Aenhancement)
2. Create a new issue with:
   - Clear use case
   - Expected behavior
   - Why this would be valuable

### Pull Requests

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes following our coding standards
4. Add tests if applicable
5. Ensure all tests pass: `pytest tests/`
6. Commit with clear messages
7. Push to your fork
8. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/workflow-automation-dashboard.git
cd workflow-automation-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Run tests
pytest tests/ -v
```

## Coding Standards

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Write tests for new features

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
feat: add support for JSON file uploads
fix: resolve duplicate row detection bug
docs: update API endpoint documentation
test: add tests for report generator
refactor: simplify data cleaning logic
```

## Code Review Process

1. All PRs require at least one review
2. CI tests must pass
3. Code must follow style guidelines
4. Changes should be focused and well-documented

## Questions?

Feel free to open an issue for any questions or clarifications!

---

Thank you for contributing! 🎉
