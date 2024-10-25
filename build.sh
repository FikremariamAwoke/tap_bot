#!/bin/bash
IMAGE_NAME=urkocoin-bot

# shellcheck disable=SC2181
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" != "" ]]; then
  echo "--> removing '$IMAGE_NAME'";
  docker image rm -f $IMAGE_NAME;
fi;

# Build the Docker image
docker build --no-cache -t $IMAGE_NAME .

# Run the Docker container
docker run -d --name urkocoin-bot-container --cap-add=SYS_ADMIN --restart=always $IMAGE_NAME
