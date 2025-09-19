#!/bin/bash
set -e

cd ~/app

echo "Create .env from Github Secrets"
cat > .env << EOL
DB_USER=${{ secrets.DB_USER }}
DB_PASSWORD=${{ secrets.DB_PASSWORD }}
DB_HOST=${{ secrets.DB_HOST }}
DB_NAME=${{ secrets.DB_NAME }}
SECRET_KEY=${{ secrets.SECRET_KEY}}
ALGORITHM=${{ secrets.ALGORITHM }}
EOL

docker-compose down
docker compose up -d --build