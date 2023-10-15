"""Handles endpoints for user interaction service"""
from typing import Final
from httpx import ConnectError
from starlette.requests import Request
from starlette.responses import JSONResponse
from user_interaction_service.services.user_interaction import InteractionService
from user_interaction_service.models import ASYNC_DB_ENGINE
from user_interaction_service.exceptions import (
    UserDoesNotExistError,
    InvalidRequest,
    InternalCommunication,
)


class UserInteractionEndpoint:
    """endpoint class to handle user interaction services"""

    svc: InteractionService = InteractionService(ASYNC_DB_ENGINE)
    NOT_FOUND: Final[int] = 404
    CREATED: Final[int] = 201
    SUCCESS: Final[int] = 200
    INTERNAL_AUTH_VAL: Final[str] = "content"
    BAD_REQUEST: Final[int] = 404
    SERVER_ERROR: Final[int] = 500

    @classmethod
    async def add_like(cls, request: Request) -> JSONResponse:
        """Handles add content like endpoint"""

        try:
            title: str = request.path_params["title"]
            user_id: str = request.path_params["id"]
            await cls.svc.add_content_like(user_id, title)
            return JSONResponse(None, status_code=cls.CREATED)
        except ValueError:
            return JSONResponse(
                UserDoesNotExistError.error(), status_code=cls.NOT_FOUND
            )
        except KeyError:
            return JSONResponse(InvalidRequest.error(), status_code=cls.BAD_REQUEST)
        except ConnectError:
            return JSONResponse(
                InternalCommunication.error(), status_code=cls.SERVER_ERROR
            )

    @classmethod
    async def add_read(cls, request: Request) -> JSONResponse:
        """Handles add content read endpoint"""

        try:
            title: str = request.path_params["title"]
            user_id: str = request.path_params["id"]
            await cls.svc.add_content_read(user_id, title)
            return JSONResponse(None, status_code=cls.CREATED)
        except ValueError:
            return JSONResponse(
                UserDoesNotExistError.error(), status_code=cls.NOT_FOUND
            )
        except KeyError:
            return JSONResponse(InvalidRequest.error(), status_code=cls.BAD_REQUEST)
        except ConnectError:
            return JSONResponse(
                InternalCommunication.error(), status_code=cls.SERVER_ERROR
            )

    @classmethod
    async def fetch_like_and_read(cls, request: Request) -> JSONResponse:
        """Handles read content read and like endpoint"""

        try:
            page: str = request.query_params.get("page", "1")
            x_internal: str = request.headers["x-internal"]
            if x_internal != cls.INTERNAL_AUTH_VAL:
                raise KeyError
            data: list[dict[str, int | str]] = await cls.svc.read_like_and_read_service(
                int(page)
            )
            return JSONResponse(data, status_code=cls.SUCCESS)
        except KeyError:
            return JSONResponse(InvalidRequest.error(), status_code=cls.BAD_REQUEST)
