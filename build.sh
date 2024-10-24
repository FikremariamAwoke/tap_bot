#!/bin/bash

# Build the Docker image
docker build --no-cache -t urkocoin-bot3 .

# Run the Docker container
docker run -d --name urkocoin-bot-container urkocoin-bot
