from feast import FeatureStore

store = FeatureStore(repo_path=".")

features = store.get_online_features(
    features=[
        "iris_measurements:sepal_length",
        "iris_measurements:sepal_width",
        "iris_measurements:petal_length",
        "iris_measurements:petal_width",
        "iris_engineered_features:sepal_area",
        "iris_engineered_features:petal_area",
        "iris_engineered_features:sepal_to_petal_length_ratio",
    ],
    entity_rows=[
        {"sample_id": 1},
        {"sample_id": 2},
        {"sample_id": 3},
    ],
).to_df()

print("Reusable features for clustering:")
print(features)