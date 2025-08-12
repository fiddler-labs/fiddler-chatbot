#!/usr/bin/env bash

# Docker Manager for Fiddler Chatbot
# Version: 1.3.0
# Description: Comprehensive Docker container lifecycle management utility

set -euo pipefail

# ============================================================================
# Configuration and Defaults
# ============================================================================

# Script metadata
readonly SCRIPT_VERSION="1.3.0"
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Docker defaults
DOCKER_IMAGE_NAME="${DOCKER_IMAGE_NAME:-fiddler-chatbot}"
DOCKER_IMAGE_TAG="${DOCKER_IMAGE_TAG:-latest}"
DOCKER_CONTAINER_NAME="${DOCKER_CONTAINER_NAME:-fiddler-chatbot}"

# Application defaults
DEFAULT_PORT="${DEFAULT_PORT:-8000}"
DEFAULT_ENV_FILE="${DEFAULT_ENV_FILE:-.env}"
DEFAULT_HOST="${DEFAULT_HOST:-0.0.0.0}"

# Build defaults
DEFAULT_BUILD_CACHE="${DEFAULT_BUILD_CACHE:-false}"
DEFAULT_PLATFORM="${DEFAULT_PLATFORM:-}"

# Runtime flags
DRY_RUN=false
QUIET=false
VERBOSE=false
DEBUG="${DEBUG:-}"

# Colors for output (disabled if not TTY)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    BOLD=''
    NC=''
fi

# ============================================================================
# Utility Functions
# ============================================================================

# Print colored output
print_color() {
    local color="$1"
    shift
    echo -e "${color}$*${NC}"
}

# Print info message
info() {
    [[ "$QUIET" == "true" ]] && return
    print_color "$BLUE" "ℹ️  $*"
}

# Print success message
success() {
    [[ "$QUIET" == "true" ]] && return
    print_color "$GREEN" "✅ $*"
}

# Print warning message
warn() {
    print_color "$YELLOW" "⚠️  $*" >&2
}

# Print error message
error() {
    print_color "$RED" "❌ $*" >&2
}

# Print debug message
debug() {
    [[ -n "$DEBUG" ]] && print_color "$CYAN" "🔍 DEBUG: $*" >&2
}

# Print verbose message
verbose() {
    [[ "$VERBOSE" == "true" ]] && print_color "$CYAN" "➤ $*"
}

# Execute command (respects dry-run)
execute() {
    local cmd="$*"

    if [[ "$DRY_RUN" == "true" ]]; then
        print_color "$CYAN" "[DRY-RUN] $cmd"
    else
        verbose "Executing: $cmd"
        if [[ "$VERBOSE" == "true" ]]; then
            eval "$cmd"
        else
            eval "$cmd" > /dev/null 2>&1 || {
                error "Command failed: $cmd"
                return 1
            }
        fi
    fi
}

# Check if Docker is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed or not in PATH"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        error "Docker daemon is not running"
        exit 1
    fi

    debug "Docker is available and running"
}

# Check if container is running
is_container_running() {
    local name="${1:-$DOCKER_CONTAINER_NAME}"
    docker ps --format '{{.Names}}' | grep -q "^${name}$"
}

# Check if image exists
image_exists() {
    local image="${1:-$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG}"
    docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "^${image}$"
}

# Load configuration file if exists
load_config() {
    local config_file="${SCRIPT_DIR}/.docker-manager.conf"
    if [[ -f "$config_file" ]]; then
        debug "Loading configuration from $config_file"
        # shellcheck source=/dev/null
        source "$config_file"
    fi
}

# Confirm action
confirm() {
    local message="${1:-Are you sure?}"
    local response

    if [[ "$DRY_RUN" == "true" ]]; then
        return 0
    fi

    read -r -p "$(print_color "$YELLOW" "$message [y/N]: ")" response
    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# ============================================================================
# Command Functions
# ============================================================================

# Build Docker image
cmd_build() {
    local use_cache="$DEFAULT_BUILD_CACHE"
    local tag="$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG"
    local platform="$DEFAULT_PLATFORM"

    # Parse build options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --cache)
                use_cache="true"
                shift
                ;;
            --no-cache)
                use_cache="false"
                shift
                ;;
            --tag)
                tag="$2"
                shift 2
                ;;
            --platform)
                platform="$2"
                shift 2
                ;;
            --help|-h)
                show_build_help
                exit 0
                ;;
            *)
                error "Unknown build option: $1"
                show_build_help
                exit 1
                ;;
        esac
    done

    info "Building Docker image: $tag"

    local build_cmd="docker build"

    if [[ "$use_cache" == "false" ]]; then
        build_cmd="$build_cmd --no-cache"
        verbose "Building without cache"
    else
        verbose "Using Docker build cache"
    fi

    if [[ -n "$platform" ]]; then
        build_cmd="$build_cmd --platform $platform"
        verbose "Building for platform: $platform"
    fi

    build_cmd="$build_cmd -t $tag ."

    execute "cd '$SCRIPT_DIR' && $build_cmd"

    if [[ $? -eq 0 ]]; then
        success "Successfully built image: $tag"
    else
        error "Failed to build image"
        exit 1
    fi
}

