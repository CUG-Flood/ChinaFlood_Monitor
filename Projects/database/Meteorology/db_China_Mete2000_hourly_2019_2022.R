library(Ipaper)
library(data.table)
devtools::load_all()

## 1. connect database
config = yaml::read_yaml("env/db_userinfo.yml")
dbinfo = config$nas
con_mysql = open_mysql(dbinfo, 1)
con_mariadb = open_mariadb(dbinfo, 1)
con = con_mariadb


## 2. write data
f = "Z:/DATA/China/ChinaMet_hourly_mete2000/data/China_Mete2000_hourly_full_2020-2022_tidy.fst"
df = import(f)

table = "China_Mete2000_hourly_2020_2022"
copy_to(con, df, table, overwrite = TRUE, temporary = FALSE)


table = "China_Mete2000_hourly_2020_2022"
import_table_large(df, table, chunksize=2e6)

## 测试索引是否有效
