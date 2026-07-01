from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.modules.auth.presentation.router import router as auth_router
from app.modules.products.presentation.router import router as products_router
from app.modules.categories.presentation.router import router as categories_router
from app.modules.shops.presentation.router import router as shops_router
from app.modules.shop_products.presentation.router import router as shop_products_router
from app.modules.product_requests.presentation.router import router as product_requests_router
from app.modules.areas.presentation.router import router as areas_router
from app.modules.notifications.presentation.router import router as notifications_router
from app.modules.addresses.presentation.router import router as addresses_router
from app.modules.orders.presentation.router import router as orders_router
from app.modules.deliveries.presentation.router import router as deliveries_router
from app.modules.optimization.presentation.router import router as optimization_router
from app.modules.analytics.presentation.router import router as analytics_router
from app.modules.recommendations.presentation.router import router as recommendations_router
configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(products_router)
api_router.include_router(categories_router)
api_router.include_router(shops_router)
api_router.include_router(shop_products_router)
api_router.include_router(product_requests_router)
api_router.include_router(areas_router)
api_router.include_router(notifications_router)
api_router.include_router(addresses_router)
api_router.include_router(orders_router)
api_router.include_router(deliveries_router)
api_router.include_router(optimization_router)
api_router.include_router(analytics_router)
api_router.include_router(recommendations_router)
app.include_router(api_router)

@app.get("/", tags=["root"])
def root() -> dict:
    return {"message": f"Welcome to {settings.APP_NAME} !", "version": settings.APP_VERSION, "Environment": settings.APP_ENV}

@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok", "version": settings.APP_VERSION}


if __name__ == "__main__":
    import os
    os.system("fastapi dev")
