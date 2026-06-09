

import streamlit as st

import plotly.express as px

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Bird Species Observation Dashboard",
    page_icon="🦜",
    layout="wide"
)

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("cleaned_bird_data.csv")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

species = st.sidebar.selectbox(
    "Select Species",
    ["All"] + sorted(df["Common_Name"].unique().tolist())
)

selected_habitat = st.sidebar.multiselect(
    "Habitat",
    df["Location_Type"].unique(),
    default=df["Location_Type"].unique()
)

selected_season = st.sidebar.multiselect(
    "Season",
    df["Season"].unique(),
    default=df["Season"].unique()
)

# Apply Filters
filtered_df = df.copy()

if species != "All":
    filtered_df = filtered_df[
        filtered_df["Common_Name"] == species
    ]

filtered_df = filtered_df[
    filtered_df["Location_Type"].isin(selected_habitat)
]

filtered_df = filtered_df[
    filtered_df["Season"].isin(selected_season)
]

# -------------------------
# Title
# -------------------------
st.title("🦜 Bird Species Observation Dashboard")

st.markdown('''
Analyze bird observations, habitats,
environmental conditions and conservation insights.
''')

# -------------------------
# Download Button
# -------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "bird_analysis.csv",
    "text/csv"
)

# -------------------------
# KPI Cards
# -------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Observations",
    len(filtered_df)
)

col2.metric(
    "Species",
    filtered_df["Scientific_Name"].nunique()
)

col3.metric(
    "Habitats",
    filtered_df["Location_Type"].nunique()
)

col4.metric(
    "Observers",
    filtered_df["Observer"].nunique()
)

# -------------------------
# Dataset Preview
# -------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(), width="stretch")

# -------------------------
# Top Species
# -------------------------
st.subheader("Top 10 Bird Species")

top_species = (
    filtered_df["Common_Name"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_species.columns = [
    "Species",
    "Observations"
]

fig = px.bar(
    top_species,
    x="Observations",
    y="Species",
    orientation="h"
)

st.plotly_chart(fig, width="stretch")

# -------------------------
# Habitat Analysis
# -------------------------
st.subheader("Habitat Diversity")

habitat = (
    filtered_df
    .groupby("Location_Type")
    ["Scientific_Name"]
    .nunique()
    .reset_index()
)

fig = px.bar(
    habitat,
    x="Location_Type",
    y="Scientific_Name"
)

st.plotly_chart(fig, width="stretch")

# -------------------------
# Temperature Analysis
# -------------------------
st.subheader("Temperature vs Bird Count")

fig = px.scatter(
    filtered_df,
    x="Temperature",
    y="Initial_Three_Min_Cnt",
    color="Location_Type"
)

st.plotly_chart(fig, width="stretch")

# -------------------------
# Conservation Analysis
# -------------------------
st.subheader("Conservation Status")

watchlist = (
    filtered_df["PIF_Watchlist_Status"]
    .value_counts()
    .reset_index()
)

watchlist.columns = ["Status", "Count"]

fig = px.pie(
    watchlist,
    values="Count",
    names="Status"
)

st.plotly_chart(fig, width="stretch")

# -------------------------
# Monthly Trend
# -------------------------
st.subheader("Monthly Trend")

monthly = (
    filtered_df
    .groupby("Month")
    .size()
    .reset_index(name="Observations")
)

fig = px.line(
    monthly,
    x="Month",
    y="Observations",
    markers=True
)

st.plotly_chart(fig, width="stretch")

# -------------------------
# Footer
# -------------------------
st.markdown("---")

st.markdown('''
### Project Summary

✔ Species Diversity Analysis
✔ Habitat Comparison
✔ Environmental Analysis
✔ Conservation Monitoring
✔ Seasonal Trends

Built with Streamlit, Pandas and Plotly.
''')
