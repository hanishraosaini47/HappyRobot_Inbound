"""API key authentication dependency."""

import secrets

from fastapi import Header, HTTPException, status

from app.config import settings


async def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Reject any request that does not include a matching X-API-Key header.

    Uses constant-time comparison to prevent timing attacks.
    """
    if not x_api_key or not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
