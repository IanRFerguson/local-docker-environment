#!/bin/bash

# Pull down any existing container, compose it back up, and start interactive shell
echo "Stopping container..."
docker compose down > /dev/null 2>&1

echo "Restarting detached container..."
docker compose up -d  > /dev/null 2>&1

echo "Installing pygit2..."
docker compose exec local_parsons_dev pip install -r requirements.txt > /dev/null 2>&1

echo "Successfully started container!"