import yaml
import pymysql
import os
import pandas as pd


def db_load_config(f = "env/db_userinfo.yml"):
  with open(f, 'r') as fid:
    uInfo = yaml.load(fid, Loader=yaml.FullLoader)
  return uInfo


def db_open(dbinfo=None, which_db=0):
  return pymysql.connect(
      host=dbinfo["host"],
      user=dbinfo["user"],
      port=dbinfo["port"],
      password=dbinfo["pwd"],
      database=dbinfo["dbname"][which_db]
    )


def query_table_columns(cursor, table_name):
  query = f"DESCRIBE {table_name}"
  cursor.execute(query)
  # Fetch the results
  column_names = [row[0] for row in cursor.fetchall()]
  return column_names


def query_data_site(cursor, tbl, site=None):
  """
  - `site`: integer, 站点编号
  - `tbl` : string, 数据库名
  """
  if site is None:
    sql = f"SELECT * FROM {tbl}"
  else:
    sql = "SELECT * FROM %s WHERE (`site` = %d)" % (tbl, site)

  cursor.execute(sql) 
  # 检索查询结果
  data = cursor.fetchall()
  vars = query_table_columns(cursor, tbl) # column names
  df = pd.DataFrame(data, columns=vars)
  return df



def hello():
  print("hello")
