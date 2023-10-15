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

    def __init__(self, db_engine: AsyncEngine) -> None:
        self.async_session = sessionmaker(
            db_engine, class_=AsyncSession
        )  # type: ignore

    @classmethod
    async def user_exists(cls, user_id: str) -> bool:
        """check if user exists in user service repo"""

        async with AsyncClient(timeout=10.0) as client:
            url: str = f"{Config.USER_SERVICE_HOST}/user/{user_id}"
            user: Response = await client.get(url)
            return user.status_code != cls.NOT_FOUND

    async def add_content_like(self, user_id: str, title: str) -> None:
        """Create user interaction entry with like enum"""

        if not self.user_exists(user_id):
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
            except IntegrityError as error:
                await db_session.rollback()
            except Exception as error:
                db_session.rollback()
                raise error

    async def add_content_read(self, user_id: str, title: str) -> None:
        """Create user interaction entry with read enum"""

        if not self.user_exists(user_id):
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
            except IntegrityError as error:
                await db_session.rollback()
            except Exception as error:
                db_session.rollback()
                raise error

    async def read_like_and_read_service(
        self, title: str
    ) -> list[dict[str, int | str]]:
        """Read content based on the content title"""

        async with self.async_session() as db_session:  # type: ignore
            query = select(
                func.count()  # pylint: disable=not-callable
                .filter(
                    Interaction.contentTitle == title,
                    Interaction.operationType == OperationType.READ,
                )
                .label("reads"),
                func.count()  # pylint: disable=not-callable
                .filter(
                    Interaction.contentTitle == title,
                    Interaction.operationType == OperationType.LIKE,
                )
                .label("likes"),
            )
            interaction: Interaction = await db_session.execute(query)
            interaction_data = interaction.first()
            return {
                "title": title,
                "total_read": interaction_data.reads,  # type: ignore
                "total_like": interaction_data.likes,  # type: ignore
            }
