#!/bin/sh
mkdir /certs
openssl ecparam -genkey -name prime256v1 -noout -out /certs/private_key.pem && \
openssl ec -in ../certs/private_key.pem -pubout -out /certs/public_key.pem