# Run container
cmd_run() {
    local port="$DEFAULT_PORT"
    local env_file="$DEFAULT_ENV_FILE"
    local container_name="$DOCKER_CONTAINER_NAME"
    local image_tag="$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG"
    local detach=false
    local remove=true

    # Parse run options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --port|-p)
                port="$2"
                shift 2
                ;;
            --env-file)
                env_file="$2"
                shift 2
                ;;
            --name)
                container_name="$2"
                shift 2
                ;;
            --tag)
                image_tag="$2"
                shift 2
                ;;
            --detach|-d)
                detach=true
                shift
                ;;
            --no-rm)
                remove=false
                shift
                ;;
            --help|-h)
                show_run_help
                exit 0
                ;;
            *)
                error "Unknown run option: $1"
                show_run_help
                exit 1
                ;;
        esac
    done

    # Check if image exists
    if ! image_exists "$image_tag"; then
        warn "Image $image_tag not found. Building it first..."
        cmd_build
    fi

    # Check if container is already running
    if is_container_running "$container_name"; then
        warn "Container $container_name is already running"
        if confirm "Stop existing container and start new one?"; then
            info "Stopping existing container..."
            execute "docker stop $container_name"
            execute "docker rm $container_name 2>/dev/null || true"
        else
            exit 1
        fi
    fi

    # Check env file
    if [[ ! -f "$env_file" ]]; then
        error "Environment file not found: $env_file"
        exit 1
    fi

    info "Starting container: $container_name"
    verbose "Image: $image_tag"
    verbose "Port: $port"
    verbose "Env file: $env_file"

    local run_cmd="docker run"

    [[ "$remove" == "true" ]] && run_cmd="$run_cmd --rm"
    [[ "$detach" == "true" ]] && run_cmd="$run_cmd -d"

    run_cmd="$run_cmd --name $container_name"
    run_cmd="$run_cmd -p ${port}:8000"
    run_cmd="$run_cmd --env-file '$env_file'"
    run_cmd="$run_cmd $image_tag"

    execute "$run_cmd"

    if [[ $? -eq 0 ]]; then
        success "Container started successfully"
        if [[ "$detach" == "false" ]]; then
            info "Container is running in foreground. Press Ctrl+C to stop."
        else
            info "Container is running in background"
            info "View logs: $SCRIPT_NAME logs"
            info "Stop container: $SCRIPT_NAME stop"
        fi
        info "Application available at: http://localhost:${port}"
    else
        error "Failed to start container"
        exit 1
    fi
}

# Development mode
cmd_dev() {
    local port="$DEFAULT_PORT"
    local additional_mounts=""

    # Parse dev options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --port|-p)
                port="$2"
                shift 2
                ;;
            --mount)
                additional_mounts="$additional_mounts -v '$(pwd)/$2:/app/$2'"
                shift 2
                ;;
            --help|-h)
                show_dev_help
                exit 0
                ;;
            *)
                error "Unknown dev option: $1"
                show_dev_help
                exit 1
                ;;
        esac
    done

    # Check if image exists
    if ! image_exists; then
        warn "Image not found. Building it first..."
        cmd_build --cache
    fi

    info "Starting development mode on port $port"
    info "Hot-reload enabled for src/ and public/ directories"

    local dev_cmd="docker run --rm -it"
    dev_cmd="$dev_cmd --name ${DOCKER_CONTAINER_NAME}-dev"
    dev_cmd="$dev_cmd -p ${port}:8000"
    dev_cmd="$dev_cmd --env-file '${DEFAULT_ENV_FILE}'"
    dev_cmd="$dev_cmd -v '${SCRIPT_DIR}/src:/app/src'"
    dev_cmd="$dev_cmd -v '${SCRIPT_DIR}/public:/app/public'"
    dev_cmd="$dev_cmd $additional_mounts"
    dev_cmd="$dev_cmd $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG"
    dev_cmd="$dev_cmd sh -lc '/app/.venv/bin/chainlit run src/chatbot_chainlit.py -w --host 0.0.0.0 --port 8000'"

    execute "$dev_cmd"
}

