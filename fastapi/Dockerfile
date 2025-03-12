FROM python:3.12.9-bullseye

WORKDIR /fastapi

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root;

COPY main.py ./
COPY src ./src
COPY tests ./tests
