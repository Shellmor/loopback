from fastapi import FastAPI
from core.config import settings
from api.api_router import api_router
from core.middlewares import SQLAlchemyMiddleware
from core.logging import setup_logging


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/swagger_doc.json",
    docs_url="/api/swagger",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    redoc_url=None,
    on_startup=[setup_logging],
    debug=settings.DEBUG

)


app.include_router(api_router)
app.add_middleware(SQLAlchemyMiddleware)
