from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from app.application.exceptions.user_already_exists_exception import UserAlreadyExistsException


class ExceptionHandlingMiddleware:
    async def __call__(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            print("I've been called! , ", type(e) is UserAlreadyExistsException)
            return JSONResponse(
                status_code=400,
                content={"message": "HI"},
            )
