
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

### Practical 8: Automated Testing with pytest and Coverage

**Objective:** Test data collection, preprocessing, feature engineering, data validation, model training, and model output quality using automated tests.

#### Test Modules

| Test File | Tests | Purpose |
|---|---:|---|
| `tests/test_collect.py` | 4 | Data collection, species mapping, timestamps, and CSV output |
| `tests/test_features.py` | 4 | Feature calculations, ratios, bins, and saving output |
| `tests/test_preprocess.py` | 3 | Duplicate removal, missing-value handling, and timestamp removal |
| `tests/test_training.py` | 8 | Data loading, model training, configuration, evaluation, predictions, probability checks, and model accuracy |
| `tests/test_validate.py` | 5 | Required columns, null values, valid species, and measurement ranges |
| **Total** | **24** | **All automated tests passed** |

#### Run the Tests

Run the complete test suite with coverage reporting and XML output:

```bash
pytest tests/ -v --cov=src.pipeline --cov=src.train --cov-report=term-missing --junitxml=test-results.xml
```

#### Latest Test Results

- **Tests passed:** 24/24
- **Tests failed:** 0
- **Execution time:** 2.17 seconds
- **Overall code coverage:** 78%
- **Test report:** `test-results.xml`

The test suite verifies data-processing functions, training behavior, prediction validity, probability outputs, and a minimum model accuracy of 90%.

The generated `test-results.xml` file contains the test execution results in JUnit XML format.