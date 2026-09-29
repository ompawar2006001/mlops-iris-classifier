import os
import mlflow
import mlflow.sklearn
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)


# ---------------------------------------------------------
# 1. MLflow configuration
# ---------------------------------------------------------

mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
)

mlflow.set_experiment("iris-classification-baseline")


# ---------------------------------------------------------
# 2. Load dataset
# ---------------------------------------------------------

DATA_PATH = "data/processed/iris_features.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)

# Features from Experiment 4
FEATURE_COLUMNS = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
    "sepal_area",
    "petal_area",
    "sepal_to_petal_length_ratio",
]

TARGET_COLUMN = "species"

X = df[FEATURE_COLUMNS].copy()
y = df[TARGET_COLUMN].copy()


# ---------------------------------------------------------
# 3. Handle missing values
# ---------------------------------------------------------

imputer = SimpleImputer(strategy="median")
X = pd.DataFrame(
    imputer.fit_transform(X),
    columns=FEATURE_COLUMNS,
)

# Convert species names into numbers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)


# ---------------------------------------------------------
# 4. Train-test split
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded,
)


# ---------------------------------------------------------
# 5. Define three models
# ---------------------------------------------------------

models = {
    "logistic_regression": LogisticRegression(
        max_iter=200,
        C=1.0,
    ),

    "random_forest_shallow": RandomForestClassifier(
        n_estimators=50,
        max_depth=3,
        random_state=42,
    ),

    "random_forest_deep": RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
    ),
}


# ---------------------------------------------------------
# 6. Train and track each model
# ---------------------------------------------------------

results = []

for model_name, model in models.items():

    with mlflow.start_run(run_name=model_name):

        print("\n" + "=" * 60)
        print("Training:", model_name)
        print("=" * 60)

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(
            y_test,
            y_pred,
            average="macro",
            zero_division=0,
        )
        recall = recall_score(
            y_test,
            y_pred,
            average="macro",
            zero_division=0,
        )
        f1 = f1_score(
            y_test,
            y_pred,
            average="macro",
            zero_division=0,
        )

        # -------------------------------------------------
        # Log parameters
        # -------------------------------------------------

        mlflow.log_param("model_type", model_name)

        if model_name == "logistic_regression":
            mlflow.log_param("max_iter", 200)
            mlflow.log_param("C", 1.0)

        else:
            mlflow.log_param(
                "n_estimators",
                model.n_estimators,
            )
            mlflow.log_param(
                "max_depth",
                model.max_depth,
            )

        # -------------------------------------------------
        # Log metrics
        # -------------------------------------------------

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision_macro", precision)
        mlflow.log_metric("recall_macro", recall)
        mlflow.log_metric("f1_macro", f1)

        # -------------------------------------------------
        # Confusion matrix
        # -------------------------------------------------

        cm = confusion_matrix(y_test, y_pred)

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=label_encoder.classes_,
        )

        disp.plot()

        confusion_matrix_path = (
            f"confusion_matrix_{model_name}.png"
        )

        plt.title(f"Confusion Matrix - {model_name}")
        plt.savefig(confusion_matrix_path)
        plt.close()

        mlflow.log_artifact(confusion_matrix_path)

        # -------------------------------------------------
        # Log model
        # -------------------------------------------------

        mlflow.sklearn.log_model(
            model,
            "model",
        )

        # -------------------------------------------------
        # Store result
        # -------------------------------------------------

        results.append(
            {
                "model": model_name,
                "accuracy": accuracy,
                "precision_macro": precision,
                "recall_macro": recall,
                "f1_macro": f1,
            }
        )

        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")


# ---------------------------------------------------------
# 7. Compare models
# ---------------------------------------------------------

results_df = pd.DataFrame(results)

print("\n")
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

print(results_df.to_string(index=False))

best_model = results_df.loc[
    results_df["f1_macro"].idxmax()
]

print("\nBest model based on F1 score:")
print(best_model["model"])