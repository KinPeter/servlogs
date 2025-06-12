import asyncio
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from app.utils.auth import auth_ws_user
from app.utils.logger import get_logger

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
)


@router.websocket("/logs/{container_id}")
async def websocket_logs(websocket: WebSocket, container_id: str):
    logger = websocket.app.state.logger
    auth_ws_user(websocket)

    await websocket.accept()
    if websocket.client is None:
        logger.error("WebSocket connection failed: No client information available.")
        await websocket.close()
        return

    logger.info(
        f"WebSocket connection established for {websocket.client.host}:{websocket.client.port} to container {container_id[0:12]}..."
    )

    tail = int(websocket.query_params.get("tail", "100"))
    container = websocket.app.state.docker.containers.get(container_id)
    log_stream = container.logs(stream=True, follow=True, timestamps=True, tail=tail)

    queue = asyncio.Queue()

    loop = asyncio.get_running_loop()  # Get the main event loop

    # Producer: runs in a thread, puts log lines into the queue
    def log_producer(loop):
        try:
            for log_line in log_stream:
                asyncio.run_coroutine_threadsafe(queue.put(log_line), loop)
        except Exception as e:
            logger.error(f"Log producer error: {e}")

    producer_thread = asyncio.to_thread(log_producer, loop)
    producer_task = asyncio.create_task(producer_thread)

    try:
        while True:
            # Wait for either a log line or a client message
            done, pending = await asyncio.wait(
                [
                    asyncio.create_task(queue.get()),
                    asyncio.create_task(websocket.receive_text()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in done:
                if task is not None and not task.cancelled():
                    result = task.result()
                    # If result is a log line, send it
                    if isinstance(result, bytes) or isinstance(result, str):
                        await websocket.send_text(
                            result.decode("utf-8")
                            if isinstance(result, bytes)
                            else result
                        )
                    else:
                        # Received a message from the client (could be ping, close, etc.)
                        pass

            # Cancel any pending tasks to avoid warnings
            for task in pending:
                task.cancel()

    except WebSocketDisconnect:
        logger.info(
            f"WebSocket disconnected: {websocket.client.host}:{websocket.client.port}"
        )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        try:
            await websocket.send_text(f"Error: {str(e)}")
        except Exception:
            pass
    finally:
        producer_task.cancel()
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()
        logger.info(
            f"WebSocket connection closed for {websocket.client.host}:{websocket.client.port} to container {container_id[0:12]}"
        )
        log_stream.close()
