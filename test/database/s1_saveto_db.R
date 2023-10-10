library(data.table)

f = "z:/DATA/China/ChinaMet_hourly_mete2000/data/China_Mete2000_daily_full_2020-2022_tidy.csv"
df = fread(f)

system.time({
  copy_to(con, df, "China_Mete2000_daily_2019_2022", overwrite = TRUE)
})

## 测试索引是否有效
