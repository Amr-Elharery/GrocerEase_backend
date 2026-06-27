from pydantic import BaseModel
from typing import Optional


class AreaSummary(BaseModel):
    id: int
    area_name: str
    city_name: str


class CreateAddressRequest(BaseModel):
    area_id: int
    street: str
    building: str
    floor: str
    apt_number: str
    latitude: float
    longitude: float
    label: str
    additional_directions: Optional[str] = None


class UpdateAddressRequest(BaseModel):
    area_id: Optional[int] = None
    street: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[str] = None
    apt_number: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    label: Optional[str] = None
    additional_directions: Optional[str] = None


class AddressResponse(BaseModel):
    id: int
    user_id: str
    area_id: int
    street: str
    building: str
    floor: str
    apt_number: str
    latitude: float
    longitude: float
    label: str
    additional_directions: Optional[str] = None
    area: Optional[AreaSummary] = None
