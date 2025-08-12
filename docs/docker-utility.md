# Docker Manager Utility

A comprehensive command-line utility for managing the Fiddler Chatbot Docker container lifecycle.

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Commands](#commands)
- [Examples](#examples)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Quick Start

```bash
# Most common usage: rebuild without cache and run
./docker-manager.sh

# Build only
./docker-manager.sh build

# Run existing image
./docker-manager.sh run

# Development mode with hot-reload
./docker-manager.sh dev

# View logs
./docker-manager.sh logs
```

## Installation

1. Make the script executable:

    ```sh
    chmod +x docker-manager.sh
    ```

2. Ensure Docker is installed and running:

    ```sh
    docker --version  # Should be 24+
    ```

3. Ensure you have a `.env` file with required variables:

    ```sh
    # Required
    FIDDLER_API_KEY=your_api_key
    FIDDLER_APP_ID=your_app_id
    OPENAI_API_KEY=your_openai_key

    # Optional (defaults provided)
    FIDDLER_URL=preprod.cloud.fiddler.ai
    PORT=8000
    HOST=0.0.0.0
    ```

## Commands

### Default Command (No Arguments)

```bash
./docker-manager.sh
```

**Behavior**: Performs a clean rebuild (no cache) and runs the container

- Equivalent to: `./docker-manager.sh build --no-cache && ./docker-manager.sh run`
- Most common developer workflow
- Ensures latest code and dependencies

### `build` - Build Docker Image

```bash
./docker-manager.sh build [OPTIONS]
```

**Purpose**: Build the Docker image with various caching strategies

**Options**:

- `--no-cache` - Force rebuild without using cache (default for standalone build)
- `--cache` - Use Docker build cache if available
- `--tag NAME` - Custom image tag (default: `fiddler-chatbot:latest`)
- `--platform PLATFORM` - Build for specific platform (e.g., `linux/amd64`)

**Examples**:

```sh
./docker-manager.sh build                    # Build without cache
./docker-manager.sh build --cache            # Build with cache
./docker-manager.sh build --tag prod:v1.0    # Custom tag
```

### `run` - Run Container

```bash
./docker-manager.sh run [OPTIONS]
```

**Purpose**: Run the container from existing image

**Options**:

- `--port PORT` - Host port mapping (default: 8000)
- `--env-file FILE` - Environment file (default: `.env`)
- `--detach` / `-d` - Run in background
- `--name NAME` - Container name (default: `fiddler-chatbot`)
- `--no-rm` - Don't remove container on exit

**Examples**:

```sh
./docker-manager.sh run                      # Run on port 8000
./docker-manager.sh run --port 8080          # Custom port
./docker-manager.sh run -d                   # Run in background
./docker-manager.sh run --env-file prod.env  # Different env file
```

### `dev` - Development Mode

```bash
./docker-manager.sh dev [OPTIONS]
```

**Purpose**: Run container with hot-reload for development

**Features**:

- Mounts `./src` and `./public` directories
- Enables Chainlit watch mode
- Interactive terminal
- Auto-restarts on file changes

**Options**:

- `--port PORT` - Development port (default: 8000)
- `--mount PATH` - Additional paths to mount

**Example**:

```sh
./docker-manager.sh dev                      # Start dev mode
./docker-manager.sh dev --port 3000          # Custom port
./docker-manager.sh dev --mount ./configs    # Mount additional directory
```

### `test` - Run Tests

```sh
./docker-manager.sh test [OPTIONS]
```

**Purpose**: Run test suite inside container

**Options**:

- `--file FILE` - Run specific test file
- `--coverage` - Generate coverage report (default: true)
- `--verbose` / `-v` - Verbose output

**Examples**:

```sh
./docker-manager.sh test                     # Run all tests with coverage
./docker-manager.sh test --file test_validator_url.py  # Specific test
./docker-manager.sh test --no-coverage -v    # Verbose, no coverage
```

### `logs` - View Container Logs

```bash
./docker-manager.sh logs [OPTIONS]
```

**Purpose**: Display container logs

**Options**:

- `--follow` / `-f` - Follow log output (default: true)
- `--tail N` - Show last N lines (default: all)
- `--since TIME` - Show logs since timestamp

**Examples**:

```sh
./docker-manager.sh logs                     # Follow all logs
./docker-manager.sh logs --tail 100          # Last 100 lines
./docker-manager.sh logs --since 10m         # Last 10 minutes
```

### `stop` - Stop Container

```bash
./docker-manager.sh stop [OPTIONS]
```

**Purpose**: Stop running container

**Options**:

- `--name NAME` - Container name (default: `fiddler-chatbot`)
- `--all` - Stop all fiddler-chatbot containers

**Example**:

```sh
./docker-manager.sh stop                     # Stop default container
./docker-manager.sh stop --all               # Stop all related containers
```

### `clean` - Cleanup Resources

```sh
./docker-manager.sh clean [OPTIONS]
```

**Purpose**: Remove containers, images, and volumes

**Options**:

- `--containers` - Remove stopped containers
- `--images` - Remove images
- `--volumes` - Remove volumes
- `--all` - Remove everything (containers, images, volumes)
- `--force` - Don't prompt for confirmation

**Examples**:

```sh
./docker-manager.sh clean --containers       # Remove stopped containers
./docker-manager.sh clean --all              # Full cleanup (with prompt)
./docker-manager.sh clean --all --force      # Full cleanup (no prompt)
```

### `status` - Check Status

```sh
./docker-manager.sh status
```

**Purpose**: Display current Docker status

- Running containers
- Built images
- Port mappings
- Resource usage

### `shell` - Container Shell Access

```bash
./docker-manager.sh shell [OPTIONS]
```

**Purpose**: Open interactive shell in running container

**Options**:

- `--name NAME` - Container name (default: `fiddler-chatbot`)
- `--new` - Start new container with shell

**Example**:

```sh
./docker-manager.sh shell                    # Shell into running container
./docker-manager.sh shell --new              # Start new container with shell
```

## Global Options

These options work with all commands:

- `--help` / `-h` - Show help message
- `--version` / `-v` - Show script version
- `--dry-run` - Show commands without executing
- `--quiet` / `-q` - Suppress non-error output
- `--verbose` - Enable verbose output

## Configuration

### Environment Variables

The script respects these environment variables:

```bash
# Docker settings
DOCKER_IMAGE_NAME="fiddler-chatbot"          # Base image name
DOCKER_IMAGE_TAG="latest"                    # Default tag
DOCKER_CONTAINER_NAME="fiddler-chatbot"      # Default container name

# App settings
DEFAULT_PORT="8000"                          # Default port
DEFAULT_ENV_FILE=".env"                      # Default env file

# Build settings
DEFAULT_BUILD_CACHE="false"                  # Use cache by default
DEFAULT_PLATFORM=""                          # Auto-detect platform
```

### Configuration File

Create `.docker-manager.conf` for persistent settings:

```bash
# .docker-manager.conf
DEFAULT_PORT=8080
DEFAULT_ENV_FILE=production.env
DOCKER_IMAGE_TAG=prod
DEFAULT_BUILD_CACHE=true
```

## Examples

### Common Workflows

#### Daily Development

```sh
# Morning: Clean rebuild and start
./docker-manager.sh

# During development: Use dev mode
./docker-manager.sh dev

# Check logs when debugging
./docker-manager.sh logs --tail 50

# End of day: Clean up
./docker-manager.sh stop
```

#### Production Deployment

```sh
# Build production image
./docker-manager.sh build --tag prod:v1.0 --platform linux/amd64

# Run with production config
./docker-manager.sh run --env-file prod.env --name fiddler-prod -d

# Monitor
./docker-manager.sh logs --name fiddler-prod
```

#### Testing Workflow

```sh
# Run full test suite
./docker-manager.sh test

# Run specific tests
./docker-manager.sh test --file test_validator_url.py -v

# Test in fresh container
./docker-manager.sh build --no-cache && ./docker-manager.sh test
```

### Advanced Usage

#### Multiple Environments

```sh
# Development
./docker-manager.sh run --env-file dev.env --name fiddler-dev --port 8000

# Staging
./docker-manager.sh run --env-file staging.env --name fiddler-staging --port 8001

# Production
./docker-manager.sh run --env-file prod.env --name fiddler-prod --port 8002
```

#### CI/CD Integration

```sh
# CI build script
./docker-manager.sh build --no-cache --tag "fiddler:${CI_COMMIT_SHA}"

# Run tests
./docker-manager.sh test --coverage

# Deploy if tests pass
if [ $? -eq 0 ]; then
    ./docker-manager.sh run --tag "fiddler:${CI_COMMIT_SHA}" -d
fi
```

## Troubleshooting

### Common Issues

#### Port Already in Use

```sh
# Check what's using the port
lsof -i :8000

# Use different port
./docker-manager.sh run --port 8080
```

#### Container Won't Start

```sh
# Check logs
./docker-manager.sh logs --tail 100

# Try clean rebuild
./docker-manager.sh clean --all
./docker-manager.sh build --no-cache
./docker-manager.sh run
```

#### Permission Denied

```sh
# Make script executable
chmod +x docker-manager.sh

# Run with sudo if needed (not recommended)
sudo ./docker-manager.sh
```

#### Out of Disk Space

```sh
# Clean up Docker resources
./docker-manager.sh clean --all --force

# Prune Docker system
docker system prune -a
```

### Debug Mode

Enable debug output for troubleshooting:

```sh
DEBUG=1 ./docker-manager.sh build
```

### Getting Help

```bash
# Show general help
./docker-manager.sh --help

# Show command-specific help
./docker-manager.sh build --help
./docker-manager.sh run --help
```

## Best Practices

- Always use `.env` files for secrets (never commit them)
- Tag production images with version numbers
- Use `--dry-run` to preview commands before execution
- Run `clean` periodically to free disk space
- Use dev mode for local development, not production
- Monitor logs when deploying new versions
- Test in container before deploying

## Version History

- **1.0.0** - Initial release with core commands
- **1.1.0** - Added dev mode and test commands
- **1.2.0** - Added configuration file support
- **1.3.0** - Added shell access and status commands

## Contributing

To add new features to the Docker manager:

1. Update this documentation first
2. Implement the feature in the script
3. Add tests if applicable
4. Update version number

## License

This utility is part of the Fiddler Chatbot project and follows the same license.
