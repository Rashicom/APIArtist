FROM python:3.11-alpine3.20

WORKDIR /code
ENV PYTHONPATH=/code/src

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev postgresql-dev
RUN apk update && apk add bash

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry

COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction

COPY . /code/

CMD [ "/bin/bash", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000" ]
