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