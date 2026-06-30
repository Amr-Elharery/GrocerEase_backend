from pydantic import BaseModel
from typing import Dict, List, Optional


class OptimizeTripRequest(BaseModel):
    shopping_list: Dict[int, float]
    customer_address_id: int
    max_stores: int = 3


class LegResponse(BaseModel):
    from_location: str
    to_location: str
    distance_km: float


class RouteResponse(BaseModel):
    route: List[str]
    route_indices: List[int]
    legs: List[Dict]
    total_distance_meters: int
    total_distance_km: float
    estimated_cost: float
    num_stops: int


class ItemAssignmentResponse(BaseModel):
    store: str
    shop_id: int
    shop_product_id: Optional[int]
    price: float


class OptimizeTripResponse(BaseModel):
    stores_to_visit: List[str]
    item_assignment: Dict[int, ItemAssignmentResponse]
    item_cost: float
    delivery_cost: float
    total_cost: float
    route: RouteResponse
