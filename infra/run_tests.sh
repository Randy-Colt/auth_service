#!/bin/sh

if [ ! -f "/certs/private_key.pem" ]; then
  ./create_keys.sh
fi

poetry run coverage run -m pytest && poetry run coverage report