# Fiddler Chatbot Build and Deploy Script

This document explains how to use the `build-and-deploy.sh` script to build, tag, push, and deploy the fiddler-chatbot Docker image to AWS ECR and Kubernetes.

## Overview

The `build-and-deploy.sh` script automates the complete deployment pipeline for the fiddler-chatbot application:

1. **Build** - Creates a Docker image from the current codebase
2. **Tag** - Tags the image for AWS ECR
3. **Push** - Uploads the image to AWS ECR
4. **Deploy** - Restarts the Kubernetes deployment

## Prerequisites

Before running the script, ensure you have the following tools installed and configured:

### Required Tools
- **Docker** - For building and pushing images
- **AWS CLI** - For ECR authentication and EKS configuration
- **kubectl** - For Kubernetes deployment management

### AWS Configuration
- AWS CLI configured with appropriate credentials
- Access to the ECR registry: `079310353266.dkr.ecr.us-west-2.amazonaws.com`
- Access to the EKS cluster: `fdl-extqa`

### AWS Authentication (Required First Step)

Before running the build and deploy script, you **must** authenticate to the Fiddler AWS account using the company's authentication script:

```bash
fiddler/scripts/gsts/awslogin.sh <your-username>@fiddler.ai
```

Replace `<your-username>` with your actual Fiddler email username.

**Example:**
```bash
fiddler/scripts/gsts/awslogin.sh john.doe@fiddler.ai
```

This authentication step is **mandatory** and must be completed before running the build script.

### Kubernetes Access
- kubectl configured to access the `fdl-extqa` cluster
- Access to the `fiddler-chatbot` namespace

## Usage

### Step 1: AWS Authentication (Required)

First, authenticate to the Fiddler AWS account:

```bash
fiddler/scripts/gsts/awslogin.sh <your-username>@fiddler.ai
```

### Step 2: Run the Build Script

Run the script from the project root directory:

```bash
# Build with cache enabled (default, faster builds)
./build-and-deploy.sh

# Build without cache (clean rebuild, slower but ensures fresh layers)
./build-and-deploy.sh --no-cache
```

#### Command Line Options

- `--no-cache` or `--disable-cache` - Disables Docker build cache, forcing a complete rebuild of all layers from scratch
- `-h` or `--help` - Shows usage information and available options

### What the Script Does

The script follows this sequence:

1. **Argument Parsing** - Parses command line arguments (e.g., `--no-cache`)
2. **Prerequisites Check** - Verifies all required tools are available
3. **ECR Authentication** - Logs into AWS ECR using your AWS credentials
4. **Docker Build** - Builds the image with tag `fiddler-chatbot:latest` (with or without cache based on flags)
5. **Docker Tag** - Tags the image for ECR as `079310353266.dkr.ecr.us-west-2.amazonaws.com/fiddler-chatbot:latest`
6. **Docker Push** - Pushes the image to ECR
7. **Kubectl Configuration** - Ensures kubectl is configured for the `fdl-extqa` cluster
8. **Deployment Restart** - Restarts all deployments in the `fiddler-chatbot` namespace
9. **Status Check** - Waits for rollout completion and shows final status

## Docker Build Cache Control

By default, Docker caches intermediate layers during the build process to speed up subsequent builds. The script provides control over this behavior through command line arguments.

### Default Behavior (Cache Enabled)

When run without any flags, the script uses Docker's default caching behavior:

```bash
./build-and-deploy.sh
```

**Benefits:**
- Faster builds when dependencies haven't changed
- Reuses cached layers for unchanged parts of the Dockerfile
- Reduces build time and network usage

**How it works:**
- Docker caches each layer (RUN, COPY, etc.) based on the layer's content and the commands that created it
- If a layer's inputs haven't changed, Docker reuses the cached layer
- Only changed layers and subsequent layers are rebuilt

### Disabling Cache (Clean Rebuild)

To force a complete rebuild without using cached layers:

```bash
./build-and-deploy.sh --no-cache
# or
./build-and-deploy.sh --disable-cache
```

