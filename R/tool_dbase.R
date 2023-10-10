library(dbplyr)
library(DBI)
library(RMySQL)
# library(dplyr)
# library(Ipaper)
# library(data.table)
# library(tidymet)
# library(tidydb) # pak::pkg_install(c("rpkgs/tidydb", "rpkgs/tidymet"))

setMethod("dbSendQuery", c("MySQLConnection", "character"),
  function(conn, statement, ...) {
    RMySQL:::checkValid(conn)

    rsId <- .Call( RMySQL:::RS_MySQL_exec, conn@Id, as.character(statement))
    new("MySQLResult", Id = rsId)
  }
)

#' @import DBI dbplyr
#' @import RMySQL
open_mysql <- function(dbinfo, dbname=1) {
  if (is.numeric(dbname)) dbname = dbinfo$dbname[dbname]  
  bold(ok(sprintf("[info] opening db: %s", dbname)))

  dev = RMySQL::MySQL()
  # dev = odbc::odbc()
  # odbc::odbcListDrivers()
  # dev = RMariaDB::MariaDB()
  con <- dbConnect(dev, 
    # driver = "MySQL ODBC 8.1 ANSI Driver",
    host=dbinfo$host, 
    user=dbinfo$user, 
    password=as.character(dbinfo$pwd), 
    dbname = dbname)
  return(con)
}

open_mariadb <- function(dbinfo, dbname=1) {
  if (is.numeric(dbname)) dbname = dbinfo$dbname[dbname]  
  bold(ok(sprintf("[info] opening db: %s", dbname)))

  # dev = odbc::odbc()
  # odbc::odbcListDrivers()
  dev = RMariaDB::MariaDB()
  con <- dbConnect(dev, 
    host=dbinfo$host, 
    user=dbinfo$user, 
    password=as.character(dbinfo$pwd), 
    database = dbname, 
    dbname = dbname)
  
  str(dbGetInfo(con))
  return(con)
}


db_info <- function(con) {
  str(dbGetInfo(con))
}

# copy_to(con, st_met2481)
# `copy_to` not work for mysql
tbl_copy <- function(con, tbl, tbl_name = NULL, overwrite = TRUE, row.names=FALSE, ...) {
  if (is.null(tbl_name)) tbl_name = deparse(substitute(tbl))
  t = system.time({
    DBI::dbWriteTable(con, tbl_name, tbl, 
      overwrite = overwrite, row.names = row.names, ...)
  })
  print(t)

  cmd_encode = sprintf(
    "ALTER TABLE %s CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;", tbl_name)
  DBI::dbExecute(con, cmd_encode)
}

db_append <- function(con, tbl, values) {
  dbWriteTable(con, tbl, values, append = TRUE)
}


dbRemoveTables_like <- function(con, pattern="dbplyr", del=TRUE) {
  tbls_bad = dbListTables(con) %>% .[grep(pattern, .)]
  # print(tbls_bad)  
  if (del) {
    for (tbl_bad in tbls_bad) dbRemoveTable(con, tbl_bad)
  }
  tbls_bad
}
