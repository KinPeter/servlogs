import asyncio
from fastapi import APIRouter, Depends, Request, WebSocket

from app.utils.auth import auth_user


router = APIRouter(
    prefix="/containers",
    tags=["containers"],
    dependencies=[Depends(auth_user)],
)


@router.get("/", summary="List all Docker containers")
async def list_containers(request: Request):
    """List all Docker containers."""
    containers = request.app.state.docker.containers.list(all=True)
    return [{"id": container.id, "name": container.name} for container in containers]


@router.websocket("/ws/logs/{container_name}")
async def websocket_logs(websocket: WebSocket, request: Request, container_name: str):
    await websocket.accept()
    try:
        container = request.app.state.docker.containers.get(container_name)
        # Stream logs (follow=True yields new log lines as they appear)
        log_stream = container.logs(stream=True, follow=True, tail=10)
        for log_line in log_stream:
            await websocket.send_text(log_line.decode("utf-8"))
            await asyncio.sleep(0)  # Yield control to event loop
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()
