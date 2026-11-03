# Docker Deployment Documentation

## 1. Overview

This document describes the containerization and deployment of the Iris
Machine Learning classification application using Docker.

The application provides an HTTP API for health checks and Iris species
predictions.

## 2. Multi-Stage Docker Build

The Dockerfile uses two stages:

### Builder Stage

- Uses Python 3.11-slim.
- Installs dependencies from requirements-serving.txt.
- Copies the processed Iris dataset.
- Executes src/train_final_model.py.
- Generates the trained model and label encoder.

### Runtime Stage

- Uses Python 3.11-slim.
- Copies the installed dependencies from the builder stage.
- Copies the trained model and label encoder.
- Copies src/serve.py.
- Exposes port 8000.

### Advantages

Multi-stage builds keep training-related files and the dataset out of the
final runtime image. This reduces unnecessary files and separates model
training from model serving.

A naive single-stage build would retain the training script and dataset
alongside runtime components. Its image size was not separately measured
in this experiment.

## 3. Docker Image Details

| Property | Value |
|---|---|
| Image name | iris-classifier |
| Tag | v1 |
| Base image | python:3.11-slim |
| Architecture | ARM64 (Apple Silicon) |
| Docker content size | 152 MB |
| Docker disk usage | 709 MB |

The content size and disk usage are separate measurements reported by
Docker.

## 4. Health Check Configuration

The Dockerfile includes the following health check:

    HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
        CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

Configuration:

- Interval: 30 seconds
- Timeout: 5 seconds
- Start period: 10 seconds
- Retries: 3

The health endpoint returns:

    {"status": "healthy"}

The container health status was verified as healthy.

## 5. Build and Run Commands

Build the Docker image:

    docker build -t iris-classifier:v1 .

Run the container:

    docker run -d --name iris-classifier-container -p 8000:8000 iris-classifier:v1

Check running containers:

    docker ps

Test the health endpoint:

    curl http://localhost:8000/health

Test the prediction endpoint:

    curl -X POST http://localhost:8000/predict \
      -H "Content-Type: application/json" \
      -d '{"sepal length (cm)": 5.1, "sepal width (cm)": 3.5, "petal length (cm)": 1.4, "petal width (cm)": 0.2, "sepal_area": 17.85, "petal_area": 0.28, "sepal_to_petal_length_ratio": 3.642857}'

Inspect container health:

    docker inspect --format='{{.State.Health.Status}}' iris-classifier-container

Inspect image size:

    docker images iris-classifier

Inspect image history:

    docker history iris-classifier:v1

View application logs:

    docker logs iris-classifier-container

Stop and remove the container:

    docker stop iris-classifier-container
    docker rm iris-classifier-container

## 6. Testing Results

| Test | Result |
|---|---|
| Docker image build | Passed |
| Container startup | Passed |
| Health endpoint | Passed |
| Valid prediction | Passed |
| Invalid input validation | Passed |
| Container health check | Healthy |
| Image inspection | Completed |
| Container cleanup | Completed |

The application successfully predicted the Iris species as setosa for
the supplied sample input.
