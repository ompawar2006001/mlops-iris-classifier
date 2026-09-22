# Experiment 5: Feature Store Analysis

## 1. Objective

This experiment demonstrates the creation and use of a local feature store using Feast.

The experiment covers:

- Feature repository creation
- Feature definition and registration
- Offline feature retrieval
- Online feature retrieval
- Feature materialization
- Feature reusability

## 2. Feature Store

A feature store is a centralized system for storing, managing, and serving machine-learning features.

In this experiment, Feast is used as the feature store.

The local setup uses:

- Feast 0.66.0
- SQLite as the online store
- Parquet as the source/offline data
- Python and pandas for data preparation

## 3. Entity

The entity used in this experiment is:

`sample_id`

It uniquely identifies each Iris sample.

## 4. Feature Views

Two Feature Views were created:

### iris_measurements

Contains the original Iris measurements:

- sepal_length
- sepal_width
- petal_length
- petal_width
- species

### iris_engineered_features

Contains engineered features created in Experiment 4:

- sepal_area
- petal_area
- sepal_to_petal_length_ratio
- petal_length_bin

## 5. Feature Service

The Feature Service created in this experiment is:

`iris_feature_service`

It groups the required original and engineered features together for ML applications.

## 6. Online Feature Retrieval

Features were materialized into the SQLite online store.

Online retrieval was successfully tested using:

`sample_id = 1`

The system returned both original and engineered features.

## 7. Historical Feature Retrieval

Historical features were retrieved from the offline source using event timestamps.

Five historical samples were successfully retrieved.

Result:

`5 rows x 11 columns`

This demonstrates historical feature retrieval for training data.

## 8. Feature Reusability

The registered features were reused for another ML workflow.

Three samples were successfully retrieved for the clustering example.

Result:

`3 rows x 8 columns`

This demonstrates that the same registered features can be reused by multiple ML models.

## 9. Benefits of a Feature Store

A feature store provides:

- Centralized feature definitions
- Feature reuse
- Consistent feature computation
- Online feature serving
- Historical feature retrieval
- Reduced duplication of feature engineering
- Better reproducibility
- Reduced risk of training-serving skew

## 10. Experiment Result

The local Feast feature store was successfully created and tested.

The experiment successfully demonstrated:

1. Feature repository creation
2. Feature registration
3. Online feature materialization
4. Online feature retrieval
5. Historical feature retrieval
6. Feature reusability
7. Feature Service creation

## 11. Conclusion

The experiment demonstrates how a feature store can organize and serve machine-learning features for different ML workflows.

Feast provided a reusable feature management layer between the data pipeline and machine-learning models.