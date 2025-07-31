.PHONY: install release patch minor major dev-install help clean all-patch

help:
	@echo "Available commands:"
	@echo "  make install      - Install in editable mode (for development)"
	@echo "  make dev-install  - Install with dev dependencies (includes commitizen)"
	@echo "  make release      - Bump patch version and install globally"
	@echo "  make patch        - Bump patch version (0.0.X) and install"
	@echo "  make minor        - Bump minor version (0.X.0) and install"
	@echo "  make major        - Bump major version (X.0.0) and install"
	@echo "  make all-patch    - Bump patch, clean, and build (ready for uv publish)"
	@echo "  make clean        - Clean build artifacts"

install:
	uv tool install --force -e .

dev-install:
	uv pip install -e ".[dev]"

release: patch

patch:
	@echo "Bumping patch version..."
	uv run cz bump --increment PATCH --yes
	uv tool install --force --reinstall .
	@echo "Installation complete!"

minor:
	@echo "Bumping minor version..."
	uv run cz bump --increment MINOR --yes
	uv tool install --force --reinstall .
	@echo "Installation complete!"

major:
	@echo "Bumping major version..."
	uv run cz bump --increment MAJOR --yes
	uv tool install --force --reinstall .
	@echo "Installation complete!"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf dist/*
	@echo "Clean complete!"

all-patch:
	@echo "Bumping patch version..."
	uv run cz bump --increment PATCH --yes
	@echo "Cleaning old builds..."
	rm -rf dist/*
	@echo "Building package..."
	uv build
	@echo "Build complete! Ready for: uv publish --token YOUR_TOKEN"