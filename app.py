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
    st.markdown("""
    This module provides a concise overview of ecommerce KPIs including total revenue, order volume, and purchase behavior over time. These metrics help frame financial performance and support daily operations or stakeholder reporting.
    """)
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
        st.markdown("""
        Crypto currently leads all other payment methods in frequency of use, suggesting customer preference for decentralized or alternative currencies. Meanwhile, gift cards and PayPal are nearly equal, with usage of credit cards slightly lower. Consider adjusting checkout UI to prioritize most-used methods.
        """)
        st.markdown("\n\n")
        st.image(load_image("KPI_analysis", "distribution_of_purchase_amounts.png"), caption="Purchase Value Distribution")
        st.markdown("""
        Purchases are heavily skewed toward lower values. Most transactions cluster below $50. While this ensures volume, it limits per-order profit. Promotional strategies or bundling discounts may increase order value and improve gross margin.
        """)
    with col2:
        st.image(load_image("KPI_analysis", "revenue_contribution_by_category.png"), caption="Revenue by Product Category")
        st.markdown("""
        Beauty, Electronics, and Clothing make up a majority of total revenue. These categories demonstrate healthy margins and traction. Recommendations include:
        - Personalizing email flows for beauty product buyers.
        - Bundling accessories in electronics.
        - Creating urgency for clothing through time-based sales.

        Segmenting campaigns by product category can improve targeting precision and boost ROI by tailoring incentives and messaging.
        """)

# A/B Testing (Single Run)
elif selected == "A/B Testing (Single Run)":
    st.title("A/B Testing (Single Experiment Analysis)")
    st.markdown("""
    In this module, we explore the results of a single controlled A/B test conducted across multiple product categories. The goal was to measure the effectiveness of a new feature or campaign variant on conversion rates. By comparing Group A (control) and Group B (treatment), we identify statistical lift and category-specific impact.

    **Why this matters:** A/B testing allows data-driven decisions when deploying new features. Understanding how users respond in different segments helps minimize risk and optimize rollout.
    """)
    st.markdown("---")

    st.image(load_image("ab_testing", "ab_single_run_conversion_rates.png"), caption="Conversion Rates by Group")
    st.markdown("""
    This bar chart illustrates the raw conversion rates observed in each product category for Group A and Group B. Early indicators suggest significant improvements in conversion rates for select categories under the treatment condition.
    """)

    st.image(load_image("ab_testing", "ab_single_run_lift_by_category.png"), caption="Lift by Category")
    st.markdown("""
    The lift chart shows the percentage change in conversion rates between Group B and Group A. Positive lift indicates improved performance due to the treatment. The test results include:

    - **Clothing**: Significant lift with high statistical confidence (p < 0.001). Strong candidate for immediate rollout.
    - **Electronics**: Also demonstrated strong uplift and confidence, suggesting favorable user reception to treatment.
    - **Home Goods**: Moderate lift but within acceptable margin for positive effect.
    - **Toys**: Experienced a negative lift. This may reflect a mismatch between treatment features and buyer intent.
    - **Beauty**: Showed negligible difference — no evidence that treatment impacted behavior.

    **Next Steps:**
    - Roll out to Clothing and Electronics categories.
    - Reevaluate or A/B test Toys with an alternative treatment.
    - Monitor Beauty further before taking action.

    **Insight:** Even when overall performance appears promising, category-specific tests reveal critical variance that should guide strategy.
    """)
    st.markdown("---")
    # A/B Testing (Simulation)
elif selected == "A/B Testing (Simulation)":
    st.title("A/B Testing (Simulation Analysis)")
    st.markdown("""
    This module simulates the variability in A/B test results across multiple randomized trials. Instead of a one-off result, simulation helps assess how stable the observed effect is across different samples and customer segments.
    
    **Why Simulation Matters:**  
    In real-world scenarios, the outcome of an A/B test can vary based on sample size, randomness, or seasonality. Running simulations allows analysts to quantify the likelihood of observing meaningful lift or noise across runs. It's a best practice before rolling out a major update.
    """)
    st.markdown("---")

    st.image(load_image("ab_testing", "ab_simulation_lift_distribution.png"), caption="Lift Distribution Over 100 Simulations")
    st.markdown("""
    This histogram shows the simulated lift distribution across 100 test replications. Each simulation involves resampling the test/control groups and re-calculating the conversion lift.

    **Key Observations:**
    - **Clothing and Electronics** segments maintain strong positive lift distributions with low variance.
    - **Home Goods** shows a wider spread but still positive central tendency, indicating moderate effect.
    - **Toys** consistently underperform, with most simulations suggesting negative lift.
    - **Beauty** fluctuates around zero, confirming a high-noise or low-signal effect.

    **Takeaway:**
    - Confidence in **Clothing, Electronics, and Home Goods** to perform reliably across customer samples.
    - **Toys** treatment likely needs redesign or different segmentation logic.
    - Avoid rolling out changes across **Beauty** without further targeted testing.

    Simulations like this are ideal for modeling uncertainty and decision-making under probabilistic confidence.
    """)
    st.markdown("---")

