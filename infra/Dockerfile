FROM python:3.10-slim
 
WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install poetry

RUN poetry install --no-dev --no-root

EXPOSE 8000
