from fastapi import HTTPException


class AnalyticsError(HTTPException):
    def __init__(self, detail: str = "Analytics error", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class ShopNotFoundError(AnalyticsError):
    def __init__(self):
        super().__init__(detail="Shop not found", status_code=404)
