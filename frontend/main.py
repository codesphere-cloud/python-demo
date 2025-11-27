import os
import streamlit as st
import pandas as pd
import numpy as np
import requests

API_URL = f"http://ws-server-{os.getenv('WORKSPACE_ID', 123456)}-backend.workspaces:3000/api/data"

st.set_page_config(
    page_title="Porsche Demo",
    page_icon="🎉",
    layout="wide"
)

st.sidebar.header("Settings")
st.sidebar.write("Use the controls to steer the app.")

num_points = st.sidebar.slider(
    label="Number of data points:",
    min_value=10,
    max_value=100,
    value=30,
    step=5
)

chart_type = st.sidebar.selectbox(
    label="Select a chart type:",
    options=["Line Chart", "Bar Chart", "Area Chart"]
)

@st.cache_data 
def fetch_data(url: str, points: int):
    try:
        response = requests.get(url, params={"points": points}, timeout=3)
        response.raise_for_status() 
        
        data = response.json()      
        return pd.DataFrame(data['data'], columns=data['columns'], index=data['index'])

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from API: {e}")
        return pd.DataFrame()


st.header(f"Mein neues {chart_type}")
st.write(f"Displaying a chart with {num_points} random data points.")


chart_data = fetch_data(API_URL, num_points)

if chart_type == "Line Chart":
    st.line_chart(chart_data)
elif chart_type == "Bar Chart":
    st.bar_chart(chart_data)
elif chart_type == "Area Chart":
    st.area_chart(chart_data)

def calculate_summary_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {'mean_A': 0, 'max_B': 0, 'total_points': 0}
    
    stats = {
        'mean_A': df['A'].mean(),
        'max_B': df['B'].max(),
        'total_points': len(df)
    }
    return stats

st.divider() 
st.subheader("Summary Statistics")

if not chart_data.empty:
    summary = calculate_summary_stats(chart_data)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Points", summary['total_points'])
    col2.metric("Mean of Column A", f"{summary['mean_A']:.2f}")
    col3.metric("Max of Column B", f"{summary['max_B']:.2f}")
else:
    st.warning("No data available to calculate statistics.")


if st.checkbox("Show raw chart data"):
    st.subheader("Raw Data")
    st.write(chart_data)

if __name__ == "__main__":
  pass
