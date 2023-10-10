# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 00:18:42 2023

@author: 他也是周杰伦
"""
#%%将某一指定csv导入数据库
import pandas as pd
from sqlalchemy import create_engine

#腾讯云数据库
'''用单个文件测试
# CSV文件路径和表名
csv_file = 'C:\\Users\\18174\\Desktop\\mete2000\\mete2000_complete_2023-week09_[2023022600,2023030421].csv'
table_name = 'week09_2023'

# 创建MySQL数据库连接
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

# 读取CSV文件数据
df = pd.read_csv(csv_file)

# 将某一指定csv写入MySQL数据库表中
df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

# 关闭数据库连接
engine.dispose()
'''
#将指定 文件夹 的所有csv导入数据库
#将指定 文件夹 的所有csv导入数据库
#将指定 文件夹 的所有csv导入数据库

import os
import glob

# 创建MySQL数据库连接
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

# 获取CSV文件列表
csv_directory = 'C:/Users/18174/Desktop/mete2000/'
csv_files = glob.glob(csv_directory + '*.csv')
# 遍历所有CSV文件
for csv_file in csv_files:
    #获得每个文件的名字作为table name
    table_name = os.path.splitext(os.path.basename(csv_file))[0]
    # 读取CSV文件数据
    df = pd.read_csv(csv_file)
   
    # 将数据写入MySQL数据库表中
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

# 关闭数据库连接
engine.dispose()

#%%将数据库中每个table进行合并并生成union_table

# 构建包含所有表名的子查询
import pandas as pd
from sqlalchemy import create_engine

# MySQL数据库连接信息
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

# 获取所有表名
query = "SHOW TABLES"
df_tables = pd.read_sql_query(query, engine)

# 创建批量读取和插入的大小
batch_size = 5

# 执行查询和插入
for i in range(0, len(df_tables), batch_size):
    tables_batch = df_tables.iloc[i:i+batch_size]
    subqueries = []
    for table_name in tables_batch.iloc[:, 0]:
        subquery = f"(SELECT * FROM `{table_name}`)"
        subqueries.append(subquery)

    engine.execute("CREATE TABLE IF NOT EXISTS union_data (id INT PRIMARY KEY AUTO_INCREMENT)")
    union_query = " UNION ALL ".join(subqueries)
    query = f"INSERT INTO union_data SELECT * FROM ({union_query}) AS result"
    engine.execute(query)



# 关闭数据库连接
engine.dispose()

#%%

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')
#获取所有表名
query = "SHOW TABLES"
df_tables = pd.read_sql_query(query, engine)
print(df_tables)

#将所有表建立子查询
subqueries = []
for table_name in df_tables.iloc[:, 0]:
    subquery = f"(SELECT * FROM `{table_name}`)"
    subqueries.append(subquery)

# 构建UNION ALL查询
union_query = " UNION ALL ".join(subqueries)
print(union_query)

# 执行查询并获取结果
query = f"SELECT * FROM ({union_query}) AS result"#union all语句
df_result = pd.read_sql_query(query, engine)

# 输出结果
table_name = 'union_data'  # 替换为目标表名
df_result.to_sql(table_name, engine, if_exists='replace', index=False)  # 使用"replace"替换已存在的表
# 关闭数据库连接
engine.dispose()
#(SELECT * FROM `mete2000_complete_2023-week06_[2023021006,2023021121]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week07_[2023021200,2023021821]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week08_[2023021900,2023022521]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week09_[2023022600,2023030421]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week10_[2023030500,2023031121]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week11_[2023031200,2023031821]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week12_[2023031900,2023032521]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week13_[2023032600,2023040121]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week14_[2023040200,2023040821]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week15_[2023040900,2023041521]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week16_[2023041600,2023042221]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week17_[2023042300,2023042921]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week18_[2023043000,2023050621]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week19_[2023050700,2023051321]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week20_[2023051400,2023052006]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week21_[2023052100,2023052721]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week22_[2023052800,2023060321]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week23_[2023060400,2023061021]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week24_[2023061100,2023061721]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week25_[2023061800,2023062421]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week26_[2023062500,2023070121]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week27_[2023070200,2023070821]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week28_[2023070900,2023071521]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week29_[2023071600,2023072221]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week30_[2023072300,2023072921]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week33_[2023081300,2023081921]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week34_[2023082000,2023082621]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week35_[2023082700,2023090221]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week36_[2023090300,2023090921]`) UNION ALL (SELECT * FROM `mete2000_complete_2023-week37_[2023091000,2023091506]`) UNION ALL (SELECT * FROM `uniondata`)
