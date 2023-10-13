# Developing Parsons Locally with Docker
This repo provides a template to develop Parsons connectors locally in a container environment, similar to Civis / Prefect / other orchestration platforms.

## Prerequisites

* Your local development repo should be at the same directory level as Parsons
* You can confirm this by running the `bash` test below, or you can update the pathing in `docker_compose.yml`

```bash
if test -d ../parsons; then
    echo "Local pathing is setup properly";
else
    echo "Error - the relative path to Parsons is misconfigured";
fi
```

* You should install Docker on your machine
  * [Install Docker desktop](https://www.docker.com) - It's a good idea to sign up for a free account here as well!
  * [Install the Docker CLI via Homebrew](https://formulae.brew.sh/formula/docker)

You can check to see if everything is installed correctly by running the following `bash` commands:

```bash
# Open the Docker Desktop app
open -a Docker

# Check for running containers via Docker CLI
docker ps
```

## Running Docker
You can run the following `bash` commands *from this directory* (or wherever your `docker_compose.yml` file is located). Just make sure that Docker desktop is running!

```bash
# Start the container live in your terminal
# NOTE - You'll need to run commands from another terminal window
docker compose up

# Alternatively, you can start the container and have it running in the background (or "detach" it)
docker compose up -d

# If you want to trigger a full rebuild of the image you can add a --build flag on to the end
docker compose up -d --build

# When you want to pull the container down 
docker compose down
```

## Docker Compose
