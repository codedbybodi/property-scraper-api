import streamlit as st
import requests
import pandas as pd

API_URL  = "https://property-scraper-api-production-2e19.up.railway.app"

st.set_page_config(page_title="🏠 PropIQ - Egyptian Property Market", layout="wide")
st.title("🏠 PropIQ - Egyptian Property Market Analyzer")
st.markdown("Real-time property data and AI-prowed market insights for Egypt")

# Sidebar filters
st.sidebar.header("🔍 Search Filters")

location = st.sidebar.text_input("Location", placeholder="e.g. New Cairo, New Zayed")
min_price = st.sidebar.number_input("Min Price (EGP)", min_value=0, value=0, step=100000)
max_price = st.sidebar.number_input("Max Price (EGP)", min_value=0, value=10000000, step=100000)
bedrooms = st.sidebar.selectbox("Bedrooms", [0, 1, 2, 3, 4, 5], index=0)

search = st.sidebar.button("🔍 Search Properties")

# Main Tabs
tab1, tab2, tab3 = st.tabs(["📋 Properties", "📊 Market Analysis", "🤖 AI Insights"])

# Tab 1: Properties
with tab1:
    params={}
    if location: params["location"] = location
    if min_price > 0: params["min_price"] = min_price
    if max_price < 10000000: params["max_price"] = max_price
    if bedrooms > 0: params["bedrooms"] = bedrooms

    try: 
        response = requests.get(f"{API_URL}/properties", params=params)
        if response.status_code != 200:
            st.error(f"API error {response.status_code}: {response.text}")
            st.stop()
        properties = response.json()

        if properties:
            st.success(f"Found {len(properties)} properties")

            # Show as Cards 
            cols = st.columns(3)
            for i, prop in enumerate(properties):
                price = prop.get("price")
                price_text = f"{price:,.0f} EGP" if price is not None else "N/A"
                area = prop.get("area_m2")
                area_text = f"{area:g}" if area is not None else "N/A"
                beds = prop.get("bedrooms")
                beds_text = beds if beds is not None else "N/A"
                with cols[i % 3]:
                    st.markdown(f""" 
                    <div style='border:1px solid #ddd; border-radius:10px; padding:15px; margin:5px; background:#f9f9f9;'>            
                        <h4 style='color:#111827;'>🏘️ {prop['title']} </h4>
                        <p style='color:#111827;'>💰 <b>{price_text}</b> </p>
                        <p style='color:#111827;'>📍 {prop['location']} </p>
                        <p style='color:#111827;'>🛏️ {beds_text} beds  Â· 🏠 {area_text} m²</p>
                        <p style='color:#111827;'>🏷️ {prop.get('property_type', 'N/A')} </p>
                    </div>
                    """, unsafe_allow_html=True)
        else: 
            st.warning("No Propeties found. Try different filters")
    except Exception as e:
        st.error(f"could not connect to API: {e}")

# Tab2: Market Analysis 
with tab2:
    st.subheader("📊 Market Statistics") 

    analysis_location = st.text_input("Analyze Location", placeholder="e.g. Cairo, or leave empty for all Egypt")
    analyze_btn = st.button("📊 Run Analysis")

    if analyze_btn:
        with st.spinner("Analyzing market data..."):
            try:
                params = {}
                if analysis_location:
                    params["location"] = analysis_location

                response = requests.get(f"{API_URL}/analyze", params=params)
                if response.status_code != 200:
                    st.error(f"API error {response.status_code}: {response.text}")
                    st.stop()
                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    # Metrics row
                    col1, col2, col3 , col4 = st.columns(4)
                    col1.metric("Total Listings", data["total_listings"])
                    col2.metric("Avg Price", f"{data['avg_price']:,.0f} EGP")
                    col3.metric("Avg Price/m²", f"{data['avg_price_per_m2']:,.0f} EGP")
                    col4.metric("Avg Area", f"{data['avg_area_m2']} m²")

                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Highest Price", f"{data['max_price']:,.0f} EGP")
                    with col2:
                        st.metric("Lowest Price", f"{data['min_price']:,.0f} EGP")
                    
                    #  Chart by property type
                    if data.get("avg_by_type"):
                        st.subheader("Averge price by Property Type")
                        chart_data = pd.DataFrame(
                            list(data["avg_by_type"].items()),
                            columns=["Type", "Avg Price (EGP)"]
                        )
                        st.bar_chart(chart_data.set_index("Type"))

            except Exception as e:
                st.error(f"Error: {e}")

# Tab3: AI Insights 
with tab3:
    st.subheader("🤖 AI Market Insights")
    st.markdown("Powered by Google Gemini - Analysis based or real property data")

    ai_location = st.text_input("Location for AI analysis", placeholder="e.g. Cairo")
    ai_btn = st.button("🤖 Generate AI Insights")

    if ai_btn:
        with st.spinner("Generating AI insights from real data..."):
            try:
                params = {}
                if ai_location:
                    params["location"] = ai_location

                response = requests.get(f"{API_URL}/analyze", params=params)
                if response.status_code != 200:
                    st.error(f"API error {response.status_code}: {response.text}")
                    st.stop()
                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.markdown(f"### 📍 Market Analysis: {data['location']}")
                    st.info(f"Based on **{data['total_listings']} real listings** with avg price of **{data['avg_price']:,.0f} EGP**")
                    st.markdown("---")
                    st.markdown(data['ai_analysis'])
            except Exception as e:
                st.error(f"Error: {e}")

# Footer 
st.markdown("---")
st.markdown("Built with FastAPI + PostgreSQL + Google Gemini AI | PropIQ 🏠")
