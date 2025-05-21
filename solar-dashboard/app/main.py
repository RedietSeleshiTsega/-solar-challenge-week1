import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data, get_region_stats


st.set_page_config(
    page_title="West Africa Solar Potential",
    page_icon="☀️",
    layout="wide"
)

@st.cache_data
def load_cached_data():
    return load_data()

df = load_cached_data()
region_stats = get_region_stats(df)

st.sidebar.header("Dashboard Controls")
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

selected_metric = st.sidebar.selectbox(
    "Select Solar Metric",
    options=['GHI', 'DNI', 'DHI'],
    index=0
)

show_regions = st.sidebar.checkbox("Show Top Regions Table", value=True)

st.title("☀️ West Africa Solar Potential Dashboard")
st.markdown("Compare solar energy potential across Benin, Sierra Leone, and Togo")

st.header("Country Comparison")
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader(f"{selected_metric} Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=df[df['Country'].isin(selected_countries)],
        x='Country',
        y=selected_metric,
        ax=ax
    )
    ax.set_ylabel(f"{selected_metric} (kWh/m²/day)")
    st.pyplot(fig)

with col2:
    st.subheader("Summary Statistics")
    stats = df[df['Country'].isin(selected_countries)]
    stats = stats.groupby('Country')[selected_metric].describe()
    st.dataframe(stats.style.format("{:.2f}"))

if show_regions:
    st.header("Top Regions by Solar Potential")
    filtered_regions = region_stats[region_stats['Country'].isin(selected_countries)]
    st.dataframe(
        filtered_regions.head(10),
        column_config={
            "GHI": st.column_config.NumberColumn(format="%.2f kWh/m²/day"),
            "DNI": st.column_config.NumberColumn(format="%.2f kWh/m²/day"),
            "DHI": st.column_config.NumberColumn(format="%.2f kWh/m²/day")
        },
        hide_index=True
    )

st.sidebar.markdown("---")
st.sidebar.info(
    "ℹ️ Select countries and metrics to update visualizations. "
    "Data shows daily solar irradiance values."
)
