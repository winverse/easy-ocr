#!/bin/sh

docker stop pdf-to-text-docker-container
docker rm pdf-to-text-docker-container
docker rmi pdf-to-text-docker-image