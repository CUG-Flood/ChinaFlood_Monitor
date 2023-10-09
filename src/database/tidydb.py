import yaml
import pymysql
import os

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
