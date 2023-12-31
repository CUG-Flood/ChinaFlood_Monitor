import yaml
import pymysql
import os
import pandas as pd

print(os.getcwd())


def db_load_config(f = "env/db_userinfo.yml"):
  with open(f, 'r') as fid:
    uInfo = yaml.load(fid, Loader=yaml.FullLoader)
  return uInfo


def db_open(dbinfo=None, which_db=0):
  if dbinfo is None:
    INFO = db_load_config()
    dbinfo = INFO["Kong"]
    # dbinfo = INFO["JiaYing"]  
  return pymysql.connect(
      host=dbinfo["host"],
      user=dbinfo["user"],
      password=dbinfo["pwd"],
      database=dbinfo["dbname"][which_db]
    )



def query_data_site(cursor, tbl, site):
  """
  - `site`: integer, 站点编号
  - `tbl` : string, 数据库名
  """
  cursor.execute("SELECT * FROM %s WHERE (`Station_Id_C` = %d)" % (tbl, site))
  # 检索查询结果
  data = cursor.fetchall()
  vars = query_table_columns(cursor, tbl)  # column names
  df = pd.DataFrame(data, columns=vars)
  return df
