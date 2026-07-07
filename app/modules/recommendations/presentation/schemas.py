from pydantic import BaseModel, Field
from typing import List
from datetime import date


class ProductRecommendation(BaseModel):
    product_id: int
    name: str
    brand: str | None = None
    category: str | None = None
    image_url: str | None = None
    # Price/availability are only populated for shop-aware.
    price: float | None = None
    shop_product_id: int | None = None
    available_stock: int | None = None
    score: float
    pair_count: int | None = None
    lift: float | None = None


class ReplenishmentRecommendation(BaseModel):
    product_id: int
    name: str
    brand: str | None = None
    category: str | None = None
    image_url: str | None = None
    rebuy_probability: float
    rank: int
    prediction_date: date
    model_version: str


class CartCompletionRequest(BaseModel):
    # Catalog product ids currently in the cart (pair stats are catalog-level).
    product_ids: List[int] = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=50)
