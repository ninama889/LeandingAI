import pandas as pd
import streamlit as st
import plotly.express as px
from windrose import WindroseAxes
from matplotlib import pyplot as plt

@st.cache_data
def load_data():
    data = pd.read_csv("C:/Users/NG/Desktop/streamlit/climate data.csv")
    wind_data = pd.read_csv("C:/Users/NG/Desktop/streamlit/Wind Data.csv")
    return data, wind_data


st.title("Climate Data Analysis")
st.markdown("This app analyzes hourly meteorological data from NASA POWER.")

data, wind_data = load_data()

# Data Cleaning
data.replace(-999, None, inplace=True)

# Sidebar filters
st.sidebar.header("Filters")
selected_Year = st.sidebar.multiselect(
    "Select Year", 
    options=sorted(data["YEAR"].unique()),  
    default=[int(data["YEAR"].max())]  
)
selected_Month = st.sidebar.multiselect(
    "Select Month", 
    options=sorted(data["MO"].unique()),  
    default=[int(data["MO"].max())]  
)
selected_day = st.sidebar.multiselect(
    "Select Day", 
    options=sorted(data["DY"].unique()),  
    default=[int(data["DY"].max())]  
)

selected_wind_speed = st.sidebar.slider(
    "Select Wind Speed Range (m/s)", 
    min_value=float(wind_data["VELOCIDAD"].min()), 
    max_value=float(wind_data["VELOCIDAD"].max()), 
    value=(float(wind_data["VELOCIDAD"].min()), float(wind_data["VELOCIDAD"].max()))
)
selected_direction = st.sidebar.multiselect(
    "Select Wind Direction", 
    options=sorted(wind_data["DIRECCION"].unique()), 
    default=sorted(wind_data["DIRECCION"].unique())
)

# Filter data
filtered_data = data[
    (data["DY"].isin(selected_day)) &
    (data["MO"].isin(selected_Month)) & 
    (data["YEAR"].isin(selected_Year))
]
filtered_wind_data = wind_data[
    (wind_data["VELOCIDAD"].between(*selected_wind_speed)) &
    (wind_data["DIRECCION"].isin(selected_direction))
]


st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Temp (°C)", round(filtered_data["T2M"].mean(), 2))
col2.metric("Max Temp (°C)", round(filtered_data["T2M"].max(), 2))
col3.metric("Avg Humidity (g/kg)", round(filtered_data["QV2M"].mean(), 2))
col4.metric("Avg Wind Speed (m/s)", round(filtered_data["WS10M"].mean(), 2))


st.write("### Hourly Temperature (T2M) Trend")
temp_fig = px.line(filtered_data, x="T2M", y="HR", markers=True,
                   labels={"T2M": "Temperature (°C)", "HR": "Hour"},
                   template="plotly")
st.plotly_chart(temp_fig, use_container_width=True)

st.write("### Specific Humidity (QV2M) Distribution")
humidity_fig = px.histogram(filtered_data, x="QV2M", nbins=10, color_discrete_sequence=["skyblue"],
                            labels={"QV2M": "Specific Humidity (g/kg)"},
                            template="plotly")
st.plotly_chart(humidity_fig, use_container_width=True)

st.write("### Precipitation vs Wind Speed")
scatter_fig = px.scatter(filtered_data, x="WS10M", y="PRECTOTCORR", color="HR", color_continuous_scale="Viridis",
                          labels={"WS10M": "Wind Speed (m/s)", "PRECTOTCORR": "Precipitation (mm/hour)", "HR": "Hour"},
                          template="plotly")
st.plotly_chart(scatter_fig, use_container_width=True)


st.write("### Windrose Plot (Matplotlib)")
fig = plt.figure(figsize=(5, 5))  
ax = WindroseAxes.from_ax(fig=fig)
ax.bar(filtered_wind_data["DIRECCION"], filtered_wind_data["VELOCIDAD"], normed=True, opening=0.8, edgecolor='white')
ax.set_legend(title="Wind Speed (m/s)")
plt.subplots_adjust(left=0.1, right=0.5, top=0.5, bottom=0.1) 
st.pyplot(fig)


st.write("### Interactive Windrose Plot")

windrose_data = (
    filtered_wind_data.groupby("DIRECCION", as_index=False)["VELOCIDAD"]
    .mean()
    .sort_values("DIRECCION")
)

plotly_fig = px.bar_polar(
    windrose_data,
    r="VELOCIDAD",
    theta="DIRECCION",
    color="VELOCIDAD",
    color_continuous_scale=px.colors.sequential.Viridis,
    labels={"VELOCIDAD": "Wind Speed (m/s)", "DIRECCION": "Wind Direction"},
    template="plotly"
)

plotly_fig.update_traces(
    hovertemplate="<b>Direction:</b> %{theta}°<br><b>Speed:</b> %{r} m/s",
    marker_line_color="white",  
    marker_line_width=1
)

plotly_fig.update_layout(
    polar=dict(
        radialaxis=dict(showgrid=True, ticksuffix=" m/s"), 
        angularaxis=dict(showgrid=True, direction="clockwise"),
    ),
    height=400,  
    width=400    
)

st.plotly_chart(plotly_fig, use_container_width=True)
