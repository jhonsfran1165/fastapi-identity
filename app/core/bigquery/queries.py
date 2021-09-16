import pathlib
import aiosql
from app.core.bigquery import AioBigQueryAdapter


def get_queries(file: str, path: str = "sql"):
  queries = aiosql.from_path(
    pathlib.Path(file).parent / path,
    AioBigQueryAdapter
  )

  return queries