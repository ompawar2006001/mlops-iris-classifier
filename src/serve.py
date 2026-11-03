"""HTTP server for the containerized Iris classifier."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import joblib
import numpy as np

MODEL_PATH = "models/final_model.joblib"
ENCODER_PATH = "models/label_encoder.joblib"

FEATURE_ORDER = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
    "sepal_area",
    "petal_area",
    "sepal_to_petal_length_ratio",
]

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)


class PredictionHandler(BaseHTTPRequestHandler):

    def _respond(self, status, payload):
        response = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        if self.path == "/health":
            self._respond(200, {"status": "healthy"})
        else:
            self._respond(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/predict":
            self._respond(404, {"error": "not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length))

            missing = [key for key in FEATURE_ORDER if key not in body]

            if missing:
                self._respond(
                    400,
                    {"error": "Missing features", "missing": missing},
                )
                return

            features = np.array(
                [[float(body[key]) for key in FEATURE_ORDER]]
            )

            prediction = model.predict(features)
            probabilities = model.predict_proba(features)[0]

            species = label_encoder.inverse_transform(prediction)[0]

            self._respond(
                200,
                {
                    "prediction": species,
                    "probabilities": probabilities.tolist(),
                },
            )

        except (ValueError, TypeError, json.JSONDecodeError):
            self._respond(400, {"error": "Invalid request"})


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), PredictionHandler)
    print("Iris server listening on port 8000")
    server.serve_forever()