# Run tests
cmd_test() {
    local test_file=""
    local coverage=true
    local verbose_flag=""

    # Parse test options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --file|-f)
                test_file="$2"
                shift 2
                ;;
            --no-coverage)
                coverage=false
                shift
                ;;
            --verbose|-v)
                verbose_flag="-v"
                shift
                ;;
            --help|-h)
                show_test_help
                exit 0
                ;;
            *)
                error "Unknown test option: $1"
                show_test_help
                exit 1
                ;;
        esac
    done

    # Check if image exists
    if ! image_exists; then
        warn "Image not found. Building it first..."
        cmd_build --cache
    fi

    info "Running tests in container"

    local test_cmd="docker run --rm -it"
    test_cmd="$test_cmd -v '${SCRIPT_DIR}/tests:/app/tests'"
    test_cmd="$test_cmd -v '${SCRIPT_DIR}/pytest.ini:/app/pytest.ini'"
    test_cmd="$test_cmd $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG"
    test_cmd="$test_cmd sh -lc 'uv run pytest"

    if [[ -n "$test_file" ]]; then
        test_cmd="$test_cmd tests/agentic_tools/${test_file}"
        verbose "Running specific test: $test_file"
    fi

    if [[ "$coverage" == "true" ]]; then
        test_cmd="$test_cmd --cov=src --cov-report=term-missing"
        verbose "Coverage reporting enabled"
    fi

    test_cmd="$test_cmd $verbose_flag'"

    execute "$test_cmd"

    if [[ $? -eq 0 ]]; then
        success "Tests completed successfully"
    else
        error "Tests failed"
        exit 1
    fi
}

# View logs
cmd_logs() {
    local follow=true
    local tail_lines=""
    local since=""
    local container_name="$DOCKER_CONTAINER_NAME"

    # Parse logs options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --no-follow)
                follow=false
                shift
                ;;
            --follow|-f)
                follow=true
                shift
                ;;
            --tail)
                tail_lines="$2"
                shift 2
                ;;
            --since)
                since="$2"
                shift 2
                ;;
            --name)
                container_name="$2"
                shift 2
                ;;
            --help|-h)
                show_logs_help
                exit 0
                ;;
            *)
                error "Unknown logs option: $1"
                show_logs_help
                exit 1
                ;;
        esac
    done

    if ! is_container_running "$container_name"; then
        error "Container $container_name is not running"
        exit 1
    fi

    local logs_cmd="docker logs"

    [[ "$follow" == "true" ]] && logs_cmd="$logs_cmd -f"
    [[ -n "$tail_lines" ]] && logs_cmd="$logs_cmd --tail $tail_lines"
    [[ -n "$since" ]] && logs_cmd="$logs_cmd --since $since"

    logs_cmd="$logs_cmd $container_name"

    info "Showing logs for container: $container_name"
    [[ "$follow" == "true" ]] && info "Following logs. Press Ctrl+C to stop."

    execute "$logs_cmd"
}

# Stop container
cmd_stop() {
    local container_name="$DOCKER_CONTAINER_NAME"
    local stop_all=false

    # Parse stop options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --name)
                container_name="$2"
                shift 2
                ;;
            --all)
                stop_all=true
                shift
                ;;
            --help|-h)
                show_stop_help
                exit 0
                ;;
            *)
                error "Unknown stop option: $1"
                show_stop_help
                exit 1
                ;;
        esac
    done

    if [[ "$stop_all" == "true" ]]; then
        info "Stopping all fiddler-chatbot containers"
        local containers=$(docker ps --format '{{.Names}}' | grep "^${DOCKER_CONTAINER_NAME}")
        if [[ -z "$containers" ]]; then
            warn "No fiddler-chatbot containers are running"
            exit 0
        fi
        for container in $containers; do
            info "Stopping $container"
            execute "docker stop $container"
        done
        success "All containers stopped"
    else
        if ! is_container_running "$container_name"; then
            warn "Container $container_name is not running"
            exit 0
        fi

        info "Stopping container: $container_name"
        execute "docker stop $container_name"
        success "Container stopped"
    fi
}

