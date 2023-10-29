#!/bin/bash

# Check if Docker is installed and running
if ! command -v docker &> /dev/null || ! docker info &> /dev/null; then
  echo "Docker is not installed or not running. Please install and start Docker before running this script."
  exit 1
fi

# Define the Docker image name and app port
IMAGE_NAME="backend_docker"
APP_PORT=4999

# Check if the Docker image already exists
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]] || [ "$1" == "--rebuild" ]; then
  # Build the Docker image if it doesn't exist or the rebuild flag is provided
  docker build -t $IMAGE_NAME .
fi

# Check if a container with the same name is already running
if [[ "$(docker ps -q -f name=$IMAGE_NAME)" != "" ]]; then
  # Stop the existing container
  docker stop $IMAGE_NAME
fi

# Remove the existing container
if [[ "$(docker ps -aq -f name=$IMAGE_NAME)" != "" ]]; then
  docker rm $IMAGE_NAME
fi

# Run the Docker container
docker run -d -p $APP_PORT:5000 $IMAGE_NAME

# Provide instructions to access the app
echo "Flask app is running. You can access it at http://localhost:$APP_PORT"
