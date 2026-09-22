from feast import FeatureStore

store = FeatureStore(repo_path=".")

features = store.get_online_features(
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
    entity_rows=[
        {"sample_id": 1}
    ],
).to_dict()

print("Online feature retrieval:")
for key, value in features.items():
    print(f"{key}: {value}")