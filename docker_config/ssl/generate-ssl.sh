#!/bin/sh
rm -rf /etc/nginx/ssl

mkdir -p /etc/nginx/ssl

openssl genrsa -out /etc/nginx/ssl/nginx.key 2048

#(valide 365 jours)
openssl req -new -x509 -key /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -days 365 -subj "/C=FR/ST=France/L=City/O=Portfolio/OU=IT/CN=portfolio-container"

chmod 600 /etc/nginx/ssl/nginx.key
chmod 644 /etc/nginx/ssl/nginx.crt