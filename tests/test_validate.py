
import pandas as pd
import pytest

from src.pipeline.validate import validate, DataValidationError


def create_valid_data():
    return pd.DataFrame({
        "sepal length (cm)": [5.1, 6.0],
        "sepal width (cm)": [3.5, 2.8],
        "petal length (cm)": [1.4, 4.5],
        "petal width (cm)": [0.2, 1.5],
        "species": ["setosa", "versicolor"],
        "sepal_area": [17.85, 16.8],
        "petal_area": [0.28, 6.75],
        "sepal_to_petal_length_ratio": [5.1 / 1.4, 6.0 / 4.5],
        "petal_length_bin": ["short", "medium"],
    })


def test_validate_accepts_valid_data(tmp_path):
    input_file = tmp_path / "valid.csv"
    create_valid_data().to_csv(input_file, index=False)

    result = validate(str(input_file))

    assert len(result) == 2
    assert set(result["species"]) == {"setosa", "versicolor"}


def test_validate_rejects_missing_columns(tmp_path):
    input_file = tmp_path / "missing_columns.csv"
    df = create_valid_data().drop(columns=["sepal_area"])
    df.to_csv(input_file, index=False)

    with pytest.raises(DataValidationError, match="Validation failed"):
        validate(str(input_file))


def test_validate_rejects_null_values(tmp_path):
    input_file = tmp_path / "null_values.csv"
    df = create_valid_data()
    df.loc[0, "sepal width (cm)"] = None
    df.to_csv(input_file, index=False)

    with pytest.raises(DataValidationError, match="Validation failed"):
        validate(str(input_file))


def test_validate_rejects_invalid_species(tmp_path):
    input_file = tmp_path / "invalid_species.csv"
    df = create_valid_data()
    df.loc[0, "species"] = "unknown"
    df.to_csv(input_file, index=False)

    with pytest.raises(DataValidationError, match="Validation failed"):
        validate(str(input_file))


def test_validate_rejects_out_of_range_measurements(tmp_path):
    input_file = tmp_path / "out_of_range.csv"
    df = create_valid_data()
    df.loc[0, "sepal length (cm)"] = 20.0
    df.to_csv(input_file, index=False)

    with pytest.raises(DataValidationError, match="Validation failed"):
        validate(str(input_file))
