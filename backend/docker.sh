#!/bin/bash

# Function to display usage
show_usage() {
    echo "Usage: $0 [up|down|build|restart]"
    echo "  up      - Start the container"
    echo "  down    - Stop and remove the container"
    echo "  build   - Build the Docker image"
    echo "  restart - Rebuild and restart the container"
}

# Function to build the image
build_image() {
    echo "Building Docker image..."
    DOCKER_BUILDKIT=0 docker build --progress=plain -t baseapi:latest .
}

# Function to start the container
start_container() {
    echo "Starting container..."
    docker run -d \
        --name baseapi \
        -p 80:80 \
        -v $(pwd):/app \
        --env-file .env \
        --log-driver=json-file \
        --log-opt mode=non-blocking \
        --log-opt max-buffer-size=25m \
        baseapi:latest
}

# Function to stop and remove the container
stop_container() {
    echo "Stopping and removing container..."
    docker stop baseapi 2>/dev/null || true
    docker rm baseapi 2>/dev/null || true
}

# Function to show logs
show_logs() {
    echo "Container logs:"
    docker logs baseapi
}

# Main script logic
case "$1" in
    "up")
        start_container
        show_logs
        ;;
    "down")
        stop_container
        ;;
    "build")
        build_image
        ;;
    "restart")
        stop_container
        build_image
        start_container
        show_logs
        ;;
    *)
        show_usage
        exit 1
        ;;
esac

exit 0 