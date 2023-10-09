import streamlit as st
import folium  # 用于创建地图
from streamlit_folium import folium_static  # 用于在Streamlit中显示Folium地图
import matplotlib.pyplot as plt  # 用于绘制图表

# 创建一个Streamlit应用
st.title('气象站地图与绘图')

# 创建一个Folium地图
m = folium.Map(location=[35, 100], zoom_start=10)

# 添加气象站标记到地图
weather_stations = [
    {"name": "站点1", "location": [15, 70]},
    {"name": "站点2", "location": [55, 140]},
    # 添加更多站点...
]

for station in weather_stations:
    folium.Marker(location=station["location"], popup=station["name"]).add_to(m)

# 在Streamlit中显示地图
folium_static(m)

# 创建绘图函数
def draw_chart(station_name):
    # 在这里执行绘图操作，使用Matplotlib或其他绘图库来绘制图表
    plt.figure(figsize=(8, 6))
    plt.title(f"站点 {station_name} 的图表")
    # 添加绘图逻辑
    # plt.plot(x_data, y_data)
    st.pyplot()

# 在Streamlit中添加选择站点和绘图功能
selected_station = st.selectbox("选择气象站", [station["name"] for station in weather_stations])
draw_button = st.button("绘制图表")

if draw_button:
    draw_chart(selected_station)
