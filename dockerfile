FROM python:3.12.0-alpine

WORKDIR /app

COPY poetry/poetry.lock poetry/pyproject.toml ./

RUN pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY . .