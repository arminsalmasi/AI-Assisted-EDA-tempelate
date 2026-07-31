# UrbanCart Retention Analysis: Gap Analysis Report

This document compares the data logic, scripts, notebooks, and outputs of the current project (`AI-Assisted-EDA-tempelate`) with the previous project completed by Codex (`Exploratory Data Analysis`).

---

## 1. Feature Engineering & Preprocessing Gaps
* **Status**: **Fully Resolved**.
* **Analysis**: The previous preprocessing script (`prepare_analysis_dataset.py`) computed several advanced columns essential for survival analysis, customer cohorts, and demographic retention splits.
* **Actions Taken**:
  - We updated our `src/prepare_data.py` to match the exact calculations in Codex's pipeline, including category-specific order counts (`restaurant_orders`, `grocery_orders`, etc.), delivery metrics (`on_time_delivery_rate`, `correct_order_rate`), active shopping spans, repeat customer flags, and first-order lookback retention indicators with censoring logic (`returned_after_first_order_30d` etc. mapped to NaN when observation windows are incomplete).
  - All automated validation tests in `tests/test_prepared_data.py` were updated and pass, verifying the extended 58-column customer schema and 37-column order schema.

---

## 2. Notebook Gaps
* **Status**: **Univariate Resolved; Bivariate & Multivariate Pending**.
* **Analysis**: The comparison project contains three dedicated analysis notebooks, whereas our project currently only contains the univariate analysis notebook.
* **Actions Taken & Remaining**:
  - **Univariate Notebook**: Successfully generated and executed in `notebooks/01_univariate_analysis.ipynb`. We also re-added `src/generate_univarient_notebook.py` to recreate it programmatically.
  - **Bivariate Notebook (Gap)**: Codex has `02_bivariate_analysis.ipynb` (created via `create_bivariate_notebook.py`). This notebook explores relationships between retention outcomes and delivery experiences, promo usage, and spend.
  - **Multivariate Notebook (Gap)**: Codex has `03_multivariate_analysis.ipynb` (created via `create_multivariate_notebook.py`). This notebook examines joint variables (e.g. satisfaction vs. delay vs. retention).

---

## 3. Statistical Hypothesis Testing Gaps
* **Status**: **Pending**.
* **Analysis**: Codex has `src/run_hypothesis_tests.py` which estimates binary logistic regressions, Mann-Whitney U tests, and Chi-Square tests of independence from scratch (without standard scientific libraries) and outputs findings to `reports/hypothesis_testing_results.txt`.
* **Proposed Integration**: We will build `src/run_hypothesis_tests.py` using standard scientific libraries (`scipy.stats` and `statsmodels`) which are far more robust and provide exact confidence intervals and diagnostic tests.

---

## 4. Reporting Gaps
* **Status**: **Pending**.
* **Analysis**: Codex contains a script `src/generate_html_report.py` that compiles findings into a clean, standalone HTML report `reports/urban_cart_retention_report.html` embedding the SVG charts.
* **Proposed Integration**: We will implement `src/generate_html_report.py` to build a modern HTML dashboard summarizing our descriptive statistics, survival analysis curves, and hypothesis test results.

---

## Summary Directory Mapping

| File/Folder in Codex | Purpose | Status in Our Project | Action Required |
| :--- | :--- | :--- | :--- |
| `prepare_analysis_dataset.py` | Data Engineering | **Aligned** | Integrated into `src/prepare_data.py` |
| `create_univariate_notebook.py` | Univariate generation | **Aligned** | Created `src/generate_univarient_notebook.py` |
| `create_bivariate_notebook.py` | Bivariate generation | **Gap** | Create `src/generate_bivarient_notebook.py` |
| `create_multivariate_notebook.py` | Multivariate generation | **Gap** | Create `src/generate_multivarient_notebook.py` |
| `run_hypothesis_tests.py` | Statistical tests | **Gap** | Create `src/run_hypothesis_tests.py` |
| `generate_html_report.py` | HTML Report Compiler | **Gap** | Create `src/generate_html_report.py` |
