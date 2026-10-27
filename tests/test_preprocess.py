
import pandas as pd
from src.pipeline.preprocess import preprocess


def create_sample_csv(path):
    """Create sample data for testing preprocessing."""
    df = pd.DataFrame({
        "sepal length (cm)": [5.1, 5.1, None, 6.0],
        "sepal width (cm)": [3.5, 3.5, 3.0, 2.8],
        "petal length (cm)": [1.4, 1.4, 1.5, 4.5],
        "petal width (cm)": [0.2, 0.2, 0.3, 1.5],
        "species": ["setosa", "setosa", "setosa", None],
        "collected_at": ["2026-01-01", "2026-01-01",
                         "2026-01-02", "2026-01-03"],
    })
    df.to_csv(path, index=False)


def test_preprocess_removes_duplicates_and_timestamp(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    create_sample_csv(input_file)

    result = preprocess(str(input_file), str(output_file))

    assert len(result) == 2
    assert "collected_at" not in result.columns
    assert output_file.exists()


def test_preprocess_fills_missing_numeric_values(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    create_sample_csv(input_file)

    result = preprocess(str(input_file), str(output_file))

    assert result["sepal length (cm)"].isna().sum() == 0
    assert pd.api.types.is_numeric_dtype(
        result["sepal length (cm)"]
    )


def test_preprocess_removes_missing_species(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    create_sample_csv(input_file)

    result = preprocess(str(input_file), str(output_file))

    assert result["species"].isna().sum() == 0
    assert set(result["species"]) == {"setosa"}
