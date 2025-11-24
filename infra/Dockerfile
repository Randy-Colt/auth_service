FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install poetry

COPY src/pyproject.toml src/poetry.lock ./

RUN poetry install --no-root


# тесты
FROM builder AS test

WORKDIR /src

COPY src/ .
COPY src/pyproject.toml src/poetry.lock ./

RUN poetry install --no-root --with dev

COPY infra/create_keys.sh .
COPY infra/run_tests.sh .

RUN chmod +x run_tests.sh

ENTRYPOINT ["./run_tests.sh"]


# старт приложения
FROM python:3.13-slim AS production

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install poetry

COPY src/pyproject.toml src/poetry.lock ./

RUN poetry install --no-root --without dev

COPY src .

COPY infra/entrypoint.sh .
COPY infra/create_keys.sh .

RUN chmod +x entrypoint.sh create_keys.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
