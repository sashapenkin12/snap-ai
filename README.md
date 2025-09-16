# snap-ai
Web-server for calories tracker mobile app. Based on FastAPI and async SQLAlchemy frameworks. 

## Launch 🚀
- 1. Copy test values from .env.example to the .env file.
- 2. Launch Docker Compose commands(Verify, that Docker is installed. Otherwise - download it [here](https://www.docker.com/products/docker-desktop/)):
```bash
docker compose build
docker compose up -d
```

## Usage ⚙️
### Access web-server on url: http://127.0.0.1:8000/
### Health-check🩺: http://127.0.0.1:8000/health/