**When to use:**
- When you suspect cached layers may be causing issues
- When you want to ensure all dependencies are freshly downloaded
- When debugging build problems
- When base images or dependencies may have been updated externally

**Trade-offs:**
- Slower builds (all layers rebuilt from scratch)
- More network usage (dependencies re-downloaded)
- Ensures completely fresh build environment

### Cache Behavior Details

The Dockerfile is structured to maximize cache efficiency:

- **Early layers** (base image, OS packages) are cached and reused when unchanged
- **Dependency installation** (`pyproject.toml`, `uv.lock`) is cached separately from application code
- **Application code** (`COPY . .`) invalidates cache when any file changes

When cache is disabled (`--no-cache`), Docker will:
- Re-download base images
- Re-install all OS packages
- Re-install all Python dependencies
- Re-copy all application files

## Configuration

The script uses these default configuration values (defined at the top of the script):

```bash
ECR_REGISTRY="079310353266.dkr.ecr.us-west-2.amazonaws.com"
IMAGE_NAME="fiddler-chatbot"
TAG="latest"
NAMESPACE="fiddler-chatbot"
AWS_REGION="us-west-2"
EKS_CLUSTER="fdl-extqa"
DISABLE_CACHE=false  # Can be overridden via --no-cache flag
```

### Customizing Configuration

To modify these values, edit the configuration section at the top of the `build-and-deploy.sh` script:

```bash
# Configuration
ECR_REGISTRY="your-registry.dkr.ecr.region.amazonaws.com"
IMAGE_NAME="your-app-name"
TAG="your-tag"
NAMESPACE="your-namespace"
AWS_REGION="your-region"
EKS_CLUSTER="your-cluster"
```

## Environment Variables

The script does **not** handle environment variables or `.env` files. Environment variables must be managed separately through Kubernetes Secrets or ConfigMaps.

### How Environment Variables Are Managed

- **`.env` files are NOT copied into Docker images** - The `.dockerignore` file explicitly excludes `.env` and `.env.*` files from Docker builds
- **Environment variables are provided at runtime** via Kubernetes Secrets or ConfigMaps
- **The application uses `python-dotenv`** to load environment variables, but expects them to be available as environment variables in the container (not from a `.env` file in the image)

### Required Environment Variables

The application expects these environment variables:
- `FIDDLER_API_KEY` - Fiddler API key for authentication
- `OPENAI_API_KEY` - OpenAI API key for LLM access
- `FIDDLER_APP_ID` - Fiddler application ID (may be in config or env var)



## Output and Logging

The script provides colored output for better readability:

- 🔵 **[INFO]** - General information messages
- 🟢 **[SUCCESS]** - Successful operations
- 🟡 **[WARNING]** - Warning messages
- 🔴 **[ERROR]** - Error messages

### Example Output

**With cache enabled (default):**
```
[INFO] Starting fiddler-chatbot build and deployment process...
[INFO] Build cache: ENABLED (default)

[INFO] Checking prerequisites...
[SUCCESS] All prerequisites are available

[INFO] Authenticating to ECR...
[SUCCESS] Successfully authenticated to ECR

[INFO] Building Docker image...
[INFO] Docker build cache enabled (using cached intermediate layers)
[SUCCESS] Docker image built successfully
```

**With cache disabled (`--no-cache`):**
```
[INFO] Starting fiddler-chatbot build and deployment process...
[INFO] Build cache: DISABLED (--no-cache)

[INFO] Checking prerequisites...
[SUCCESS] All prerequisites are available

[INFO] Authenticating to ECR...
[SUCCESS] Successfully authenticated to ECR

[INFO] Building Docker image...
[INFO] Docker build cache disabled (--no-cache flag enabled)
[SUCCESS] Docker image built successfully

[INFO] Tagging image for ECR...
[SUCCESS] Image tagged as 079310353266.dkr.ecr.us-west-2.amazonaws.com/fiddler-chatbot:latest

[INFO] Pushing image to ECR...
[SUCCESS] Image pushed to ECR successfully

[INFO] Configuring kubectl for EKS cluster: fdl-extqa
[SUCCESS] kubectl configured for cluster: fdl-extqa

[INFO] Restarting deployment in namespace: fiddler-chatbot
[SUCCESS] Deployment restart initiated successfully
[SUCCESS] Deployment rollout completed successfully

[SUCCESS] Build and deployment process completed successfully!
```

