# from app.user.routers import user, auth
from app.place.routers import place
from app.core.config import settings


async def api_router_setup(server):
  # server.auth.create_api_router(auth.router, tags=["auth"])
  # server.auth.create_api_router(user.router, tags=["users"])
  place_auth_router = server.auth.create_api_router(
    prefix=f"{settings.API_PREFIX}/places",
    tags=["places"]
  )

  # send auth routers to setup of each sub-module
  await place.setup(place_auth_router)