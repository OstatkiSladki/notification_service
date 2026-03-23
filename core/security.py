"""Security helpers for Notification Service."""

from fastapi import HTTPException, Request, status


def get_current_user_id(request: Request) -> int:
    """Extract current user id from request headers.

    Temporary local approach for integration until full auth middleware is wired.
    """
    x_user_id = request.headers.get("X-User-Id")
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    try:
        return int(x_user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-User-Id must be an integer",
        ) from exc
