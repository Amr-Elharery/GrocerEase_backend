from fastapi import APIRouter, Depends, Query, status
from typing import List
from app.core.dependencies import get_current_user
from app.modules.recommendations.presentation.controller import RecommendationsController
from app.modules.recommendations.presentation.schemas import (
    CartCompletionRequest,
    ProductRecommendation,
    ReplenishmentRecommendation,
)
from app.modules.recommendations.domain.errors import RecommendationsError

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get(
    "/products/{product_id}/frequently-bought-together",
    response_model=List[ProductRecommendation],
    status_code=status.HTTP_200_OK,
)
async def frequently_bought_together_global(
    product_id: int,
    limit: int = Query(10, ge=1, le=50),
    controller: RecommendationsController = Depends(RecommendationsController),
    _=Depends(get_current_user),
):
    """Catalog product page, no store selected: related products without price
    or availability."""
    try:
        return await controller.frequently_bought_together_global(product_id, limit)
    except Exception as e:
        raise RecommendationsError(str(e))


@router.get(
    "/shops/{shop_id}/products/{product_id}/frequently-bought-together",
    response_model=List[ProductRecommendation],
    status_code=status.HTTP_200_OK,
)
async def frequently_bought_together_shop(
    shop_id: int,
    product_id: int,
    limit: int = Query(10, ge=1, le=50),
    controller: RecommendationsController = Depends(RecommendationsController),
    _=Depends(get_current_user),
):
    """Product page inside a store: only items the store carries and has in
    stock, with that store's price."""
    try:
        return await controller.frequently_bought_together_shop(shop_id, product_id, limit)
    except Exception as e:
        raise RecommendationsError(str(e))


@router.post(
    "/shops/{shop_id}/cart/completion",
    response_model=List[ProductRecommendation],
    status_code=status.HTTP_200_OK,
)
async def cart_completion_shop(
    shop_id: int,
    payload: CartCompletionRequest,
    controller: RecommendationsController = Depends(RecommendationsController),
    _=Depends(get_current_user),
):
    """Cart completion inside a store: candidates limited to that store's
    in-stock products."""
    try:
        return await controller.cart_completion_shop(shop_id, payload.product_ids, payload.limit)
    except Exception as e:
        raise RecommendationsError(str(e))


@router.get(
    "/replenishment",
    response_model=List[ReplenishmentRecommendation],
    status_code=status.HTTP_200_OK,
)
async def replenishment(
    limit: int = Query(10, ge=1, le=50),
    controller: RecommendationsController = Depends(RecommendationsController),
    current_user=Depends(get_current_user),
):
    """Home page, cross-shop: products the current user is predicted to rebuy.
    The user is taken from the JWT, not from the path."""
    try:
        user_id = current_user.get("id")
        return await controller.replenishment(user_id, limit)
    except Exception as e:
        raise RecommendationsError(str(e))
