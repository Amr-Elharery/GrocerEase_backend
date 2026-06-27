from app.core.exceptions import AppException
from fastapi import status


class AddressNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Address not found", status.HTTP_404_NOT_FOUND)


class AddressNotOwnedError(AppException):
    def __init__(self) -> None:
        super().__init__("You do not own this address", status.HTTP_403_FORBIDDEN)
