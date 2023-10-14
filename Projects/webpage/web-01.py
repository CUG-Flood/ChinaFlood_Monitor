# %%
# 导入Streamlit库
from main_pkgs import *
import pandas as pd
import sqlite3
import streamlit as st
import os

st.set_page_config(layout="wide")

"""
> Dongdong Kong, CUG, 2023
"""
# # Streamlit应用程序的标题
# st.title("Hello, World!")

# # 在应用程序中显示文本
# st.write("这是一个简单的Streamlit示例，显示 'Hello, World!'")

# # 在应用程序中显示图像
# # st.image("https://www.streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png")

# # 在应用程序中添加交互元素（例如按钮）
# if st.button("点击我"):
#     st.write("你点击了按钮！")

"""
## 1. 查询数据
"""
# 在应用程序中添加用户输入
# user_input = st.text_input("请输入一些文本")
# st.write("你输入的文本是:", user_input)

# %%
print(os.getcwd())

# %%

# Execute a query to get column names
# %%

# query_table_columns(cursor, tbl)
# cursor.execute("PRAGMA table_info(%s)" % (tbl))  # 替换为您的表名
# column_info = cursor.fetchall()
# column_names = [info[1] for info in column_info]

# query = f"DESCRIBE {table_name}"

# cursor.execute(query)

# # columns = cursor.fetchall()
# columns, column_names
# query_table_columns(cursor, tbl)

# %%
# 添加站点列表啊
# stationInfo = pd.read_csv("data/st_met2481.csv")
# site = 59287

# %%
# cursor = db_open()
# tbl = "Met_hourly"
# site = 59287
uInfo = db_load_config()
dbinfo = uInfo['remote-nas']

con = db_open(dbinfo)
cursor = con.cursor()

stationInfo = query_data_site(cursor, "st_daily_met2481")
sites = stationInfo["site"].to_list()

"### 站点信息"
site = st.selectbox("请选择一个站点", sites, index=sites.index(sites[0]))
stationInfo[stationInfo.site == site]

"### 站点数据"
df = query_data_site(cursor, "China_Mete2000_daily_1951_2019", site)
df

"""
## 2. 绘图功能

> plotly

### 2.1 热浪

### 2.2 寒潮

"""

st.line_chart(
    df,
    x='date',
    y=["Tair_min"]
)
