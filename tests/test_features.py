
import pandas as pd
from src.pipeline.features import engineer_features


def create_sample_csv(path):
    df = pd.DataFrame({
        "sepal length (cm)": [5.0, 6.0, 7.0],
        "sepal width (cm)": [2.0, 3.0, 3.5],
        "petal length (cm)": [1.0, 3.0, 5.0],
        "petal width (cm)": [0.2, 1.0, 2.0],
        "species": ["setosa", "versicolor", "virginica"],
    })
    df.to_csv(path, index=False)


def test_engineer_features_calculates_areas(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    create_sample_csv(input_file)

    result = engineer_features(str(input_file), str(output_file))

    assert result.loc[0, "sepal_area"] == 10.0
    assert result.loc[0, "petal_area"] == 0.2
    assert result.loc[1, "sepal_area"] == 18.0
    assert result.loc[1, "petal_area"] == 3.0


def test_engineer_features_calculates_length_ratio(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    create_sample_csv(input_file)

    result = engineer_features(str(input_file), str(output_file))

    assert result.loc[0, "sepal_to_petal_length_ratio"] == 5.0
    assert result.loc[1, "sepal_to_petal_length_ratio"] == 2.0


def test_engineer_features_creates_petal_length_bins(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    create_sample_csv(input_file)

    result = engineer_features(str(input_file), str(output_file))

    assert result["petal_length_bin"].astype(str).tolist() == [
        "short", "medium", "long"
    ]


def test_engineer_features_saves_output(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    create_sample_csv(input_file)

    engineer_features(str(input_file), str(output_file))

    assert output_file.exists()

    saved_data = pd.read_csv(output_file)
    assert len(saved_data) == 3
    assert "sepal_area" in saved_data.columns
    assert "petal_area" in saved_data.columns
