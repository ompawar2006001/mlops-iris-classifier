
import pandas as pd

from src.pipeline.collect import collect_data


def test_collect_data_returns_150_rows(tmp_path):
    output_file = tmp_path / "iris_raw.csv"

    result = collect_data(str(output_file))

    assert len(result) == 150
    assert isinstance(result, pd.DataFrame)


def test_collect_data_maps_species_names(tmp_path):
    output_file = tmp_path / "iris_raw.csv"

    result = collect_data(str(output_file))

    assert set(result["species"]) == {
        "setosa",
        "versicolor",
        "virginica",
    }


def test_collect_data_adds_timestamp(tmp_path):
    output_file = tmp_path / "iris_raw.csv"

    result = collect_data(str(output_file))

    assert "collected_at" in result.columns
    assert result["collected_at"].notna().all()


def test_collect_data_saves_csv(tmp_path):
    output_file = tmp_path / "iris_raw.csv"

    collect_data(str(output_file))

    assert output_file.exists()

    saved_data = pd.read_csv(output_file)

    assert len(saved_data) == 150
    assert "species" in saved_data.columns
    assert "collected_at" in saved_data.columns
