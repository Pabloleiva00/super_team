from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Callable


class PermissionMiddleware(BaseHTTPMiddleware):
    
    def __init__(self, app: Callable):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get('Authorization')
        
        # Agregar la lógica de verificación de si la token es correcta y no ha vencido

        response = await call_next(request)
        return response
