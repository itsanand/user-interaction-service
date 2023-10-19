"""Handles database connection and tables"""
from sqlalchemy.engine.base import Engine
from sqlalchemy import (
    Column,
    String,
    Enum,
    PrimaryKeyConstraint,
    create_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
import user_interaction_service.settings as Config
from user_interaction_service.enums import OperationType

# Database Configuration
DB_ENGINE: Engine = create_engine(Config.DATABASE_URL)
BASE = declarative_base()
ASYNC_DB_ENGINE = create_async_engine(Config.ASYNC_DATABASE_URL)


# Define SQLAlchemy Models
class Interaction(BASE):  # type: ignore # pylint: disable=too-few-public-methods
    """User Interaction model"""

    __tablename__ = "Interaction"
    userID: Column = Column(String)
    contentTitle: Column = Column(String)
    operationType: Column = Column(Enum(OperationType))

    __table_args__ = (PrimaryKeyConstraint("userID", "contentTitle", "operationType"),)


if __name__ == "__main__":
    BASE.metadata.drop_all(DB_ENGINE)
    BASE.metadata.create_all(DB_ENGINE)
