import os
import mlflow
from mlflow.tracking import MlflowClient


# ---------------------------------------------------------
# 1. MLflow configuration
# ---------------------------------------------------------

mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
)

client = MlflowClient()


# ---------------------------------------------------------
# 2. Find the experiment
# ---------------------------------------------------------

experiment_name = "iris-classification-baseline"

experiment = client.get_experiment_by_name(experiment_name)

if experiment is None:
    raise ValueError(
        f"Experiment '{experiment_name}' not found."
    )


# ---------------------------------------------------------
# 3. Find the best run based on F1 score
# ---------------------------------------------------------

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.f1_macro DESC"],
)

if not runs:
    raise ValueError("No MLflow runs found.")


best_run = runs[0]

best_run_id = best_run.info.run_id
best_f1 = best_run.data.metrics["f1_macro"]

print("Best Run ID:", best_run_id)
print("Best F1 Score:", best_f1)


# ---------------------------------------------------------
# 4. Register the best model
# ---------------------------------------------------------

model_uri = f"runs:/{best_run_id}/model"

registered_model_name = "iris-classifier-prod"

print("\nRegistering model...")
print("Model URI:", model_uri)

result = mlflow.register_model(
    model_uri=model_uri,
    name=registered_model_name,
)

print("\nRegistered Model:")
print("Name:", result.name)
print("Version:", result.version)


# ---------------------------------------------------------
# 5. Move model to Staging
# ---------------------------------------------------------

client.transition_model_version_stage(
    name=registered_model_name,
    version=result.version,
    stage="Staging",
)

print("\nModel successfully moved to Staging.")
print(
    f"Model URI: models:/{registered_model_name}/Staging"
)