# Clean up resources
cmd_clean() {
    local clean_containers=false
    local clean_images=false
    local clean_volumes=false
    local clean_all=false
    local force=false

    # Parse clean options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --containers)
                clean_containers=true
                shift
                ;;
            --images)
                clean_images=true
                shift
                ;;
            --volumes)
                clean_volumes=true
                shift
                ;;
            --all)
                clean_all=true
                shift
                ;;
            --force)
                force=true
                shift
                ;;
            --help|-h)
                show_clean_help
                exit 0
                ;;
            *)
                error "Unknown clean option: $1"
                show_clean_help
                exit 1
                ;;
        esac
    done

    # If --all, enable all cleanup options
    if [[ "$clean_all" == "true" ]]; then
        clean_containers=true
        clean_images=true
        clean_volumes=true
    fi

    # If no specific option, default to containers
    if [[ "$clean_containers" == "false" && "$clean_images" == "false" && "$clean_volumes" == "false" ]]; then
        clean_containers=true
    fi

    # Confirm if not forced
    if [[ "$force" == "false" ]]; then
        local items=""
        [[ "$clean_containers" == "true" ]] && items="${items}containers, "
        [[ "$clean_images" == "true" ]] && items="${items}images, "
        [[ "$clean_volumes" == "true" ]] && items="${items}volumes, "
        items="${items%, }"  # Remove trailing comma

        if ! confirm "This will remove Docker ${items}. Continue?"; then
            info "Cleanup cancelled"
            exit 0
        fi
    fi

    info "Starting cleanup..."

    if [[ "$clean_containers" == "true" ]]; then
        info "Removing stopped containers..."
        execute "docker ps -a --format '{{.Names}}' | grep '^${DOCKER_CONTAINER_NAME}' | xargs -r docker rm -f"
    fi

    if [[ "$clean_images" == "true" ]]; then
        info "Removing images..."
        execute "docker images --format '{{.Repository}}:{{.Tag}}' | grep '^${DOCKER_IMAGE_NAME}' | xargs -r docker rmi -f"
    fi

    if [[ "$clean_volumes" == "true" ]]; then
        info "Removing volumes..."
        execute "docker volume ls --format '{{.Name}}' | grep '${DOCKER_CONTAINER_NAME}' | xargs -r docker volume rm -f"
    fi

    success "Cleanup completed"
}

# Show status
cmd_status() {
    info "Docker Status Report"
    echo ""

    print_color "$BOLD" "Containers:"
    local containers=$(docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep "${DOCKER_CONTAINER_NAME}" 2>/dev/null || echo "  None found")
    echo "$containers"
    echo ""

    print_color "$BOLD" "Images:"
    local images=$(docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}' | grep "${DOCKER_IMAGE_NAME}" 2>/dev/null || echo "  None found")
    echo "$images"
    echo ""

    print_color "$BOLD" "Resource Usage:"
    if is_container_running; then
        docker stats --no-stream --format 'table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}' "${DOCKER_CONTAINER_NAME}"
    else
        echo "  No running containers"
    fi
}

# Shell access
cmd_shell() {
    local container_name="$DOCKER_CONTAINER_NAME"
    local new_container=false

    # Parse shell options
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --name)
                container_name="$2"
                shift 2
                ;;
            --new)
                new_container=true
                shift
                ;;
            --help|-h)
                show_shell_help
                exit 0
                ;;
            *)
                error "Unknown shell option: $1"
                show_shell_help
                exit 1
                ;;
        esac
    done

    if [[ "$new_container" == "true" ]]; then
        info "Starting new container with shell access"
        execute "docker run --rm -it --entrypoint /bin/bash $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG"
    else
        if ! is_container_running "$container_name"; then
            error "Container $container_name is not running"
            exit 1
        fi

        info "Opening shell in container: $container_name"
        execute "docker exec -it $container_name /bin/bash"
    fi
}

# ============================================================================
# Help Functions
# ============================================================================

