import pandas as pd
from feast import FeatureStore

store = FeatureStore(repo_path=".")

# Load entity rows from the Parquet source
source_df = pd.read_parquet("data/iris_features.parquet")

# Select 5 samples for historical retrieval
entity_df = source_df[
    ["sample_id", "event_timestamp"]
].head(5)

# Retrieve historical features
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "iris_measurements:sepal_length",
        "iris_measurements:sepal_width",
        "iris_measurements:petal_length",
        "iris_measurements:petal_width",
        "iris_measurements:species",
        "iris_engineered_features:sepal_area",
        "iris_engineered_features:petal_area",
        "iris_engineered_features:sepal_to_petal_length_ratio",
        "iris_engineered_features:petal_length_bin",
    ],
).to_df()

print("Historical feature retrieval:")
print(training_df)
print("\nShape:", training_df.shape)