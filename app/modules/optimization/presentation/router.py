from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user, require_roles
from app.modules.optimization.presentation.controller import OptimizationController
from app.modules.optimization.presentation.schemas import OptimizeTripRequest, OptimizeTripResponse
from app.modules.optimization.domain.errors import OptimizationError, NoValidRouteError

router = APIRouter(prefix="/optimization", tags=["optimization"])


@router.post("/optimize", response_model=OptimizeTripResponse, status_code=status.HTTP_200_OK)
async def optimize_trip(
    payload: OptimizeTripRequest,
    controller: OptimizationController = Depends(OptimizationController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["customer"])),
):
    try:
        customer_id = current_user.get("id")
        return await controller.optimize_trip(payload, customer_id)
    except NoValidRouteError:
        raise
    except Exception as e:
        raise OptimizationError(str(e))
