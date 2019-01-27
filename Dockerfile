FROM python:3.6-alpine

RUN apk --update add --no-cache \
    curl \
    make \
    musl-dev \
    gcc \
    git \
    && \
    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && \
    mkdir /app

ENV PATH=/root/.poetry/bin:$PATH

WORKDIR /app

COPY ./pyproject.toml /app/
COPY ./poetry.lock /app/

RUN poetry install -E docs

COPY . /app