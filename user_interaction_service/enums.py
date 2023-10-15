"""Handles enum related to user interation service"""
from enum import IntEnum


class OperationType(IntEnum):
    """User interaction operation type enum class"""

    READ = 0
    LIKE = 1
