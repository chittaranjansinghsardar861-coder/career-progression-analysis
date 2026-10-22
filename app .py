import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Career Trajectory Intelligence", layout="wide")

st.title("Career Progression and Promotion Gap Analysis Dashboard")
st.subheader("Palo Alto Networks - Retention Optimization Intelligence")

# Load Dataset
@st.cache_data
def load_data():
    return pd.read_csv('processed_hr_data.csv')

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")
dept_filter = st.sidebar.multiselect("Select Department", df['Department'].unique(), default=df['Department'].unique())
promo_gap_threshold = st.sidebar.slider("Promotion Gap Threshold (Years)", 0, 15, 3)

filtered_df = df[(df['Department'].isin(dept_filter)) & (df['YearsSinceLastPromotion'] >= promo_gap_threshold)]

# Module 1: Career Path Clustering Dashboard
st.header("1. Career Path Clustering Dashboard")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cluster Distribution")
    fig1 = px.pie(filtered_df, names='ClusterLabel', title="Distribution of Career Trajectories")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Promotion Gap vs. Role Stagnation")
    fig2 = px.scatter(
        filtered_df, 
        x='YearsSinceLastPromotion', 
        y='YearsInCurrentRole', 
        color='ClusterLabel',
        hover_data=['JobRole', 'Department']
    )
    st.plotly_chart(fig2, use_container_width=True)

# Module 2: Promotion Gap Monitor & Intervention Panel
st.header("2. Promotion Gap Monitor & Intervention Panel")
st.dataframe(filtered_df[['Department', 'JobRole', 'YearsAtCompany', 'YearsSinceLastPromotion', 'ClusterLabel']])

st.success("Targeted Intervention: Focus career development plans and mentorship programs on employees with a promotion gap exceeding your selected threshold.")