# Linting and Code Quality Setup

This project uses several tools to maintain code quality and consistency:

## Tools Used

- **Black**: Code formatter for consistent code style
- **isort**: Import statement organizer
- **flake8**: Linter for style guide enforcement
- **pylint**: More comprehensive linting tool
- **mypy**: Static type checker
- **bandit**: Security linter
- **safety**: Checks for known security vulnerabilities in dependencies
- **pre-commit**: Git hooks for automated checking

## Setup

### 1. Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### 2. Install Pre-commit Hooks

```bash
make pre-commit-install
# or
pre-commit install
```

### 3. Generate gRPC Code

```bash
make grpc
# or
./generate_grpc.sh
```

## Usage

### Using Make Commands (Recommended)

```bash
# Set up the complete development environment
make dev-setup

# Run all linting checks
make lint

# Format code automatically
make format

# Check formatting without making changes
make format-check

# Run type checking
make type-check

# Run tests with coverage
make test-cov

# Run security checks
make security

# Run the complete CI pipeline locally
make ci

# Clean up generated files
make clean
```

### Manual Commands

```bash
# Format code
black .
isort .

# Lint code
flake8 src/ tests/
pylint src/

# Type check
mypy src/ --ignore-missing-imports

# Security check
bandit -r src/
safety check

# Run tests
pytest tests/ -v --cov=src --cov-report=html
```

## Configuration

### pyproject.toml
Contains configuration for:
- Black (code formatting)
- isort (import sorting)
- flake8 (linting)
- pylint (linting)
- mypy (type checking)
- pytest (testing)
- coverage (test coverage)

### .pre-commit-config.yaml
Defines the pre-commit hooks that run automatically before each commit.

### GitHub Actions
The `.github/workflows/ci.yml` file defines the CI pipeline that runs on pull requests and pushes to main branches.

## IDE Integration

### VS Code
Install these extensions for automatic linting and formatting:
- Python
- Pylance
- Black Formatter
- isort

Add to your VS Code settings:
```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.mypyEnabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## Exclusions

The following directories/files are excluded from linting:
- `src/grpc_generated/` - Auto-generated gRPC code
- `__pycache__/` - Python cache directories
- `.venv/` - Virtual environment
- `htmlcov/` - Coverage reports
- `logs/` - Log files

## CI/CD Pipeline

The GitHub Actions workflow runs on every pull request and includes:

1. **Lint Job**: Runs flake8, black, isort, mypy, and pylint
2. **Test Job**: Runs pytest with coverage reporting
3. **Security Job**: Runs bandit and safety checks
4. **Code Quality Job**: Integrates with SonarCloud (optional)

The pipeline runs on multiple Python versions (3.8-3.12) to ensure compatibility.

## Troubleshooting

### Common Issues

1. **Import errors during linting**: Make sure gRPC code is generated first
2. **Type checking failures**: Add type stubs or ignore patterns in pyproject.toml
3. **Pre-commit hooks failing**: Run `make format` to auto-fix formatting issues

### Bypassing Checks (Emergency Only)

```bash
# Skip pre-commit hooks
git commit --no-verify

# Skip specific flake8 errors (add to end of line)
# noqa: E501

# Skip pylint warnings (add to end of line)
# pylint: disable=line-too-long
```

## Best Practices

1. Run `make ci` before submitting pull requests
2. Fix linting issues rather than ignoring them
3. Add type hints to new code
4. Write docstrings for public functions and classes
5. Keep functions and classes focused and small
6. Use meaningful variable and function names
