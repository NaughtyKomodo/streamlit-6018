import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set Page Config (Consistent & Professional Theme)
st.set_page_config(page_title="2026 Data Insights Storytelling", layout="wide")

# Inject Custom CSS for Premium iOS-like Glassmorphism Metrics
st.markdown("""
    <style>
    /* Dashboard Dark Background */
    .stApp {
        background: linear-gradient(135deg, #141824 0%, #0b0d13 100%) !important;
    }
    
    /* iOS Glassmorphic Containers specifically for top KPI Cards only */
    div[data-testid="stMetricBlock"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) saturate(130%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(130%) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 16px !important;
        padding: 16px 24px !important;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4) !important;
    }

    /* Fixed Plotly container pointer events to allow ZOOMING & HOVERING */
    div.stElementContainer:has(div.stPlotlyChart) {
        pointer-events: auto !important;
        margin-bottom: 40px !important;
    }
    
    /* Elegant Headers Typography */
    h1, h3, .stMarkdown p {
        color: #f8f9fa !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    h3 {
        font-weight: 500 !important;
        letter-spacing: -0.3px;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 The 2026 Data Insights & Storytelling Challenge")
st.markdown("### Analyzing the Impact of Social Media on Student Mental Health")
st.write("---")

# Load Cleaned Data
@st.cache_data
def get_dashboard_data():
    df = pd.read_csv("Cleaned_Student_Social_Media_And_Mental_Health_Impact.csv")
    return df

df = get_dashboard_data()

# ----------------- FILTERS (Requirement 3b - At least 2 filters) -----------------
st.sidebar.header("Dashboard Navigation Filters")
selected_gender = st.sidebar.multiselect("Select Gender:", options=df['Gender'].unique(), default=df['Gender'].unique())
selected_platform = st.sidebar.multiselect("Select Primary Platform:", options=df['Most_Used_Platform'].unique(), default=df['Most_Used_Platform'].unique())

# Apply Filters
df_filtered = df[(df['Gender'].isin(selected_gender)) & (df['Most_Used_Platform'].isin(selected_platform))]

# KPI Cards / Metrics Summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("Filtered Respondents", f"{len(df_filtered)} Students")
col2.metric("Avg Daily Screen Time", f"{df_filtered['Avg_Daily_Usage_Hours'].mean():.1f} Hrs")
col3.metric("Avg Mental Health Score", f"{df_filtered['Mental_Health_Score'].mean():.1f}/10")
col4.metric("Avg Sleep Duration", f"{df_filtered['Sleep_Hours_Per_Night'].mean():.1f} Hrs")

st.write("---")

# ----------------- VERTICAL VISUAL VARIETY (No Side-by-Side Columns) -----------------

# 1. Heatmap (Full Width)
st.subheader("1. Stress Distribution Density by Platform")
fig1 = px.density_heatmap(df_filtered, x="Most_Used_Platform", y="Stress_Level", 
                         category_orders={"Stress_Level": ["Low", "Medium", "High", "Very High"]},
                         color_continuous_scale="Viridis", text_auto=True)
fig1.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font_color="#e0e0e0", xaxis_title="Most Used Platform", yaxis_title="Stress Level",
    xaxis=dict(tickangle=45, tickmode='linear'),
    height=500 # Taller frame for vertical stack
)
st.plotly_chart(fig1, use_container_width=True)

# 2. Scatter Plot with Trendline (Full Width)
st.subheader("2. Correlation: Screen Time vs Mental Health Score")
fig2 = px.scatter(df_filtered, x="Avg_Daily_Usage_Hours", y="Mental_Health_Score", 
                  color="Stress_Level", hover_data=["Age", "Academic_Level"],
                  color_discrete_sequence=px.colors.qualitative.Safe, trendline="ols")
fig2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font_color="#e0e0e0", xaxis_title="Average Daily Usage (Hours)", yaxis_title="Mental Health Score",
    height=500
)
st.plotly_chart(fig2, use_container_width=True)

# 3. Dual-Axis Line Chart (Full Width)
st.subheader("3. Time-Series: Academic Focus & Sleep Trends")
df_trend = df_filtered.groupby('Survey_Day').agg({'Study_Hours':'mean', 'Sleep_Hours_Per_Night':'mean'}).reset_index()

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df_trend['Survey_Day'], y=df_trend['Study_Hours'], name="Study Hours (Left)", mode='lines+markers'))
fig3.add_trace(go.Scatter(x=df_trend['Survey_Day'], y=df_trend['Sleep_Hours_Per_Night'], name="Sleep Hours (Right)", mode='lines+markers', yaxis="y2"))

fig3.update_layout(
    xaxis_title="Survey Timeline (Days)",
    yaxis=dict(title="Study Hours", gridcolor="rgba(255,255,255,0.05)"),
    yaxis2=dict(title="Sleep Hours", overlaying="y", side="right", gridcolor="rgba(255,255,255,0.05)"),
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font_color="#e0e0e0",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=500
)
st.plotly_chart(fig3, use_container_width=True)

# 4. Geospatial Map / Choropleth (Full Width)
st.subheader("4. Geospatial Mapping of Mental Health Scores")
df_geo = df_filtered.groupby('Country')['Mental_Health_Score'].mean().reset_index()
fig4 = px.choropleth(df_geo, locations="Country", locationmode="country names",
                     color="Mental_Health_Score", color_continuous_scale="Plasma")
fig4.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font_color="#e0e0e0", 
    coloraxis_colorbar=dict(title="Avg Score"),
    height=600,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular',
        bgcolor='rgba(0,0,0,0)',
        landcolor='rgba(255, 255, 255, 0.03)',
        lakecolor='rgba(0,0,0,0)'
    )
)
st.plotly_chart(fig4, use_container_width=True)