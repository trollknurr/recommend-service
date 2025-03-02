# Recommender service example

Service for recommendations, main refs:

* Service gRPC API ref: `proto/recommend-module/recommend_api/v1/recommend_api.proto`
* Python dependencies is managed by `poetry`, ref: `pyproject.toml`
* Build and deploy using Github Actions, ref: `.github/workflows/deploy.yaml`
* Infrastructure provisioning is done by Terraform, ref: `infra/main.tf`

## Project structure

* `src` - Bussiness logic and execution code (entrypoints)
* `test` - Some tests for project
* `weight` - ONNX exported models dir

In `src` dir two main packages:

* `domain` - Business logic of application, that divided on ports, adapters and services
* `entrypoint` - Different entrypoints of the application

`src/entrypoint/config.py` is main config module, it takes values from environment.

### Model storage

Currently, all exported models stored in `weights` directory. Amount of returned reccomendation is added to model name.
When service is starting, it check directory for model that return configured amount of recommendation.

It is not flexible solution, however it is not likely that this configurable value will be changed very often.

As minus of this solution:
* If model grow in size, hard to keep it git
* No metadata for model
* Hard to share model between projects (use same file)

As alternative solution, models can be stored in MLflow registry. Using MLflow registry will solve issues with:

* Model versioning and metadata tracking
* Sharing models between projects (central storage)
* Model size limitations (no need to store in git)


## Set up local environment

Local development is done inside Docker container to ensure consistent development environment across different platforms.

To start development:

* Make `.env.dev` file using provided template `.env.template`
* Run `make rebuild` in project root. That will build and run container with mounted project and dev dependencies
* Run `make shell` to get a shell in container
  
Check out `Makefile` for more useful commands.

Python dependencies managed by `poetry`, ref `pyproject.toml` and to official documentation for usage details.

## Running test client

Ensure optional dependency group `dev` is installed (`poetry install --with dev`)
Call test client entrypoint `python -m entrypoint.test_client`.
It accept `--host` cli argument, by default it is `localhost` for testing in container.


## Building protobuf

Compilation is done by `buf` project:

* Run `make proto-lint` to sanitize proto files
* Run `make local-api-proto-gen`, generated python modules will land in `src/grpc_proto`


## Converting model to ONNX

Ensure optional dependency group `model` is installed (`poetry install --with model`).
To run outside of container `make model-convert`, inside container `python -m entrypoint.model_convert` (because there is no `make` tool)
Torch model will be initialized according to values from `config.py` and then exported to ONNX and save to `weights/` directory.

To ensure model correctness, run tests with install `model` dependecy group

## TODO:

* Build/dependencies for onnxruntime for CUDA / CoreML
* Terraform state in shared env (s3)
* Protobuf add validation
* Add OpenTelemetry metrics (instrumentation for gRPC and manual histogram for inference time)
* Add OpenTelemetry tracing, add support for request id