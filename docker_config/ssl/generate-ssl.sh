#!/bin/sh
set -e

echo "Generating SSL certificates..."

# Nettoyer
rm -rf /etc/nginx/ssl
mkdir -p /etc/nginx/ssl

# Générer la clé privée
openssl genrsa -out /etc/nginx/ssl/nginx.key 2048

# Créer un fichier de configuration pour le certificat
cat > /tmp/openssl.cnf <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
x509_extensions = v3_req

[dn]
C = FR
ST = France
L = Paris
O = Calculator
OU = IT
CN = calculator-frontend

[v3_req]
subjectAltName = @alt_names
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[alt_names]
DNS.1 = localhost
DNS.2 = calculator-frontend
DNS.3 = *.calculator-frontend
IP.1 = 127.0.0.1
EOF

# Générer le certificat avec la config
openssl req -new -x509 -key /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt \
    -days 365 -config /tmp/openssl.cnf

# Permissions
chmod 600 /etc/nginx/ssl/nginx.key
chmod 644 /etc/nginx/ssl/nginx.crt

# Vérification
echo "Certificate generated successfully:"
openssl x509 -in /etc/nginx/ssl/nginx.crt -noout -subject -dates

# Nettoyage
rm -f /tmp/openssl.cnf

echo "SSL setup complete!"