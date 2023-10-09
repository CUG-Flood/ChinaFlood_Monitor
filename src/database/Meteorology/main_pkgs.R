library(dbplyr)
library(DBI)
library(dplyr)
library(Ipaper)
# library(data.table)
# library(tidymet)
# library(tidydb) # pak::pkg_install(c("rpkgs/tidydb", "rpkgs/tidymet"))

db_open <- function(dbinfo, dbname=1) {
  if (is.numeric(dbname)) dbname = dbinfo$dbname[dbname]  
  bold(ok(sprintf("[info] opening db: %s", dbname)))

  con <- dbConnect(RMySQL::MySQL(), 
    host=dbinfo$host, 
    user=dbinfo$user, 
    password=as.character(dbinfo$pwd), 
    dbname=dbname)
  return(con)
}

# copy_to(con, st_met2481)
# `copy_to` not work for mysql
tbl_copy <- function(con, tbl, tbl_name = NULL, overwrite = TRUE) {
  if (is.null(tbl_name)) tbl_name = deparse(substitute(tbl))
  DBI::dbWriteTable(con, tbl_name, tbl, overwrite = overwrite)
}
