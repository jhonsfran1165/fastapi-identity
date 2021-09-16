from fastapi import FastAPI
from loguru import logger
from easyauth.server import EasyAuthServer

# from app.api.errors.http_error import http_error_handler
# from app.api.errors.validation_error import http422_error_handler
from app.api.api_v1.api import api_router_setup
from app.core.config import settings
# from app.db.session import init_db


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION
    )

    return application


server = get_application()

@server.on_event("shutdown")
async def on_shutdown():
    logger.info("Shotdown api")


@server.on_event('startup')
async def startup():
    logger.info("Starting api")

    server.auth = await EasyAuthServer.create(
        server,
        "/auth/token",
        logger = logger,
        auth_secret = settings.SECRET_KEY,
        admin_title = settings.PROJECT_NAME,
        admin_prefix = "/admin"
    )

    await api_router_setup(server)
