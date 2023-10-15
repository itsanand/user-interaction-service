"""Handles user intercation services"""
from typing import Final
from httpx import AsyncClient, Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from user_interaction_service.models import Interaction
from user_interaction_service.enums import OperationType
import user_interaction_service.settings as Config


class InteractionService:
    """User interaction service class"""

    NOT_FOUND: Final[int] = 404
    DATA_PER_PAGE: Final[int] = 100
    INTERNAL_HEADERS: dict[str, str] = {
        "x-internal": "interaction",
    }

    def __init__(self, db_engine: AsyncEngine) -> None:
        self.async_session = sessionmaker(
            db_engine, class_=AsyncSession
        )  # type: ignore

    @classmethod
    async def user_exists(cls, user_id: str) -> bool:
        """check if user exists in user service repo"""

        async with AsyncClient(timeout=10.0) as client:
            url: str = f"{Config.USER_SERVICE_HOST}/user/{user_id}"
            user: Response = await client.get(url, headers=cls.INTERNAL_HEADERS)
            return user.status_code != cls.NOT_FOUND

    async def add_content_like(self, user_id: str, title: str) -> None:
        """Create user interaction entry with like enum"""

        if not await self.user_exists(user_id):
            raise ValueError
        async with self.async_session() as db_session:  # type: ignore
            try:
                interaction: Interaction = Interaction(
                    userID=user_id,
                    contentTitle=title,
                    operationType=OperationType.LIKE,
                )
                db_session.add(interaction)
                await db_session.commit()
            except IntegrityError:
                await db_session.rollback()
            except Exception as error:
                db_session.rollback()
                raise error

    async def add_content_read(self, user_id: str, title: str) -> None:
        """Create user interaction entry with read enum"""

        if not await self.user_exists(user_id):
            raise ValueError
        async with self.async_session() as db_session:  # type: ignore
            try:
                interaction: Interaction = Interaction(
                    userID=user_id,
                    contentTitle=title,
                    operationType=OperationType.READ,
                )
                db_session.add(interaction)
                await db_session.commit()
            except IntegrityError:
                await db_session.rollback()
            except Exception as error:
                db_session.rollback()
                raise error

    async def read_like_and_read_service(self, page: int) -> list[dict[str, int | str]]:
        """Read content based on the content title"""

        async with self.async_session() as db_session:  # type: ignore
            query = (
                select(
                    Interaction.contentTitle,
                    func.count()  # pylint: disable=not-callable
                    .filter(Interaction.operationType == OperationType.READ)
                    .label("reads"),
                    func.count()  # pylint: disable=not-callable
                    .filter(Interaction.operationType == OperationType.LIKE)
                    .label("likes"),
                )
                .group_by(Interaction.contentTitle)
                .order_by(
                    func.count()  # pylint: disable=not-callable
                    .filter(Interaction.operationType == OperationType.LIKE)
                    .desc(),
                    func.count()  # pylint: disable=not-callable
                    .filter(Interaction.operationType == OperationType.READ)
                    .desc(),
                )
                .offset((page - 1) * self.DATA_PER_PAGE)
                .limit(page * self.DATA_PER_PAGE)
            )
            interaction: Interaction = await db_session.execute(query)
            interaction_data = interaction.all()
            return [
                {
                    "title": interaction.contentTitle,
                    "totalReads": interaction.reads,  # type: ignore
                    "totalLikes": interaction.likes,  # type: ignore
                }
                for interaction in interaction_data
            ]
