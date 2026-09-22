from datetime import timedelta

from feast import (
    Entity,
    FeatureView,
    Field,
    FileSource,
    FeatureService,
)
from feast.types import Float32, String


# Entity
sample = Entity(
    name="sample_id",
    join_keys=["sample_id"],
    value_type=__import__("feast").ValueType.INT64,
    description="Unique identifier for each Iris sample",
)


# Source data
iris_source = FileSource(
    name="iris_features_source",
    path="data/iris_features.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)


# Original Iris measurements
iris_measurements = FeatureView(
    name="iris_measurements",
    entities=[sample],
    ttl=timedelta(days=365),
    schema=[
        Field(name="sepal_length", dtype=Float32),
        Field(name="sepal_width", dtype=Float32),
        Field(name="petal_length", dtype=Float32),
        Field(name="petal_width", dtype=Float32),
        Field(name="species", dtype=String),
    ],
    online=True,
    source=iris_source,
    tags={"team": "mlops"},
)


# Engineered features from Experiment 4
iris_engineered_features = FeatureView(
    name="iris_engineered_features",
    entities=[sample],
    ttl=timedelta(days=365),
    schema=[
        Field(name="sepal_area", dtype=Float32),
        Field(name="petal_area", dtype=Float32),
        Field(name="sepal_to_petal_length_ratio", dtype=Float32),
        Field(name="petal_length_bin", dtype=String),
    ],
    online=True,
    source=iris_source,
    tags={"team": "mlops"},
)


# Feature service
iris_feature_service = FeatureService(
    name="iris_feature_service",
    features=[
        iris_measurements,
        iris_engineered_features,
    ],
)