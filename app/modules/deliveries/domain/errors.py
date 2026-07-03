from app.core.exceptions import AppException
from fastapi import status


class DeliveryNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Delivery not found", status.HTTP_404_NOT_FOUND)


class OrderAlreadyAssignedError(AppException):
    def __init__(self) -> None:
        super().__init__("This order is already assigned to a delivery person", status.HTTP_409_CONFLICT)


class NotAssignedToOrderError(AppException):
    def __init__(self) -> None:
        super().__init__("You are not assigned to this order", status.HTTP_403_FORBIDDEN)


class DeliveryProfileNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Delivery profile not found", status.HTTP_404_NOT_FOUND)


class DeliveryProfileAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__("Delivery profile already exists for this user", status.HTTP_409_CONFLICT)


class OrderGroupNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Order group not found", status.HTTP_404_NOT_FOUND)


class OrderGroupAlreadyAssignedError(AppException):
    def __init__(self) -> None:
        super().__init__("One or more orders in this group are already assigned", status.HTTP_409_CONFLICT)
