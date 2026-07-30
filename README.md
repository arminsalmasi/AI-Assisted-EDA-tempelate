# Multi-Platform Python Environment & Data Pipeline Setup

This project provides an automated, cross-platform setup for a Python 3.12 virtual environment and a data feature engineering pipeline compatible with **Apple Silicon (M1/M2/M3/M4) Macs, Intel Macs, Linux, and Windows**.

It manages environment creation, dependency resolution, data preparation/feature engineering, and validation testing via a single `Makefile` interface.

---

## Directory Structure

```text
AI-Assisted-EDA-tempelate/
├── data/
│   ├── raw/                 # Raw customers, orders, and deliveries CSV files (Source)
│   └── interim/             # Cleaned and feature-engineered CSV files (Outputs)
├── notebooks/               # Jupyter exploratory and prototyping notebooks
├── report/                  # slide decks, data dictionaries, figures, final reports
│   └── figures/             # Exported visualizations and plots
├── src/                     # Core Python modules and scripts
│   └── prepare_data.py      # Feature engineering and dataset merging pipeline
├── tests/                   # Integration and data validation tests
│   ├── test_libraries.py    # Environment library imports and GPU check tests
│   └── test_prepared_data.py# Interim data schema and integrity validation tests
├── Makefile                 # Automation Makefile
├── requirements.txt         # Pinned pip requirements with PEP 508 markers
└── README.md                # This documentation
```

---

## Supported Environments & Acceleration

1. **Apple Silicon macOS (M-series)**: Accelerated GPU training via Apple Metal Performance Shaders (MPS for PyTorch) and `tensorflow-metal` plug-in (for TensorFlow).
2. **Intel macOS**: CPU-only execution (fallback).
3. **Linux / Windows (NVIDIA GPU)**: Accelerated GPU training using NVIDIA CUDA (supported out-of-the-box by standard PyPI wheels for TensorFlow and PyTorch).
4. **Linux / Windows (No GPU)**: CPU-only execution (fallback).

---

## Prerequisites

### Unix-like Systems (macOS, Linux, WSL)
1. **Xcode Command Line Tools** (on macOS):
   ```bash
   xcode-select --install
   ```
2. **GNU Make** and standard compiler tools.

### Windows (Native Command Prompt/PowerShell)
1. **make**: A make utility installed (e.g. through Chocolatey, MSYS2, or Git Bash).
2. **Python 3.12** on PATH.

---

## Getting Started

The `Makefile` automates all phases of the project setup.

### 1. Build and Run the Complete Pipeline
To create the virtual environment, install requirements, run feature engineering, and execute tests:
```bash
make
```
This is equivalent to running `make venv`, `make install`, `make prepare`, and `make test`.

### 2. Activate the Environment
* **macOS / Linux / WSL**:
  ```bash
  source .venv/bin/activate
  ```
* **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **Windows (Command Prompt)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```

### 3. Run Data Preparation (Feature Engineering)
To run the data cleaning, merging, and feature engineering script (`src/prepare_data.py`) separately:
```bash
make prepare
```
This processes the raw data in `data/raw/` and outputs files in `data/interim/`:
* `data/interim/master_orders.csv`: An order-level transaction dataset containing joined customer and delivery details, along with binary indicators for delays and inaccuracies.
* `data/interim/customer_features.csv`: A customer-level aggregated dataset summarizing customer behavioral patterns (RFM), active lifetimes, promotion sensitivity, churn flags, and early experience delay/inaccuracy statistics.

### 4. Run Verification Tests
To run the full verification test suite (verifying imports, GPU availability, and intermediate data schema integrity):
```bash
make test
```

### 5. Clean Up
To remove the virtual environment and all generated intermediate data:
```bash
make clean
```

---

## VS Code Integration

To configure VS Code to run notebooks or scripts with the new environment:
1. Open the Command Palette (`Cmd+Shift+P` on Mac, `Ctrl+Shift+P` on Windows/Linux).
2. Type and select **Python: Select Interpreter**.
3. Choose the interpreter located inside the virtual environment:
   - macOS/Linux: `./.venv/bin/python`
   - Windows: `./.venv/Scripts/python.exe`
