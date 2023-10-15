"""Handles user service related exception"""
from typing import Union


class UserDoesNotExistError:  # pylint: disable=too-few-public-methods
    """class for user does not exist error"""

    @staticmethod
    def error() -> dict[str, Union[str, int]]:
        """user does not exist payload"""

        return {"code": 404, "error": "User not Found"}


class InvalidRequest:  # pylint: disable=too-few-public-methods
    """class for invalid request data error"""

    @staticmethod
    def error() -> dict[str, Union[str, int]]:
        """invalid request data error"""

        return {"code": 400, "error": "Invalid request data"}
