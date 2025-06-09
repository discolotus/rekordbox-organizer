# Rekordbox Music Organizer - Makefile
# 
# This Makefile provides convenient commands for installing, developing,
# and managing the Rekordbox Music Organizer package.

.PHONY: help install-cli install-dev uninstall test clean lint format check-pipx

# Default target
help:
	@echo "Rekordbox Music Organizer - Available Commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install-cli     Install globally using pipx (recommended)"
	@echo "  install-dev     Install in development mode with pip"
	@echo "  uninstall       Uninstall the package"
	@echo ""
	@echo "Development:"
	@echo "  test           Run tests with sample files"
	@echo "  lint           Run code linting"
	@echo "  format         Format code with black"
	@echo "  clean          Clean build artifacts"
	@echo ""
	@echo "Requirements:"
	@echo "  check-pipx     Check if pipx is installed"
	@echo ""
	@echo "Usage after installation:"
	@echo "  rekordbox-organizer --help"
	@echo "  music-scanner --help"
	@echo "  test-rekordbox"

# Check if pipx is installed
check-pipx:
	@which pipx > /dev/null || (echo "❌ pipx not found. Install with: python -m pip install --user pipx" && exit 1)
	@echo "✅ pipx is available"

# Install globally using pipx (recommended)
install-cli: check-pipx
	@echo "🚀 Installing Rekordbox Organizer globally with pipx..."
	pipx install .
	@echo ""
	@echo "✅ Installation complete!"
	@echo ""
	@echo "📋 Available commands:"
	@echo "  rekordbox-organizer  - Main organizer tool"
	@echo "  music-scanner        - Music file analysis tool"
	@echo "  test-rekordbox       - Test Rekordbox connection"
	@echo ""
	@echo "🎵 Quick start:"
	@echo "  rekordbox-organizer --help"
	@echo "  test-rekordbox"

# Install in development mode
install-dev:
	@echo "🔧 Installing in development mode..."
	pip install -e .
	@echo "✅ Development installation complete!"

# Uninstall the package
uninstall:
	@echo "🗑️  Uninstalling Rekordbox Organizer..."
	@if which pipx > /dev/null && pipx list | grep -q rekordbox-organizer; then \
		pipx uninstall rekordbox-organizer; \
	else \
		pip uninstall rekordbox-organizer -y; \
	fi
	@echo "✅ Uninstallation complete!"

# Run basic tests
test:
	@echo "🧪 Running basic functionality tests..."
	@echo "Testing help commands..."
	python rekordbox_organizer.py --help > /dev/null && echo "✅ rekordbox_organizer.py help works"
	python music_file_scanner.py --help > /dev/null && echo "✅ music_file_scanner.py help works"
	python test_rekordbox_connection.py > /dev/null && echo "✅ test_rekordbox_connection.py works"
	@echo "🎉 Basic tests passed!"

# Lint code
lint:
	@echo "🔍 Running code linting..."
	@if which flake8 > /dev/null; then \
		flake8 *.py --max-line-length=120 --ignore=E501,W503; \
	else \
		echo "⚠️  flake8 not found. Install with: pip install flake8"; \
	fi

# Format code
format:
	@echo "🎨 Formatting code..."
	@if which black > /dev/null; then \
		black *.py --line-length=120; \
	else \
		echo "⚠️  black not found. Install with: pip install black"; \
	fi

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	@echo "✅ Cleanup complete!"

# Build package
build: clean
	@echo "📦 Building package..."
	python setup.py sdist bdist_wheel
	@echo "✅ Package built successfully!"

# Install from PyPI (when published)
install-pypi: check-pipx
	@echo "📥 Installing from PyPI..."
	pipx install rekordbox-organizer
	@echo "✅ Installed from PyPI!"

# Development setup
dev-setup:
	@echo "🛠️  Setting up development environment..."
	pip install -e .
	pip install black flake8 pytest
	@echo "✅ Development environment ready!"

# Show installation status
status:
	@echo "📊 Installation Status:"
	@echo ""
	@if which rekordbox-organizer > /dev/null; then \
		echo "✅ rekordbox-organizer command available"; \
		rekordbox-organizer --help | head -1; \
	else \
		echo "❌ rekordbox-organizer command not found"; \
	fi
	@if which music-scanner > /dev/null; then \
		echo "✅ music-scanner command available"; \
	else \
		echo "❌ music-scanner command not found"; \
	fi
	@if which test-rekordbox > /dev/null; then \
		echo "✅ test-rekordbox command available"; \
	else \
		echo "❌ test-rekordbox command not found"; \
	fi
	@echo ""
	@if which pipx > /dev/null; then \
		echo "📦 pipx packages:"; \
		pipx list | grep rekordbox || echo "  (no rekordbox packages found)"; \
	fi
