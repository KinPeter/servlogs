# ServeLogs

A web-based tool for viewing and following Docker container logs in real time. It provides a simple, secure interface to list running containers, stream their logs live via WebSockets, and filter or tail log output directly from your browser.

## Features

- **List Docker containers**: View all Docker containers running on the server, including their names, IDs, and statuses.
- **Live log streaming**: Follow logs from any container in real time using WebSockets.
- **Log tailing**: Specify how many lines to tail and filter logs directly from the UI.
- **Secure API access**: Protected with API key authentication.
- **Simple web UI**: Lightweight, responsive interface built with vanilla HTML, CSS, and JavaScript.
- **Multi-platform support**: Easily run locally with Docker Compose or deploy to any Linux server.

## Technologies used

- Python with FastAPI
- Websockets
- Docker SDK
- Docker with Docker-compose
- Simple HTML, CSS and vanilla JS for UI

## Setup and run locally

1. Install Python 3.12.x and set up the virtual environment.

   ```bash
   pyenv install 3.12.10
   pyenv local 3.12.10
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables into the `.env` file.

   ```bash
   # API Key for authentication
   API_KEY=

   # Root path on the server where the script is running
   ROOT_PATH=
   ```

## API

Run in local:

```bash
fastapi dev api/main.py
```

Open your browser:

- Web app: `http://localhost:9999/`
- Api docs: `http://localhost:9999/docs`

Publish new docker image:

```bash
./deploy.sh
```