## Error Handling

The script includes comprehensive error handling:

- **Exit on Error** - Script stops immediately if any step fails
- **Prerequisites Check** - Verifies all required tools are available before starting
- **AWS Authentication** - Validates ECR login success
- **Docker Operations** - Checks build, tag, and push success
- **Kubernetes Operations** - Validates namespace and deployment existence
- **Rollout Monitoring** - Waits for deployment completion with timeout

## Troubleshooting

### Common Issues

#### 1. AWS Authentication Failed
```
[ERROR] Failed to authenticate to ECR
```
**Solution**: Ensure you have authenticated to the Fiddler AWS account first:
```bash
# Step 1: Authenticate to Fiddler AWS account ( via alreadylocally set alias command in .bashrc)

awslogin

# Step 2: Verify authentication
aws sts get-caller-identity
```

#### 2. Docker Build Failed
```
[ERROR] Failed to build Docker image
```
**Solution**:
- Check Dockerfile syntax and ensure all required files are present
- Try building without cache to rule out cache-related issues: `./build-and-deploy.sh --no-cache`
- Verify Docker has sufficient disk space for the build

#### 3. ECR Push Failed
```
[ERROR] Failed to push image to ECR
```
**Solution**: Verify ECR repository exists and you have push permissions.

#### 4. Kubernetes Access Denied
```
[ERROR] Failed to configure kubectl for cluster: fdl-extqa
```
**Solution**: Ensure you have access to the EKS cluster:
```bash
aws eks update-kubeconfig --region us-west-2 --name fdl-extqa
```

#### 5. Namespace Not Found
```
[ERROR] Namespace 'fiddler-chatbot' does not exist
```
**Solution**: Create the namespace or update the script configuration:
```bash
kubectl create namespace fiddler-chatbot
```

### Debugging

To debug issues, you can run individual steps manually:

```bash
# Test ECR authentication
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 079310353266.dkr.ecr.us-west-2.amazonaws.com

# Test Docker build (with cache)
docker build -t fiddler-chatbot:latest .

# Test Docker build (without cache)
docker build --no-cache -t fiddler-chatbot:latest .

# Test kubectl access
kubectl get pods -n fiddler-chatbot
```

## Security Considerations

- **No Secrets in Build** - Environment variables are not passed during Docker build, and `.env` files are excluded from Docker images via `.dockerignore`
- **Kubernetes Secrets** - Sensitive data should be stored in Kubernetes Secrets, not in `.env` files committed to the repository
- **Runtime Configuration** - Environment variables are provided to containers via Kubernetes Secrets/ConfigMaps at runtime
- **ECR Security** - Uses AWS IAM for authentication
- **Kubernetes RBAC** - Relies on existing Kubernetes permissions

## Best Practices

1. **Test Locally** - Always test Docker builds locally before running the full script
2. **Use Cache for Development** - Use default caching behavior during development for faster iteration
3. **Disable Cache for Production** - Consider using `--no-cache` for production builds to ensure completely fresh dependencies
4. **Review Changes** - Check what files are being copied into the Docker image
5. **Monitor Deployments** - Watch the deployment status after script completion
6. **Backup Strategy** - Keep previous image versions in ECR for rollback capability
7. **Environment Separation** - Use different ECR repositories for different environments
8. **Cache Troubleshooting** - If builds behave unexpectedly, try `--no-cache` to rule out stale cache issues

## Support

If you encounter issues not covered in this documentation:

1. Check the script output for specific error messages
2. Verify all prerequisites are installed and configured
3. Test individual components (Docker, AWS CLI, kubectl) separately
4. Review AWS and Kubernetes permissions
5. Check the application logs in Kubernetes after deployment

## Script Location

The script is located at: `./build-and-deploy.sh`

Make sure to run it from the project root directory where the Dockerfile is located.
