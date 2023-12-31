library(dbplyr)
library(DBI)
library(RMySQL)
library(crayon)
library(dplyr)
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
  bold(Ipaper::ok(sprintf("[info] opening db: %s", dbname)))

  dev = RMySQL::MySQL()
  # dev = odbc::odbc()
  # odbc::odbcListDrivers()
  port = 3306
  if (!is.null(dbinfo$port)) port = dbinfo$port

  con <- dbConnect(dev, 
    # driver = "MySQL ODBC 8.1 ANSI Driver",
    host=dbinfo$host, port = port,
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
  port = 3306
  if (!is.null(dbinfo$port)) port = dbinfo$port

  con <- dbConnect(dev, 
    load_data_local_infile = TRUE,
    host=dbinfo$host, port = port,
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


import_table_large <- function(df, table, chunksize=1e6) {
  n = nrow(df)
  # chunksize = 1e6
  chunks = ceiling(n/chunksize)
  fprintf("chunks = %d\n", chunks)

  for (i in 1:chunks) {
    fout = sprintf("%s_chunk%02d", table, i)
    ok(fprintf("running %s \n", fout))

    i_beg = (i-1)*chunksize + 1
    i_end = pmin(i*chunksize, n)
    d = df[i_beg:i_end, ]

    t = system.time({
      # if (i == 1) {
        copy_to(con, d, fout, overwrite = TRUE, temporary = FALSE)
      # } else {
      #   copy_to(con, d, table, append = TRUE, temporary = FALSE)
      # }
    })
    print(t)
  }
}
