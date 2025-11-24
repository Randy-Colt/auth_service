#!bin/bash
if [ ! -f "../certs/private_key.pem" ]; then
  /bin/bash ./create_keys.sh
fi

alembic upgrade head && \
poetry run main.py
