library(Ipaper)
library(RMySQL)
library(dplyr)

config <- yaml::read_yaml("env/db_userinfo.yml")
dbinfo <- config$JiaYing
dbinfo <- config$Kong

con <- open_mysql(dbinfo, 1)
con

# temp = mtcars
copy_to(con, mtcars, "mtcars", overwrite = TRUE)
table = tbl(con, "mtcars")
data = collect(table)[1:10, ]

## 之后应该删除临时表格
rows_append(table, data, copy=TRUE, in_place = TRUE)
dbRemoveTables_like(con, "dbplyr")
