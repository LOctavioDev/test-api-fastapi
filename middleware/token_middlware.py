from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
from utils.jwt_config import validate_token
import json

EXCLUDED_PATHS = [
    "/auth/login",
    "/auth/register",
    "/users",
    "/docs",
    "/redoc",
    "/openapi.json",
]


class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if any(request.url.path.startswith(path) for path in EXCLUDED_PATHS):
                return await call_next(request)

            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return Response(
                    content=json.dumps({"detail": "Token missing or invalid"}),
                    status_code=401,
                    media_type="application/json",
                )

            token = auth_header.split(" ")[1]
            validate_token(token)

            return await call_next(request)

        except HTTPException as e:
            return Response(
                content=json.dumps({"detail": e.detail}),
                status_code=e.status_code,
                media_type="application/json",
            )
        except Exception:
            return Response(
                content=json.dumps({"detail": "Internal server error"}),
                status_code=500,
                media_type="application/json",
            )
