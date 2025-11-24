#!/bin/sh

if [ ! -f "/certs/private_key.pem" ]; then
  ./create_keys.sh
fi

poetry run alembic upgrade head && \
poetry run python main.py
