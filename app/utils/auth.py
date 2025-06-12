import os
from typing import Annotated
from fastapi import HTTPException, Security, WebSocket, WebSocketException, status
from fastapi.security import APIKeyHeader

from app.utils.logger import get_logger

api_key_header = APIKeyHeader(name="X-Api-Key", scheme_name="API Key", auto_error=True)


async def auth_user(
    api_key: Annotated[str, Security(api_key_header)],
):
    logger = get_logger()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication data. `X-Api-Key` is required in the headers.",
        )

    if api_key != os.getenv("API_KEY"):
        logger.warning(f"Unauthorized access attempt with API key: {api_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )

    return True


def auth_ws_user(websocket: WebSocket):
    api_key = websocket.query_params.get("api_key")
    logger = websocket.app.state.logger

    if websocket.client is None:
        logger.error("WebSocket connection failed: No client information available.")
        raise WebSocketException(
            code=status.HTTP_400_BAD_REQUEST,
            reason="WebSocket connection failed: No client information available.",
        )

    client_info = f"{websocket.client.host}:{websocket.client.port}"

    if not api_key:
        reason = "Missing authentication data. `api_key` is required in the query parameters."
        logger.warning(
            f"Unauthorized WebSocket access attempt from {client_info}: {reason}"
        )
        raise WebSocketException(
            code=status.HTTP_401_UNAUTHORIZED,
            reason=reason,
        )

    if api_key != os.getenv("API_KEY"):
        reason = "Invalid API key."
        logger.warning(
            f"Unauthorized WebSocket access attempt from {client_info}: {reason}"
        )
        raise WebSocketException(
            code=status.HTTP_401_UNAUTHORIZED,
            reason=reason,
        )

    logger.info(f"WebSocket authenticated for {client_info} with API key.")
    return True
