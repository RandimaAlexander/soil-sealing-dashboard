import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Soil Sealing Dashboard", layout="wide")

# ---------- CUSTOM SIDEBAR STYLE ---------
st.markdown("""
<style>

/* Sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1e293b);
}

/* Sidebar title */
[data-testid="stSidebar"] h2 {
    color: #f1f5f9;
    font-weight: 600;
}

/* Labels */
label {
    color: #cbd5f5 !important;
    font-size: 14px;
}

/* Dropdown + inputs */
.stSelectbox, .stSlider {
    background-color: #0f172a;
    border-radius: 10px;
    padding: 5px;
}

/* Selected box */
div[data-baseweb="select"] > div {
    background-color: #020617 !important;
    border-radius: 10px !important;
    border: 1px solid #334155 !important;
}

/* Slider color */
.stSlider > div > div > div > div {
    background-color: #3b82f6;
}

/* Divider */
hr {
    border: 1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
df = pd.read_csv("final_cleaned_soil_sealing.csv")

# ---------- HEADER ----------
st.title("🌍 Global Soil Sealing Dashboard")
st.markdown("""
This dashboard provides an interactive analysis of soil sealing across countries and regions.
It helps identify environmental impact, urban expansion patterns, and sustainability risks.
""")

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 🔎 Filters")
st.sidebar.markdown("---")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + list(df["Country"].unique())
)

region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(df["Region"].unique())
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Dashboard by Randima**")

# ---------- FILTER LOGIC ----------
filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country]

if region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region]

filtered_df = filtered_df[
    filtered_df["Year"].between(year_range[0], year_range[1])
]

# ---------- KPIs ----------
st.markdown("## 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

country_avg = filtered_df["Soil_Sealing"].mean()

global_avg = df[
    df["Year"].between(year_range[0], year_range[1])
]["Soil_Sealing"].mean()

diff_percent = ((country_avg - global_avg) / global_avg) * 100

col1.metric("Country Avg", f"{country_avg:.2f}")
col2.metric("Global Avg", f"{global_avg:.2f}")
col3.metric("Difference %", f"{diff_percent:.2f}%")

st.markdown("---")

# ---------- TREND + REGION ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Trend Over Time")
    st.markdown("This chart shows how soil sealing changes over time based on selected filters.")
    
    trend_data = filtered_df.groupby("Year")["Soil_Sealing"].mean().reset_index()
    fig_trend = px.line(trend_data, x="Year", y="Soil_Sealing")
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.markdown("### 🌍 Regional Comparison")
    st.markdown("This chart compares average soil sealing across regions.")

    region_data = df[df["Region"] != "EU Aggregate"]
    region_data = region_data.groupby("Region")["Soil_Sealing"].mean().reset_index()

    fig_bar = px.bar(
        region_data,
        x="Region",
        y="Soil_Sealing",
        color="Region"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ---------- GROWTH ----------
st.markdown("### 🚀 Top 10 Growth Countries")
st.markdown("This chart highlights countries with the highest growth rates.")

top_growth = df.sort_values(by="Growth_Rate", ascending=False).head(10)

fig_growth = px.bar(
    top_growth,
    x="Growth_Rate",
    y="Country",
    orientation="h",
    color="Growth_Rate",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_growth, use_container_width=True)

st.markdown("---")

# ---------- SCATTER ----------
st.markdown("### 🔍 Growth vs Soil Sealing")
st.markdown("This chart shows the relationship between growth rate and soil sealing.")

fig_scatter = px.scatter(
    df,
    x="Growth_Rate",
    y="Soil_Sealing",
    color="Region",
    size="Soil_Sealing",
    hover_name="Country"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ---------- DISTRIBUTION ----------
st.markdown("### 📊 Distribution")
st.markdown("This chart shows the distribution of soil sealing values.")

fig_hist = px.histogram(
    df,
    x="Soil_Sealing",
    nbins=30,
    color_discrete_sequence=["#2CA58D"]
)

st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# --------- INSIGHT ---------
if country != "All":
    insight = f"""
    {country} has an average soil sealing of {country_avg:.2f}, 
    which is {abs(diff_percent):.2f}% {'higher' if diff_percent > 0 else 'lower'} than the global average.

    This indicates {'higher urban pressure and environmental impact' if diff_percent > 0 else 'relatively lower environmental impact'}.
    """
else:
    insight = "Select a country to generate detailed insights."

st.success(insight)

st.markdown("---")

# ---------- DATA ----------
st.markdown("### 📄 Filtered Data")
st.dataframe(filtered_df)
