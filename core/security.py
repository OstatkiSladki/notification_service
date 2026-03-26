from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

x_user_id_header = APIKeyHeader(name="X-User-ID", scheme_name="X-User-ID", auto_error=False)


def require_user_id(x_user_id: str | None = Security(x_user_id_header)) -> int:
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-ID header is required",
        )

    try:
        return int(x_user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="X-User-ID must be integer",
        ) from exc
