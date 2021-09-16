
from collections import defaultdict
from contextlib2 import asynccontextmanager
from .patterns import var_pattern

def replacer(match):
    gd = match.groupdict()
    if gd["dblquote"] is not None:
        return gd["dblquote"]
    elif gd["quote"] is not None:
        return gd["quote"]
    else:
        return f'{gd["lead"]}:{gd["var_name"]}{gd["trail"]}'


def replace_sql_parameters(sql, parameters):
  for key in parameters:
    sql = sql.replace(":{}".format(key), str(parameters[key]))

  return sql


class AioBigQueryAdapter:
    is_aio_driver = True

    def __init__(self):
      self.var_sorted = defaultdict(list)

    def process_sql(self, _query_name, _op_type, sql):
      return var_pattern.sub(replacer, sql)

    async def select(self, conn, _query_name, sql, parameters, _record_class=None):
      sql = replace_sql_parameters(sql, parameters)
      return conn.query(sql)


    async def select_one(self, conn, _query_name, sql, parameters, record_class=None):
      # TODO
      sql = replace_sql_parameters(sql, parameters)
      return conn.query(sql)


    async def select_value(self, conn, _query_name, sql, parameters):
      # TODO
      sql = replace_sql_parameters(sql, parameters)
      return conn.query(sql)


    @asynccontextmanager
    async def select_cursor(self, conn, _query_name, sql, parameters):
      return {}


    async def insert_returning(self, conn, _query_name, sql, parameters):
      return {}

    async def insert_update_delete(self, conn, _query_name, sql, parameters):
      # TODO
      sql = replace_sql_parameters(sql, parameters)
      return conn.query(sql)


    async def insert_update_delete_many(self, conn, _query_name, sql, parameters):
      # TODO
      sql = replace_sql_parameters(sql, parameters)
      return conn.query(sql)


    async def execute_script(self, conn, sql):
      # TODO
      sql = replace_sql_parameters(sql)