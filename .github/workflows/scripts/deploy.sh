#!/bin/bash
set -e

cd ~/app

echo "Create .env from Github Secrets"
cat > .env << EOL
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=${DB_HOST}
DB_NAME=${DB_NAME}
SECRET_KEY=${SECRET_KEY}
ALGORITHM=${ALGORITHM}
EOL

docker-compose down
docker compose up -d --build