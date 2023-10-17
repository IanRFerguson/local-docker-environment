#!/bin/bash

# Pull down any existing container, compose it back up, and start interactive shell
docker compose down &&
docker compose up -d &&
docker compose exec local_parsons_dev pip install pygit2