show_help() {
    cat << EOF
$(print_color "$BOLD" "Docker Manager for Fiddler Chatbot v${SCRIPT_VERSION}")

$(print_color "$CYAN" "USAGE:")
    $SCRIPT_NAME [COMMAND] [OPTIONS]

$(print_color "$CYAN" "COMMANDS:")
    $(print_color "$GREEN" "build")       Build Docker image
    $(print_color "$GREEN" "run")         Run container from image
    $(print_color "$GREEN" "dev")         Start development mode with hot-reload
    $(print_color "$GREEN" "test")        Run tests in container
    $(print_color "$GREEN" "logs")        View container logs
    $(print_color "$GREEN" "stop")        Stop running container
    $(print_color "$GREEN" "clean")       Remove containers/images/volumes
    $(print_color "$GREEN" "status")      Show Docker status
    $(print_color "$GREEN" "shell")       Access container shell

$(print_color "$CYAN" "DEFAULT BEHAVIOR:")
    Running without arguments performs: build --no-cache && run

$(print_color "$CYAN" "GLOBAL OPTIONS:")
    --help, -h      Show this help message
    --version, -v   Show script version
    --dry-run       Preview commands without execution
    --quiet, -q     Suppress non-error output
    --verbose       Enable verbose output

$(print_color "$CYAN" "EXAMPLES:")
    $SCRIPT_NAME                    # Build and run (most common)
    $SCRIPT_NAME build --no-cache   # Force rebuild
    $SCRIPT_NAME run --port 8080    # Run on different port
    $SCRIPT_NAME dev                # Development mode
    $SCRIPT_NAME test               # Run all tests
    $SCRIPT_NAME logs -f            # Follow logs

For command-specific help, use: $SCRIPT_NAME [COMMAND] --help
EOF
}

show_build_help() {
    cat << EOF
$(print_color "$BOLD" "BUILD COMMAND")

Build Docker image with various options.

$(print_color "$CYAN" "USAGE:")
    $SCRIPT_NAME build [OPTIONS]

$(print_color "$CYAN" "OPTIONS:")
    --cache         Use Docker build cache
    --no-cache      Force rebuild without cache (default)
    --tag NAME      Custom image tag (default: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG})
    --platform PLAT Build for specific platform
    --help, -h      Show this help

$(print_color "$CYAN" "EXAMPLES:")
    $SCRIPT_NAME build                      # Build without cache
    $SCRIPT_NAME build --cache              # Use cache if available
    $SCRIPT_NAME build --tag prod:v1.0      # Custom tag
EOF
}

show_run_help() {
    cat << EOF
$(print_color "$BOLD" "RUN COMMAND")

Run container from built image.

$(print_color "$CYAN" "USAGE:")
    $SCRIPT_NAME run [OPTIONS]

$(print_color "$CYAN" "OPTIONS:")
    --port, -p PORT     Host port (default: ${DEFAULT_PORT})
    --env-file FILE     Environment file (default: ${DEFAULT_ENV_FILE})
    --name NAME         Container name (default: ${DOCKER_CONTAINER_NAME})
    --tag TAG           Image tag to run
    --detach, -d        Run in background
    --no-rm             Don't remove container on exit
    --help, -h          Show this help

$(print_color "$CYAN" "EXAMPLES:")
    $SCRIPT_NAME run                        # Run with defaults
    $SCRIPT_NAME run --port 8080            # Different port
    $SCRIPT_NAME run -d                     # Background mode
EOF
}

show_dev_help() {
    cat << EOF
$(print_color "$BOLD" "DEV COMMAND")

Start development mode with hot-reload.

$(print_color "$CYAN" "USAGE:")
    $SCRIPT_NAME dev [OPTIONS]

$(print_color "$CYAN" "OPTIONS:")
    --port, -p PORT     Development port (default: ${DEFAULT_PORT})
    --mount PATH        Additional path to mount
    --help, -h          Show this help

$(print_color "$CYAN" "FEATURES:")
    - Mounts src/ and public/ directories
    - Enables Chainlit watch mode
    - Auto-restarts on file changes

$(print_color "$CYAN" "EXAMPLES:")
    $SCRIPT_NAME dev                        # Start dev mode
    $SCRIPT_NAME dev --port 3000            # Custom port
EOF
}

show_test_help() {
    cat << EOF
$(print_color "$BOLD" "TEST COMMAND")

Run test suite in container.

$(print_color "$CYAN" "USAGE:")
    $SCRIPT_NAME test [OPTIONS]

$(print_color "$CYAN" "OPTIONS:")
    --file, -f FILE     Run specific test file
    --no-coverage       Disable coverage report
    --verbose, -v       Verbose output
    --help, -h          Show this help

$(print_color "$CYAN" "EXAMPLES:")
    $SCRIPT_NAME test                       # All tests with coverage
    $SCRIPT_NAME test --file test_url.py    # Specific test
    $SCRIPT_NAME test -v --no-coverage      # Verbose, no coverage
EOF
}

