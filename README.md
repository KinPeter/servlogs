# ServeLogs

Describe the app here.

## Features

- **Some feature** Explain the feature.

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
