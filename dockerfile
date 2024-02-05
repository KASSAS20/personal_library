FROM python:3.12-alpine

WORKDIR /app

COPY poetry/poetry.lock poetry/pyproject.toml ./

RUN pip install poetry

RUN poetry install

COPY . .