show_logs_help() {
    cat << EOF
$(print_color "$BOLD" "LOGS COMMAND")

View container logs.

$(print_color "$CYAN" "USAGE:")
    $SCRIPT_NAME logs [OPTIONS]

$(print_color "$CYAN" "OPTIONS:")
    --follow, -f        Follow log output (default)
    --no-follow         Don't follow logs
    --tail N            Show last N lines
    --since TIME        Show logs since timestamp
    --name NAME         Container name
    --help, -h          Show this help

$(print_color "$CYAN" "EXAMPLES:")
    $SCRIPT_NAME logs                       # Follow all logs
    $SCRIPT_NAME logs --tail 100            # Last 100 lines
    $SCRIPT_NAME logs --since 10m           # Last 10 minutes
EOF
}

show_stop_help() {
    cat << EOF
$(print_color "$BOLD" "STOP COMMAND")

Stop running container(s).

$(print_color "$CYAN" "USAGE:")
    $SCRIPT_NAME stop [OPTIONS]

$(print_color "$CYAN" "OPTIONS:")
    --name NAME         Container name (default: ${DOCKER_CONTAINER_NAME})
    --all               Stop all fiddler containers
    --help, -h          Show this help

$(print_color "$CYAN" "EXAMPLES:")
    $SCRIPT_NAME stop                       # Stop default container
    $SCRIPT_NAME stop --all                 # Stop all containers
EOF
}

show_clean_help() {
    cat << EOF
$(print_color "$BOLD" "CLEAN COMMAND")

Remove Docker resources.

$(print_color "$CYAN" "USAGE:")
    $SCRIPT_NAME clean [OPTIONS]

$(print_color "$CYAN" "OPTIONS:")
    --containers        Remove stopped containers
    --images            Remove images
    --volumes           Remove volumes
    --all               Remove everything
    --force             Don't prompt for confirmation
    --help, -h          Show this help

$(print_color "$CYAN" "EXAMPLES:")
    $SCRIPT_NAME clean --containers         # Remove containers only
    $SCRIPT_NAME clean --all                # Full cleanup
    $SCRIPT_NAME clean --all --force        # No confirmation
EOF
}

show_shell_help() {
    cat << EOF
$(print_color "$BOLD" "SHELL COMMAND")

Access container shell.

$(print_color "$CYAN" "USAGE:")
    $SCRIPT_NAME shell [OPTIONS]

$(print_color "$CYAN" "OPTIONS:")
    --name NAME         Container name (default: ${DOCKER_CONTAINER_NAME})
    --new               Start new container with shell
    --help, -h          Show this help

$(print_color "$CYAN" "EXAMPLES:")
    $SCRIPT_NAME shell                      # Shell into running container
    $SCRIPT_NAME shell --new                # New container with shell
EOF
}

# ============================================================================
# Main Script Logic
# ============================================================================

main() {
    # Load configuration
    load_config

    # Check Docker availability
    check_docker

    # Parse global options
    local command=""
    local args=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --help|-h)
                show_help
                exit 0
                ;;
            --version|-v)
                echo "Docker Manager v${SCRIPT_VERSION}"
                exit 0
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --quiet|-q)
                QUIET=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            build|run|dev|test|logs|stop|clean|status|shell)
                command="$1"
                shift
                args=("$@")
                break
                ;;
            *)
                error "Unknown option or command: $1"
                show_help
                exit 1
                ;;
        esac
    done

    # Execute command or default behavior
    if [[ -z "$command" ]]; then
        # Default behavior: build without cache and run
        info "Executing default workflow: build (no-cache) + run"
        cmd_build --no-cache
        cmd_run
    else
        # Execute specific command
        case "$command" in
            build)
                cmd_build "${args[@]}"
                ;;
            run)
                cmd_run "${args[@]}"
                ;;
            dev)
                cmd_dev "${args[@]}"
                ;;
            test)
                cmd_test "${args[@]}"
                ;;
            logs)
                cmd_logs "${args[@]}"
                ;;
            stop)
                cmd_stop "${args[@]}"
                ;;
            clean)
                cmd_clean "${args[@]}"
                ;;
            status)
                cmd_status "${args[@]}"
                ;;
            shell)
                cmd_shell "${args[@]}"
                ;;
            *)
                error "Unknown command: $command"
                show_help
                exit 1
                ;;
        esac
    fi
}

# Run main function
main "$@"
