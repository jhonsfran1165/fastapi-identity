import json

from typing import List
from loguru import logger

from app.place.queries import queries
from app.core.bigquery import bigquery
# from app.place.models.place import Place


class PlaceView():

  @logger.catch
  async def get_places(self, limit: int, skip: int) -> List[object]:
    query_job = await queries.get_places(bigquery.client, limit=limit, offset=skip)
    df = query_job.to_dataframe()
    result = json.loads(df.to_json(orient='records'))
    return result

    # I can format the response
    # places = []

    # for place in result:
    #   places.append(Place(**place))

    # return places

places_view = PlaceView()