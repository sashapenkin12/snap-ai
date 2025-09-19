FROM python:3.13.5-alpine

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create workdir
WORKDIR /app


# Install dependencies
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --frozen --no-install-project

COPY pyproject.toml .
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync

# Copy the project into the image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Run server
CMD ["uv", "run", "uvicorn", "api.app:app", "--workers", "3", "--host", "0.0.0.0", "--port", "8000"]