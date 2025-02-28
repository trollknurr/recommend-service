FROM python:3.11-slim

ARG WITH_DEV
ARG WITH_CUDA

ENV POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'


RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target="$POETRY_CACHE_DIR" poetry install \
    $(if [ "$WITH_DEV" = '1' ]; then echo '--with dev'; fi) \
    $(if [ "$WITH_CUDA" = '1' ]; then echo '--with cuda'; fi) \
    --no-interaction --no-ansi

ENV PYTHONPATH=/app/src:/app/src/grpc_proto:$PYTHONPATH

COPY . .

CMD ["python", "-m", "entrypoint.grpc_server"]
