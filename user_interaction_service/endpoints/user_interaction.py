"""Handles endpoints for user interaction service"""
from starlette.requests import Request


class UserInteractionEndpoint:
    """endpoint class to handle user interaction services"""

    @classmethod
    async def add_like(cls, _: Request) -> None:
        """Handles add content like endpoint"""

        raise NotImplementedError()

    @classmethod
    async def add_read(cls, _: Request) -> None:
        """Handles add content read endpoint"""

        raise NotImplementedError()

    @classmethod
    async def fetch_like_and_read(cls, _: Request) -> None:
        """Handles read content read and like endpoint"""

        raise NotImplementedError()
