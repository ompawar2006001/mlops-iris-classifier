
import numpy as np

from sklearn.ensemble import RandomForestClassifier

from src.train import load_data, train_model, evaluate_model


def test_load_data_returns_correct_shapes():
    X_train, X_test, y_train, y_test = load_data()

    assert X_train.shape == (120, 4)
    assert X_test.shape == (30, 4)
    assert len(y_train) == 120
    assert len(y_test) == 30


def test_train_model_returns_fitted_classifier():
    X_train, X_test, y_train, y_test = load_data()

    model = train_model(X_train, y_train)

    assert isinstance(model, RandomForestClassifier)
    assert hasattr(model, "classes_")
    assert len(model.classes_) == 3


def test_train_model_accepts_custom_parameters():
    X_train, X_test, y_train, y_test = load_data()

    model = train_model(
        X_train,
        y_train,
        n_estimators=50,
        max_depth=3
    )

    assert model.n_estimators == 50
    assert model.max_depth == 3
    assert hasattr(model, "classes_")


def test_evaluate_model_returns_accuracy_and_report():
    X_train, X_test, y_train, y_test = load_data()

    model = train_model(X_train, y_train)
    accuracy, report = evaluate_model(model, X_test, y_test)

    assert isinstance(accuracy, float)
    assert 0.0 <= accuracy <= 1.0
    assert isinstance(report, str)
    assert "precision" in report
    assert "recall" in report


def test_model_predictions_have_valid_classes():
    X_train, X_test, y_train, y_test = load_data()

    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)

    assert len(predictions) == len(y_test)
    assert set(np.unique(predictions)).issubset({0, 1, 2})

def test_prediction_probabilities_are_between_zero_and_one():
    X_train, X_test, y_train, y_test = load_data()

    model = train_model(X_train, y_train)
    probabilities = model.predict_proba(X_test)

    assert np.all(probabilities >= 0.0)
    assert np.all(probabilities <= 1.0)


def test_prediction_probabilities_sum_to_one():
    X_train, X_test, y_train, y_test = load_data()

    model = train_model(X_train, y_train)
    probabilities = model.predict_proba(X_test)

    assert np.allclose(probabilities.sum(axis=1), 1.0)


def test_model_meets_minimum_accuracy_threshold():
    X_train, X_test, y_train, y_test = load_data()

    model = train_model(X_train, y_train)
    accuracy, report = evaluate_model(model, X_test, y_test)

    assert accuracy >= 0.90, (
        f"Model accuracy {accuracy:.2%} is below the required 90% threshold"
    )
