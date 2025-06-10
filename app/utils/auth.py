import os
from typing import Annotated
from fastapi import HTTPException, Security, status
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
