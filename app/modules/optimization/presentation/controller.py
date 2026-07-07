from fastapi import Depends
from app.modules.optimization.application.services.optimization_service import OptimizationService
from app.modules.optimization.presentation.schemas import OptimizeTripRequest, OptimizeTripResponse


class OptimizationController:
    def __init__(self, service: OptimizationService = Depends(OptimizationService)) -> None:
        self.service = service

    async def optimize_trip(self, payload: OptimizeTripRequest, customer_id: str) -> OptimizeTripResponse:
        try:
            return await self.service.optimize_trip(
                shopping_list=payload.shopping_list,
                customer_address_id=payload.customer_address_id,
                customer_id=customer_id,
                max_stores=payload.max_stores,
            )
        except Exception as e:
            raise e
