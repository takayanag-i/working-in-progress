FROM python:3.12.9-bullseye

WORKDIR /docs

COPY docs/pyproject.toml docs/poetry.lock ./
RUN pip install poetry
RUN poetry install --no-root

COPY docs/mkdocs.yml ./
COPY docs/docs ./docs
COPY fastapi/src ./src

CMD ["poetry", "run", "mkdocs", "serve", "--dev-addr=0.0.0.0:8001"]
