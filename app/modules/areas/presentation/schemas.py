from pydantic import BaseModel


class AreaResponse(BaseModel):
    id: int
    area_name: str
    city_name: str


class CreateAreaRequest(BaseModel):
    area_name: str
    city_name: str
