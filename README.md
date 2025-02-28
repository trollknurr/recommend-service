# Recommender service example

Service for recommendations, main refs:

* Service gRPC API ref: `proto/recommend-module/recommend_api/v1/recommend_api.proto`
* Python dependencies is managed by `poetry`, ref: `pyproject.toml`
* Build and deploy using Github Actions, ref: `.github/workflows/deploy.yaml`
* Infrastructure provisioning is done by Terraform, ref: `infra/main.tf`

## Project structure

* `src` - Bussiness logic and execution code (entrypoints)
* `test` - Some tests for project

In `src` dir two main packages:

* `domain` - Business logic of application, that divided on ports, adapters and services
* `entrypoint` - Different entrypoints of the application

`src/entrypoint/config.py` is main config module.


## Set up local environment

Local development is done inside Docker container to ensure consistent development environment across different platforms.

To start development:

* Make `.env.dev` file using provided template `.env.template`
* Run `make rebuild` in project root. That will build and run container with mounted project and dev dependencies
* Run `make shell` to get a shell in container
  
Check out `Makefile` for more useful commands.


## Building protobuf

Compilation is done by `buf` project:

* Run `make proto-lint` to sanitize proto files
* Run `make local-api-proto-gen`, generated python modules will land in `src/grpc_proto`


## Converting model to ONNX

Ensure optional dependency group `model` is installed (`poetry install --with model`).
To run outside of container `make model-convert`, inside container `python -m entrypoint.model_convert` (because there is no `make` tool)
Torch model will be initialized according to values from `config.py` and then exported to ONNX and save to `weights/` directory.

## TODO:

* Build/dependencies for onnxruntime for CUDA / CoreML