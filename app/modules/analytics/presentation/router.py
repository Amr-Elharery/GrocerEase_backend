from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, require_roles, require_admin
from app.modules.analytics.presentation.controller import AnalyticsController
from app.modules.analytics.presentation.schemas import ShopDashboardResponse, AdminDashboardResponse
from app.modules.analytics.domain.errors import AnalyticsError, ShopNotFoundError

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/shop", response_model=ShopDashboardResponse, status_code=status.HTTP_200_OK)
async def get_shop_dashboard(
    controller: AnalyticsController = Depends(AnalyticsController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["vendor"])),
):
    try:
        owner_id = current_user.get("id")
        return await controller.get_shop_dashboard(owner_id)
    except ShopNotFoundError:
        raise
    except Exception as e:
        raise AnalyticsError(str(e))


@router.get("/admin", response_model=AdminDashboardResponse, status_code=status.HTTP_200_OK)
async def get_admin_dashboard(
    shops_by_area_limit: int = 10,
    shops_by_area_offset: int = 0,
    controller: AnalyticsController = Depends(AnalyticsController),
    _=Depends(require_admin),
):
    try:
        return await controller.get_admin_dashboard(shops_by_area_limit, shops_by_area_offset)
    except Exception as e:
        raise AnalyticsError(str(e))
