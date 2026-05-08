import streamlit as st
from data_processor import load_data, compute_kpis
from agent import ask_llm
import matplotlib.pyplot as plt
 
# Page config
st.set_page_config(
    page_title="KPI Investigation Agent",
    layout="wide"
)
 
# Title
st.title("🚀 KPI Investigation Agent")
 
# Load Data Button
if st.button("Load Data"):
    df = load_data()
    st.session_state["df"] = df
 
# If data is loaded
if "df" in st.session_state:
    df = st.session_state["df"]
    kpis = compute_kpis(df)
 
    # ===== KPI CARDS =====
    st.subheader("📊 Key Metrics")
 
    col1, col2, col3 = st.columns(3)
 
    with col1:
        st.metric("Total Trips", len(df))
 
    with col2:
        st.metric("Avg Fare", round(kpis["avg_fare"], 2))
 
    with col3:
        st.metric("Unique Zones", df["Zone"].nunique())
 
    # ===== CHARTS =====
    col1, col2 = st.columns(2)
 
    with col1:
        st.subheader("📈 Trip Volume Trend")
        #st.line_chart(kpis["daily_trips"])
        daily_trips = kpis["daily_trips"]
        daily_trips = daily_trips.sort_values("pickup_date")
 
        st.line_chart(
            daily_trips,
            x="pickup_date",
            y="trip_count"
        )
 
    with col2:
        st.subheader("💰 Average Fare")
        st.metric("Avg Fare", round(kpis["avg_fare"], 2))
 
    # Trips by Hour
    st.subheader("⏰ Peak Demand Hours")
    trips_by_hour=kpis["trips_by_hour"]
    st.bar_chart(trips_by_hour,
                 x="pickup_hour",
                 y="trip_count"
                 )
 
    # Top Zones
    st.subheader("📍 Top Pickup Zones")
    top_zones = kpis["top_zones"].sort_values("trip_count",ascending=False)
    
    fig,ax=plt.subplots(figsize=(8,5))

    ax.barh(top_zones["Zone"],top_zones["trip_count"])
 
    ax.set_xlabel("Trip Count")
    ax.set_ylabel("Zone")
    ax.set_title("Top Pickup Zones")
    
    st.pyplot(fig)
    
 
    # ===== Agent ANALYSIS =====
    st.subheader("🤖 AI Analysis")
 
    if st.button("Analyze KPIs with Agent"):
 
        summary = {
            "recent_trip_trend": kpis["daily_trips"].tail(7).to_dict(),
            "average_fare": float(kpis["avg_fare"]),
            "top_zones": kpis["top_zones"].to_dict(),
            "peak_hours": kpis["trips_by_hour"].sort_values(by="trip_count",ascending=False).head(5).to_dict()
        }
 
        prompt = f"""
        Here is KPI data from a taxi business:
 
        {summary}
 
        Analyze:
        1. Key trends
        2. Any anomalies
        3. Possible reasons
        4. Business recommendations
 
        Be specific and avoid generic statements.
        """
 
        with st.spinner("Agent is analyzing..."):
            response = ask_llm(prompt)
 
        st.subheader("📊 Agent Insights")
        st.write(response)
 
    # ===== DATASET INFO =====
    st.subheader("📂 Dataset Overview")
    st.write("Rows, Columns:", df.shape)
 
    # Debug view (optional)
    with st.expander("🔍 View Sample Data"):
        st.dataframe(df.head(50))