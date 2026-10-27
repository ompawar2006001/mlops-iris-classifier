# Continuous Integration (CI) Pipeline

## 1. Overview

This project uses GitHub Actions to automatically validate code quality, run tests, and verify model accuracy whenever changes are pushed or a pull request is opened against the `main` or `develop` branch.

## 2. CI Pipeline Jobs

The workflow is defined in `.github/workflows/ci.yml`.

### Job 1: Build and Lint

**Job name:** `build-and-lint`

- Sets up the Python environment.
- Installs the required dependencies.
- Checks source code quality using linting tools.
- Helps identify code quality issues before testing.

### Job 2: Test Suite

**Job name:** `test-suite`

- Runs the project's automated tests.
- Depends on the successful completion of `build-and-lint`.
- Prevents later jobs from running when the test suite fails.

### Job 3: Model Quality Gate

**Job name:** `model-quality-gate`

- Evaluates the Iris classification model's accuracy.
- Checks whether model accuracy meets the minimum acceptable threshold of `0.90` (90%).
- Depends on the successful completion of `test-suite`.

## 3. Job Dependency Order

The jobs execute in the following order:

1. `build-and-lint`
2. `test-suite`
3. `model-quality-gate`

If an upstream job fails, dependent jobs are skipped.

## 4. Branch Protection

The GitHub ruleset named **Protect main - CI checks** protects the `main` branch.

The ruleset requires pull requests before merging and requires these status checks to pass:

- `build-and-lint`
- `test-suite`
- `model-quality-gate`

These requirements help prevent changes from being merged when the required CI checks have not passed.

## 5. Regression Simulation

A temporary branch named `feature/simulate-regression` was used to demonstrate the model quality gate.

The minimum acceptable accuracy threshold was temporarily increased from `0.90` to `1.001`. Because the model achieved an accuracy of `1.0000`, the test failed as expected.

The regression pull request was closed without merging, and the temporary branch was deleted locally and remotely.

The normal threshold of `0.90` was verified on the `main` branch.

## 6. Conclusion

The GitHub Actions pipeline automates code quality checks, testing, and model accuracy validation. Combined with branch protection, it provides a consistent process for validating changes before they are merged into `main`.