# -*- coding: utf-8 -*-
# %%
# https://stackoverflow.com/questions/1907993/autoreload-of-modules-in-ipython
%load_ext autoreload
%autoreload 2
# %reload_ext autoreload
from tidydb import *

# %%
INFO = db_load_config()
dbinfo = INFO["Kong"]
# dbinfo = INFO["JiaYing"]
con = db_open(dbinfo)
con

# %%
"""
Created on Sat Sep 16 00:20:27 2023

@author: 他也是周杰伦
"""
import streamlit as st
import pymysql
import pandas as pd
st.set_page_config(layout="wide")
# 得到数据库数据
def connectsql(sitenumber):
    cursor = con.cursor()
    # 执行 SQL 查询语句
    sql = "SELECT * FROM mt_data.union_data WHERE Station_Id_C = %s"  # 使用%s作为占位符
    cursor.execute(sql, (str(sitenumber),))  
    results = cursor.fetchall()# 获取查询结果
    column_names = [desc[0] for desc in cursor.description]#获取列名
    return results, column_names

# 利用站点信息表格实现名称到编号
# data = pd.read_csv("C:\\Users\\18174\\Desktop\\output.csv")
column1 = data["site"].tolist()
column2 = data["name"].tolist()
data_dict = dict(zip(column1, column2))
st.title("站点信息查询")
selected_option = st.selectbox("选择一个选项", column2)# 创建下拉选择框
sitenumber = [key for key, value in data_dict.items() if value == selected_option]
sitenumber=', '.join(str(x) for x in sitenumber)

#查询界面
if sitenumber:
    results, column_names = connectsql(str(sitenumber))     
    if results:
        df = pd.DataFrame(results, columns=column_names)
        st.table(df)
    else:
        st.write("查询结果为空")
else:
    st.write("请输入站点编号")



#%%热浪分析
import plotly.graph_objects as go
