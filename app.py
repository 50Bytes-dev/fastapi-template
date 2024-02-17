import contextlib
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from admin.main import create_admin_panel
from api.router import root
from config import get_settings
from core.minio_config import init_minio

settings = get_settings()


def create_app():
    @contextlib.asynccontextmanager
    async def lifespan(app):
        # Run at startup
        await init_minio()
        yield
        # Run at shutdown

    app = FastAPI(
        title="My API",
        version="0.0.1",
        debug=settings.DEBUG,
        routes=root.routes,
        lifespan=lifespan,
        middleware=[
            Middleware(
                SessionMiddleware,
                secret_key=settings.APP_SECRET_KEY,
            ),
            Middleware(
                CORSMiddleware,
                allow_origins=settings.ALLOW_ORIGINS,
                allow_origin_regex=settings.ALLOW_ORIGIN_REGEX,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
        ],
        docs_url="/docs" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
    )

    create_admin_panel(app)

    return app
