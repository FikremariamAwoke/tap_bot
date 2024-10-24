#!/bin/bash

# Build the Docker image
docker build --no-cache -t urkocoin-bot .

# Run the Docker container
docker run -d --name urkocoin-bot-container --cap-add=SYS_ADMIN urkocoin-bot

