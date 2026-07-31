PYTHON_VERSION = 3.12
VENV = .venv
UV := $(shell command -v uv 2> /dev/null || echo "/Users/armin/.local/bin/uv")

# Detect Operating System
ifeq ($(OS),Windows_NT)
    VENV_PYTHON = $(VENV)/Scripts/python.exe
    RM = rmdir /s /q
else
    VENV_PYTHON = $(VENV)/bin/python
    RM = rm -rf
endif

.PHONY: all venv install prepare test clean

all: venv install prepare test

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment with Python $(PYTHON_VERSION) using uv..."; \
		$(UV) venv $(VENV) --python $(PYTHON_VERSION); \
	else \
		if [ -f "$(VENV_PYTHON)" ]; then \
			CURRENT_VER=$$($(VENV_PYTHON) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null); \
			if [ "$$CURRENT_VER" != "$(PYTHON_VERSION)" ]; then \
				echo "Wrong Python version ($$CURRENT_VER). Re-creating virtual environment with Python $(PYTHON_VERSION)..."; \
				$(RM) $(VENV); \
				$(UV) venv $(VENV) --python $(PYTHON_VERSION); \
			else \
				echo "Virtual environment already exists with correct Python version ($$CURRENT_VER)."; \
			fi; \
		else \
			echo "Virtual environment directory exists but Python binary is missing. Re-creating..."; \
			$(RM) $(VENV); \
			$(UV) venv $(VENV) --python $(PYTHON_VERSION); \
		fi; \
	fi

install: venv requirements.txt
	@echo "Installing requirements using uv..."
	$(UV) pip install -r requirements.txt

prepare: install
	@echo "Running data preparation and feature engineering..."
	$(VENV_PYTHON) src/prepare_data.py

test: install prepare
	@echo "Running tests..."
	$(VENV_PYTHON) -m unittest discover -s tests -p "test_*.py"

clean:
	$(RM) $(VENV)
	$(RM) data/processed
