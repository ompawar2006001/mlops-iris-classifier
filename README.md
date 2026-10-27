
# MLOps Iris Classifier

A sample machine learning project demonstrating MLOps practices, including Git-based version control, data processing, feature engineering, model training, and automated testing.

## Project Objectives

- Build a machine learning classifier using the Iris dataset.
- Practice Git and GitHub version control workflows.
- Implement data collection, preprocessing, feature engineering, and validation.
- Train and evaluate a Random Forest classifier.
- Track experiments and manage models using MLflow.
- Perform hyperparameter tuning.
- Test pipeline components using pytest and measure code coverage.

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/ompawar2006001/mlops-iris-classifier.git
cd mlops-iris-classifier
```

### 2. Create and activate a virtual environment

On macOS:

```bash
python3 -m venv .venv-mlflow
source .venv-mlflow/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the model

```bash
python3 src/train.py
```

## Practical 8: Automated Testing with pytest and Coverage

### Objective

To implement automated tests for the machine learning pipeline, verify the correctness of individual components, and measure test coverage.

### Tools Used

- Python
- pytest
- pytest-cov
- scikit-learn
- pandas

### Test Modules

| Test module | Test cases | Purpose |
|---|---:|---|
| `tests/test_collect.py` | 4 | Tests data collection, species mapping, timestamps, and CSV output. |
| `tests/test_preprocess.py` | 3 | Tests duplicate removal, missing-value handling, and missing species removal. |
| `tests/test_features.py` | 4 | Tests feature calculations, petal-length bins, and output saving. |
| `tests/test_validate.py` | 5 | Tests valid data and rejects missing columns, null values, invalid species, and out-of-range measurements. |
| `tests/test_training.py` | 5 | Tests data loading, model training, custom parameters, evaluation, and predictions. |
| **Total** | **21** | **All test cases passed.** |

### Execute the tests

Run the complete test suite with coverage and an XML test report:

```bash
pytest tests/ -v --cov=src.pipeline --cov=src.train --cov-report=term-missing --junitxml=test-results.xml
```

### Results

- Total tests executed: 21
- Tests passed: 21
- Tests failed: 0
- Overall statement coverage: 78%
- XML report: `test-results.xml`

### Conclusion

Automated testing was successfully implemented for the data collection, preprocessing, feature engineering, validation, and model training components. All 21 tests passed, and the measured statement coverage was 78%. The tests help detect errors early and improve the reliability and maintainability of the machine learning pipeline.

## Run the MLflow User Interface

If your MLflow tracking server is configured to use the local SQLite database, start it with your project's configured tracking database and port. For example:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

Then open `http://127.0.0.1:5000` in your browser.