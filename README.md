# Multi-Platform Python Environment Setup

This project provides an automated, cross-platform setup for a Python 3.12 virtual environment compatible with **Apple Silicon (M1/M2/M3/M4) Macs, Intel Macs, Linux, and Windows**. 

It dynamically configures packages and tests based on the running operating system and hardware capabilities (GPU vs. CPU).

It uses the fast Python package manager `uv` to manage the virtual environment and packages.

---

## Supported Environments & Acceleration

1. **Apple Silicon macOS (M-series)**: Accelerated GPU deep learning via Apple Metal Performance Shaders (MPS for PyTorch) and `tensorflow-metal` plug-in (for TensorFlow).
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

A `Makefile` is provided to automate environment provisioning, package installation, and test verification.

### 1. Build the Virtual Environment
To automatically check for/create the virtual environment (using Python 3.12) and install all required libraries, run:
```bash
make
```
This is equivalent to running `make venv` followed by `make install`.

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

To verify you are using the correct Python binary, run `which python` (Unix) or `where python` (Windows).

### 3. Run Verification Tests
To run the automated, platform-agnostic test suite:
```bash
make test
```
The test suite dynamically detects your operating system, architecture, and available GPU hardware (Metal/MPS, NVIDIA CUDA, or CPU fallback), reporting status cleanly.

### 4. Clean Up
To remove the virtual environment:
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

---

## Included Libraries

- **Pandas** & **NumPy**: Data manipulation and numerical operations.
- **Seaborn**: Statistical data visualization.
- **Scikit-Learn**: Classical machine learning algorithms.
- **TensorFlow**: Deep learning framework (leveraging GPU on Apple Silicon and Linux/Windows CUDA systems, CPU otherwise).
- **PyTorch** & **Torchvision**: Deep learning framework (leveraging GPU/MPS on Apple Silicon, CUDA on Linux/Windows, CPU otherwise).