# Customer Segmentation
elif selected == "Customer Segmentation":
    st.title("Customer Segmentation via Behavioral Clustering")
    st.markdown("""
    Understanding your customers at a granular level is foundational to ecommerce personalization, retention, and lifecycle marketing. This module groups users based on behavioral traits: total spend, frequency of orders, and active lifespan.
    
    **Goal:** Segment customers to deliver differentiated experiences and marketing strategies that resonate with each behavior group.
    """)
    st.markdown("---")

    st.markdown("### Clustering by Customer KPIs")
    st.image(load_image("customer_analytics", "customer_segments_by_behavior_clusters.png"), caption="Customer Segments (Behavioral Clustering)")
    st.markdown("""
    This pairplot visualizes how customers cluster by their total spend, order count, and engagement duration.

    **Insights:**
    - A tight group of high-spenders suggests elite users who warrant loyalty programs or premium tiers.
    - A large cluster of low-frequency, low-spend customers may be price-sensitive or newly acquired.
    - Mid-tier segments show consistent, healthy engagement, ideal for retention campaigns or targeted bundling.

    Tailoring messages and offers to each segment ensures higher response rates and marketing ROI.
    """)

    st.markdown("### Dimensionality Reduction for Visualization")
    st.image(load_image("customer_analytics", "pca_projection_of_customer_segments.png"), caption="PCA Projection of Customer Clusters")
    st.markdown("""
    PCA enables us to compress high-dimensional behavioral data into a 2D visualization. Each point represents a customer, colored by their assigned cluster.

    - Clear separation means strong differentiation in behavior.
    - Overlapping regions may require sub-clustering or additional features.

    Segmentation is foundational to building **personalized ecommerce pipelines** — from product recommendations to retention emails and churn prevention.
    """)
    st.markdown("---")

# Customer Lifetime Value (CLV) Modeling
elif selected == "Customer Lifetime Value (CLV) Modeling":
    st.title("Customer Lifetime Value (CLV) Modeling")
    st.markdown("""
    CLV modeling helps estimate the total revenue a customer is expected to generate over their lifecycle. Businesses use it to allocate acquisition budgets, rank customer segments, and justify retention investments.

    **Why CLV is Critical:**  
    Not all customers contribute equally. Knowing which users will yield long-term value helps optimize your acquisition spend, churn mitigation efforts, and loyalty programs.
    """)
    st.markdown("---")

    st.markdown("### Top Predictive Features of CLV")
    st.image(load_image("customer_analytics", "feature_importance_plot.png"), caption="Feature Importance for CLV Prediction")
    st.markdown("""
    Features like **average order value**, **order count**, and **recency** were the most influential in predicting future spend.

    - Customers who order frequently and recently are more likely to remain active.
    - Large average basket size boosts projected CLV.
    - Days since last purchase plays a key role in churn prediction.

    Use these features to feed into your CRM systems and create high-CLV targeting strategies.
    """)

    st.markdown("### Customer Spend Distribution")
    st.image(load_image("KPI_analysis", "total_spend_per_customer.png"), caption="Distribution of Total Spend per Customer")
    st.markdown("""
    Spend is heavily skewed — a small % of users account for a large % of revenue.

    - Top 10% of customers drive nearly 50% of total revenue.
    - Long tail of users with minimal spend is expected but should be nurtured.

    **Strategic Moves:**
    - Reward top spenders with VIP perks.
    - Run winback campaigns on dormant mid-tier users.
    - Predict early CLV and intervene with personalized incentives.

    CLV helps shift focus from acquisition-only thinking to **lifetime economics**.
    """)
    st.markdown("---")

# Sales Forecasting
elif selected == "Sales Forecasting":
    st.title("Sales Forecasting with Prophet Time Series Modeling")
    st.markdown("""
    This module uses time series modeling to predict future ecommerce sales. The **Prophet** library by Meta is used to capture seasonality, growth trends, and calendar effects.

    **Business Need:**  
    Accurate forecasting helps teams align supply chain, inventory, marketing spend, and operational staffing around anticipated demand.
    """)
    st.markdown("---")

    st.markdown("### Model Metrics Overview")
    col1, col2 = st.columns(2)
    col1.metric(label="Mean Absolute Error (MAE)", value="455.45")
    col2.metric(label="Root Mean Squared Error (RMSE)", value="540.91")

    with st.expander("Model Interpretation"):
        st.markdown("""
        - The model captured consistent **weekly seasonality** and **minor upward trend**.
        - **Holiday effects** and **outlier smoothing** were integrated for realism.
        - Confidence intervals allow us to see upside/downside demand risk.

        These forecasts form the backbone for inventory planning and ad budgeting.
        """)

    st.markdown("### Historical Sales")
    st.image(load_image("forecasting", "daily_total_sales_time_series.png"), caption="Daily Sales Time Series")

    st.markdown("### Decomposed Time Series Components")
    st.image(load_image("forecasting", "daily_total_sales_decomposition.png"), caption="Trend, Seasonality, Residuals")

    st.markdown("### Forecast Horizon")
    st.image(load_image("forecasting", "daily_sales_forecast_prophet.png"), caption="Prophet Forecast with Uncertainty Bounds")

    st.markdown("""
    **Final Notes:**
    - Consider updating models monthly for freshness.
    - Forecasts enable risk-aware decision making, especially during peak or volatile seasons.
    """)
    st.markdown("---")



