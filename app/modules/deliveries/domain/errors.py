from app.core.exceptions import AppException
from fastapi import status


class DeliveryAssignmentNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Delivery assignment not found", status.HTTP_404_NOT_FOUND)


class OrderAlreadyAssignedError(AppException):
    def __init__(self) -> None:
        super().__init__("This order is already assigned to a delivery person", status.HTTP_409_CONFLICT)


class NotAssignedToOrderError(AppException):
    def __init__(self) -> None:
        super().__init__("You are not assigned to this order", status.HTTP_403_FORBIDDEN)
