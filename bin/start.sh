#!/bin/bash

# Start docker container
docker compose down && docker compose up -d

# Install pygit2
docker compose exec local_parsons_dev pip install pygit2