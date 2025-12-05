# Lightweight, fast Python 3.11 image with uv preinstalled
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Install runtime OS deps (kept minimal)
# - ca-certificates: HTTPS
# - libev4: runtime lib sometimes used by cassandra-driver speedups
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       libev4 \
    && rm -rf /var/lib/apt/lists/*

# Avoid creating .pyc files and ensure stdout/stderr are unbuffered
# todo - PYTHONPATH may be problematic, establish a unified execution home path
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR /app

# Activate the venv for subsequent commands and at runtime
ENV VIRTUAL_ENV=/app/.venv
ENV PATH=/app/.venv/bin:$PATH

# Create unprivileged user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser


# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies into a local virtual environment using uv (cacheable layer)
# This reads dependencies directly from pyproject.toml
# Prefer lockfile for deterministic installs; fall back to resolving from pyproject if missing
RUN if [ -f uv.lock ]; then uv sync --frozen; else uv sync; fi

# Copy the entire project, relying on .dockerignore to exclude unnecessary files
COPY . .

# Expose the internal Chainlit port (informational only)
EXPOSE 8000

# Start guardrails warmup daemon in background and Chainlit in foreground
# Using exec for Chainlit so it becomes PID 1 and receives signals properly
CMD sh -c "/app/.venv/bin/python /app/src/uitls/guardrails_warmup.py & exec /app/.venv/bin/chainlit run src/chatbot_chainlit_react.py --host ${HOST:-0.0.0.0} --port ${PORT:-8000}"
