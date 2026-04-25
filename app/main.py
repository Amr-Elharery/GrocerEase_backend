from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.modules.auth.presentation.router import router as auth_router
from app.modules.products.presentation.router import router as products_router


# Base.metadata.create_all(bind=engine)

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

app.include_router(auth_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")

@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok", "version": settings.APP_VERSION}
