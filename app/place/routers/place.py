from typing import Any, List

from app.place.models.place import Place
from app.place.views import places_view


async def setup(router):
  @router.get("/", response_model=List[Place], groups=['users', 'admins'])
  async def list_places(
    skip: int = 0,
    limit: int = 100
  ) -> Any:
    """
    Retrieve places from bigquery.
    """
    places = await places_view.get_places(limit, skip)
    return places
