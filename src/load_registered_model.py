import os
import mlflow
import mlflow.sklearn


# ---------------------------------------------------------
# 1. MLflow configuration
# ---------------------------------------------------------

mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
)


# ---------------------------------------------------------
# 2. Registered model URI
# ---------------------------------------------------------

model_uri = "models:/iris-classifier-prod/Staging"

print("Loading registered model...")
print("Model URI:", model_uri)


# ---------------------------------------------------------
# 3. Load the model from MLflow Model Registry
# ---------------------------------------------------------

model = mlflow.sklearn.load_model(model_uri)


# ---------------------------------------------------------
# 4. Display loaded model
# ---------------------------------------------------------

print("\nRegistered model loaded successfully!")
print("Model:")
print(model)
