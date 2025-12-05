# Dev Container Setup

This directory contains the configuration for running the Fiddler Chatbot application in a Docker container using VSCode/Cursor's Dev Containers feature.

## Quick Start

1. **Ensure you have Docker installed and running**
   - Docker Desktop on macOS/Windows
   - Docker Engine on Linux

2. **Create a `.env` file** in the project root (if you haven't already)
   ```bash
   cp .env.template .env
   # Edit .env with your API keys
   ```

3. **Open in Dev Container**
   - In VSCode/Cursor, press `F1` (or `Cmd+Shift+P` on Mac)
   - Select: **"Dev Containers: Reopen in Container"**
   - Wait for the container to build and start (first time may take a few minutes)

4. **The application will automatically start**
   - Chainlit will run on port 8000
   - Your browser will automatically open to `http://localhost:8000`
   - Port forwarding is handled automatically by VSCode/Cursor

## What This Setup Provides

- ✅ **One-click Docker debugging** - Just reopen in container
- ✅ **Automatic port forwarding** - Port 8000 is forwarded and opened in browser
- ✅ **Live code editing** - Your workspace is mounted, so changes are reflected immediately
- ✅ **Environment variables** - `.env` file is automatically mounted
- ✅ **Python environment** - Pre-configured with all dependencies
- ✅ **Integrated terminal** - Run commands directly in the container

## Configuration

- **`devcontainer.json`** - Devcontainer configuration that builds from the root `Dockerfile`
- **`Dockerfile`** (in project root) - Defines the container image and dependencies

The setup uses VSCode/Cursor's native Dockerfile support - no docker-compose needed!

## Troubleshooting

### Port 8000 is already in use
The port forwarding is configured in `devcontainer.json`. You can change it:
```json
"forwardPorts": [8001],  // Use port 8001 instead
"portsAttributes": {
  "8001": {
    "label": "Chainlit Application",
    "onAutoForward": "openPreview"
  }
}
```

### Environment variables not loading
- Ensure `.env` file exists in the project root
- Check that the file is not in `.dockerignore` (it should be excluded from Docker build but available for mounting)
- Restart the dev container after creating/updating `.env`

### Container won't start
- Check Docker is running: `docker ps`
- View logs: Check Docker Desktop or use `docker logs <container-id>`
- Rebuild: Use "Dev Containers: Rebuild Container" from the command palette

### Application not starting automatically
The application starts via `postAttachCommand` in `devcontainer.json`. You can manually start it:
```bash
/app/.venv/bin/chainlit run src/chatbot_chainlit_react.py --host 0.0.0.0 --port 8000
```

## Manual Container Management

If you prefer to run the container manually outside of Dev Containers:

```bash
# Build
docker build -t fiddler-chatbot:dev .

# Run (with port forwarding and .env)
docker run --rm -it \
  --name fiddler-chatbot-dev \
  -p 8000:8000 \
  -v "$(pwd):/app" \
  -v "$(pwd)/.env:/app/.env:ro" \
  --env-file .env \
  fiddler-chatbot:dev \
  sh -c "sleep infinity"
```
