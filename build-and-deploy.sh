#!/bin/bash

# Build, tag, push and restart fiddler-chatbot deployment script
# This script builds a Docker image, tags it, pushes to ECR, and restarts the Kubernetes deployment

set -e  # Exit on any error

# Configuration
ECR_REGISTRY="079310353266.dkr.ecr.us-west-2.amazonaws.com"
IMAGE_NAME="fiddler-chatbot"
TAG="latest"
NAMESPACE="fiddler-chatbot"
AWS_REGION="us-west-2"
EKS_CLUSTER="fdl-extqa"

# Build options (can be overridden via CLI arguments)
DISABLE_CACHE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    if ! command_exists docker; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi

    if ! command_exists aws; then
        log_error "AWS CLI is not installed or not in PATH"
        exit 1
    fi

    if ! command_exists kubectl; then
        log_error "kubectl is not installed or not in PATH"
        exit 1
    fi

    log_success "All prerequisites are available"
}

# Function to authenticate to ECR
authenticate_ecr() {
    log_info "Authenticating to ECR..."

    aws ecr get-login-password \
        --region "$AWS_REGION" \
    | docker login \
        --username AWS \
        --password-stdin "$ECR_REGISTRY"

    if [ $? -eq 0 ]; then
        log_success "Successfully authenticated to ECR"
    else
        log_error "Failed to authenticate to ECR"
        exit 1
    fi
}

# Function to build Docker image
build_image() {
    log_info "Building Docker image..."

    # Build Docker image with optional --no-cache flag
    if [ "$DISABLE_CACHE" = true ]; then
        log_info "Docker build cache disabled (--no-cache flag enabled)"
        docker build --no-cache -t "$IMAGE_NAME:$TAG" .
    else
        log_info "Docker build cache enabled (using cached intermediate layers)"
        docker build -t "$IMAGE_NAME:$TAG" .
    fi

    if [ $? -eq 0 ]; then
        log_success "Docker image built successfully"
    else
        log_error "Failed to build Docker image"
        exit 1
    fi
}

# Function to tag image for ECR
tag_image() {
    log_info "Tagging image for ECR..."

    local full_image_name="$ECR_REGISTRY/$IMAGE_NAME:$TAG"
    docker tag "$IMAGE_NAME:$TAG" "$full_image_name"

    if [ $? -eq 0 ]; then
        log_success "Image tagged as $full_image_name"
    else
        log_error "Failed to tag image"
        exit 1
    fi
}

# Function to push image to ECR
push_image() {
    log_info "Pushing image to ECR..."

    local full_image_name="$ECR_REGISTRY/$IMAGE_NAME:$TAG"
    docker push "$full_image_name"

    if [ $? -eq 0 ]; then
        log_success "Image pushed to ECR successfully"
    else
        log_error "Failed to push image to ECR"
        exit 1
    fi
}

# Function to configure kubectl context
configure_kubectl() {
    log_info "Configuring kubectl for EKS cluster: $EKS_CLUSTER"

    # Check if kubectl context is already set to the correct cluster
    current_context=$(kubectl config current-context 2>/dev/null || echo "")

    if [[ "$current_context" == *"$EKS_CLUSTER"* ]]; then
        log_info "kubectl is already configured for cluster: $EKS_CLUSTER"
    else
        log_info "Updating kubectl context to use cluster: $EKS_CLUSTER"
        aws eks update-kubeconfig --region "$AWS_REGION" --name "$EKS_CLUSTER"

        if [ $? -eq 0 ]; then
            log_success "kubectl configured for cluster: $EKS_CLUSTER"
        else
            log_error "Failed to configure kubectl for cluster: $EKS_CLUSTER"
            exit 1
        fi
    fi
}

# Function to restart deployment
restart_deployment() {
    log_info "Restarting deployment in namespace: $NAMESPACE"

    # Check if namespace exists
    if ! kubectl get namespace "$NAMESPACE" >/dev/null 2>&1; then
        log_error "Namespace '$NAMESPACE' does not exist"
        exit 1
    fi

    # Check if deployment exists
    if ! kubectl get deployment -n "$NAMESPACE" >/dev/null 2>&1; then
        log_error "No deployments found in namespace '$NAMESPACE'"
        exit 1
    fi

    # Restart the deployment
    kubectl rollout restart deployment -n "$NAMESPACE"

    if [ $? -eq 0 ]; then
        log_success "Deployment restart initiated successfully"

        # Wait for rollout to complete
        log_info "Waiting for rollout to complete..."
        kubectl rollout status deployment -n "$NAMESPACE" --timeout=300s

        if [ $? -eq 0 ]; then
            log_success "Deployment rollout completed successfully"
        else
            log_warning "Deployment rollout may still be in progress or failed"
        fi
    else
        log_error "Failed to restart deployment"
        exit 1
    fi
}

# Function to show deployment status
show_deployment_status() {
    log_info "Current deployment status:"
    kubectl get pods -n "$NAMESPACE" -o wide
    echo ""
    kubectl get deployment -n "$NAMESPACE" -o wide
}

# Function to show usage information
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Build, tag, push and restart fiddler-chatbot deployment.

OPTIONS:
    --no-cache, --disable-cache    Disable Docker build cache (rebuild all layers from scratch)
    -h, --help                     Show this help message

EXAMPLES:
    # Build with cache (default, faster builds)
    $0

    # Build without cache (clean rebuild)
    $0 --no-cache

    # Build without cache (alternative syntax)
    $0 --disable-cache

EOF
}

# Function to parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-cache|--disable-cache)
                DISABLE_CACHE=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# Main execution
main() {
    # Parse command line arguments
    parse_arguments "$@"

    log_info "Starting fiddler-chatbot build and deployment process..."
    if [ "$DISABLE_CACHE" = true ]; then
        log_info "Build cache: DISABLED (--no-cache)"
    else
        log_info "Build cache: ENABLED (default)"
    fi
    echo ""

    # Step 1: Check prerequisites
    check_prerequisites
    echo ""

    # Step 2: Authenticate to ECR
    authenticate_ecr
    echo ""

    # Step 3: Build Docker image
    build_image
    echo ""

    # Step 4: Tag image for ECR
    tag_image
    echo ""

    # Step 5: Push image to ECR
    push_image
    echo ""

    # Step 6: Configure kubectl
    configure_kubectl
    echo ""

    # Step 7: Restart deployment
    restart_deployment
    echo ""

    # Step 8: Show deployment status
    show_deployment_status
    echo ""

    log_success "Build and deployment process completed successfully!"
    log_info "Image: $ECR_REGISTRY/$IMAGE_NAME:$TAG"
    log_info "Namespace: $NAMESPACE"
    log_info "Cluster: $EKS_CLUSTER"
}

# Run main function
main "$@"
