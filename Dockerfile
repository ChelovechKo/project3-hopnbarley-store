FROM python:3.12-alpine

WORKDIR /code

RUN pip install poetry

COPY . .

RUN poetry install