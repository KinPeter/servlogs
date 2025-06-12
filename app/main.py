import os
import docker
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from app.modules.containers import containers_router
from app.modules.ui import ui_router
from app.modules.websocket import websocket_router
from app.utils.logger import LoggingMiddleware, get_logger
from app.utils.version import get_version


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    docker_client = docker.from_env()
    app.state.docker = docker_client
    app.state.logger = get_logger()

    yield

    docker_client.close()


app = FastAPI(
    root_path=os.getenv("ROOT_PATH", ""),
    title="PK Server Logs API",
    lifespan=lifespan,
    version=get_version(),
    description="Read and follow Docker server logs",
)

app.add_middleware(LoggingMiddleware)

app.include_router(ui_router.router)
app.include_router(containers_router.router)
app.include_router(websocket_router.router)
