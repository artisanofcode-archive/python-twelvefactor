FROM python:3.6-alpine

RUN apk --update add --no-cache \
    make \
    musl-dev \
    gcc \
    git \
    && \
    pip install poetry \
    && \
    mkdir /app

WORKDIR /app

COPY ./pyproject.* /app/

RUN poetry install

COPY . /app