# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# Page Configuration
st.set_page_config(
    page_title="Ecommerce Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Utilities
@st.cache_data
def load_data():
    df = pd.read_csv("data/ecommerce_transactions.csv", parse_dates=["purchase_date"])
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    return df

def load_image(folder, filename):
    return Image.open(os.path.join("assets", folder, filename))

# Load Data
df = load_data()

# Sidebar Navigation
st.sidebar.title("Ecommerce Analytics Modules")
selected = st.sidebar.radio("Navigate", [
    "KPI Dashboard",
    "A/B Testing (Single Run)",
    "A/B Testing (Simulation)",
    "Customer Segmentation",
    "Customer Lifetime Value (CLV) Modeling",
    "Sales Forecasting"
])

# KPI Dashboard
if selected == "KPI Dashboard":
    st.title("KPI Dashboard - Revenue & Performance Overview")
    st.markdown("Gain a high-level understanding of revenue, orders, and average value over a time period. Use the filters to drill into key trends.")
    st.markdown("---")

    date_range = st.date_input("Date Range", [df.purchase_date.min(), df.purchase_date.max()])
    if len(date_range) == 2:
        df = df[(df["purchase_date"] >= pd.to_datetime(date_range[0])) & (df["purchase_date"] <= pd.to_datetime(date_range[1]))]

    total_revenue = df['purchase_amount'].sum()
    total_orders = df.shape[0]
    avg_order_value = df['purchase_amount'].mean()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("Average Order Value", f"${avg_order_value:,.2f}")
    col3.metric("Total Orders", f"{total_orders:,}")

    st.markdown("### Revenue Over Time")
    timeseries = df.groupby("purchase_date")["purchase_amount"].sum().reset_index()
    fig = px.line(timeseries, x="purchase_date", y="purchase_amount", title="Daily Revenue", template="plotly_white")
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Visual Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.image(load_image("KPI_analysis", "payment_method_distribution.png"), caption="Payment Method Distribution")
        st.markdown("Diverse preferences—Crypto leads marginally, followed by Gift Cards and Credit/PayPal.")
        st.image(load_image("KPI_analysis", "distribution_of_purchase_amounts.png"), caption="Purchase Value Distribution")
        st.markdown("Heavy concentration under $100. High spikes indicate premium offerings or bulk buys.")
    with col2:
        st.image(load_image("KPI_analysis", "revenue_contribution_by_category.png"), caption="Revenue by Product Category")
        st.markdown("Beauty and Electronics dominate in both revenue and volume. Prioritize for upsell opportunities.")

# A/B Testing (Single Run)
elif selected == "A/B Testing (Single Run)":
    st.title("A/B Testing - One-Time Experiment")
    st.markdown("Measure effectiveness of a treatment using a controlled experiment.")
    st.markdown("---")
    st.image(load_image("ab_testing", "ab_single_run_conversion_rates.png"), caption="Group A vs B Conversion Rates")
    st.image(load_image("ab_testing", "ab_single_run_lift_by_category.png"), caption="Lift by Product Category")
    st.markdown("""
    **Summary:**
    - **Clothing, Electronics, Home Goods**: Significant lift and strong p-values — rollout recommended.
    - **Toys**: Negative lift. User journey friction suspected.
    - **Beauty**: Lift close to zero. No action recommended yet.

    **Recommendations:**
    - Scale the treatment for segments with robust improvement.
    - Reevaluate treatment's usability for Toys category.
    - Consider follow-up tests with new variants in the Beauty category.
    """)

# A/B Testing (Simulation)
elif selected == "A/B Testing (Simulation)":
    st.title("A/B Testing - Simulation Analysis")
    st.markdown("Explore experiment stability through 100 bootstrapped simulations.")
    st.markdown("---")
    st.image(load_image("ab_testing", "ab_simulation_lift_distribution.png"), caption="Lift Distribution (100 Simulations)")
    st.markdown("""
    **Insights:**
    - **Stable Gains**: Clothing & Electronics consistently positive — test is reproducible.
    - **Consistent Negative**: Toys show persistent negative lift across trials.
    - **Ambiguity**: Beauty's distribution is flat and wide — indicating high uncertainty.

    **Action Plan:**
    - Deploy on consistently high-lift categories.
    - Conduct qualitative follow-up with low-performing segments.
    - Use simulations to set expectations on performance variation.
    """)

# Customer Segmentation
elif selected == "Customer Segmentation":
    st.title("Customer Segmentation Analysis")
    st.markdown("Understand customer cohorts based on behavioral and monetary features.")
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.image(load_image("customer_analytics", "customer_segments_by_behavior_clusters.png"), caption="Customer Behavior Clusters")
    col2.image(load_image("customer_analytics", "pca_projection_of_customer_segments.png"), caption="PCA Cluster Projection")
    st.markdown("""
    **Segment Types:**
    - **High-Frequency, High-Spend**: Power users — ideal for loyalty programs.
    - **Low-Frequency, High-Spend**: Big-ticket buyers — focus on retention.
    - **Frequent Low-Spend**: Promote bundles.
    - **Dormant**: Target with reactivation offers.

    **Value:** Micro-segmentation allows for personalized engagement at scale.
    """)

# CLV Modeling
elif selected == "Customer Lifetime Value (CLV) Modeling":
    st.title("Customer Lifetime Value Modeling")
    st.markdown("Forecast long-term revenue contribution by user based on early signals.")
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.image(load_image("customer_analytics", "feature_importance_plot.png"), caption="CLV Feature Importance")
    col2.image(load_image("KPI_analysis", "total_spend_per_customer.png"), caption="Customer Spend Distribution")
    st.markdown("""
    **Key Findings:**
    - CLV is highly influenced by **avg. order value**, **recency**, and **order frequency**.
    - Spend is right-skewed — top 5% of customers drive a disproportionate share.

    **Strategic Levers:**
    - Focus ad targeting on early indicators of high CLV.
    - Reduce churn for mid-tier customers through proactive engagement.
    - Assign different retention budgets by segment.
    """)

# Sales Forecasting
elif selected == "Sales Forecasting":
    st.title("Sales Forecasting - Prophet Model")
    st.markdown("Predict daily ecommerce sales and identify trends, cycles, and outliers.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    col1.metric("MAE", "455.45")
    col2.metric("RMSE", "540.91")

    st.subheader("Time Series Overview")
    st.image(load_image("forecasting", "daily_total_sales_time_series.png"), caption="Daily Sales")
    st.markdown("Sales exhibit weekly cycles, seasonal promotions, and growth over time.")

    st.subheader("STL Decomposition")
    st.image(load_image("forecasting", "daily_total_sales_decomposition.png"), caption="Trend / Seasonality / Residual")
    st.markdown("Trend shows upward slope; seasonality aligns with holidays. Residuals reflect promotion timing.")

    st.subheader("Forecast Results")
    st.image(load_image("forecasting", "daily_sales_forecast_prophet.png"), caption="Forecast with Uncertainty Interval")
    st.markdown("""
    **Use Cases:**
    - Align supply chain planning with expected peaks
    - Adjust workforce allocation ahead of demand spikes
    - Detect anomalies by comparing actuals to forecast confidence band
    """)
