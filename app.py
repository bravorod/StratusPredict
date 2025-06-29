import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# Set page configuration
st.set_page_config(
    page_title="Ecommerce Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load images from assets
def load_image(folder, filename):
    return Image.open(os.path.join("assets", folder, filename))

# Function to load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/ecommerce_transactions.csv", parse_dates=["purchase_date"])
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    return df

# Load data
df = load_data()

# Sidebar navigation
st.sidebar.title("📊 Ecommerce Analytics Dashboard")
selected = st.sidebar.radio(
    "Choose a Module",
    [
        "KPI Dashboard",
        "A/B Testing (Single Run)",
        "A/B Testing (Simulation)",
        "Customer Segmentation",
        "Customer Lifetime Value (CLV) Modeling",
        "Sales Forecasting"
    ]
)

# Sidebar filters (for KPI Dashboard)
if selected == "KPI Dashboard":
    st.sidebar.subheader("Filter Data")
    min_date = df["purchase_date"].min()
    max_date = df["purchase_date"].max()
    date_range = st.sidebar.date_input("Select Date Range:", [min_date, max_date])
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.warning("Please select a valid start and end date.")
        st.stop()
    df = df[(df["purchase_date"] >= pd.to_datetime(start_date)) & (df["purchase_date"] <= pd.to_datetime(end_date))]
    

    # KPI Summary Cards 
    total_revenue = df['purchase_amount'].sum()
    avg_order_value = df['purchase_amount'].mean()
    total_transactions = df.shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("Avg. Order Value", f"${avg_order_value:,.2f}")
    col3.metric("Total Transactions", f"{total_transactions:,}")

    # Interactive Time Series Chart
    st.subheader("Total Sales Over Time (Interactive)")

    # Aggregate daily sales
    daily_sales = (
        df.groupby("purchase_date")["purchase_amount"]
        .sum()
        .reset_index()
        .rename(columns={"purchase_date": "Date", "purchase_amount": "Total Sales"})
    )

    # Date range selector
    min_date = daily_sales['Date'].min()
    max_date = daily_sales['Date'].max()
    date_range = st.date_input("Filter by Date Range", [min_date, max_date], key="time_series")
    if len(date_range) == 2:
        ts_start, ts_end = date_range
    else:
        st.warning("Please select a valid date range for the time series.")
        st.stop()

    filtered_sales = daily_sales[(daily_sales['Date'] >= pd.to_datetime(ts_start)) & (daily_sales['Date'] <= pd.to_datetime(ts_end))]

    # Line chart with hover and zoom
    fig = px.line(
        filtered_sales,
        x="Date",
        y="Total Sales",
        title="Total Sales Over Time",
        labels={"Date": "Date", "Total Sales": "Total Sales ($)"},
        template="plotly_white"
    )
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Static KPI Visuals and Insights
    st.subheader("Key Performance Indicators (KPIs)")
    st.markdown("")

    # Payment Method Pie Chart
    st.image(load_image("KPI_analysis", "payment_method_distribution.png"), caption="Payment Method Distribution")
    st.markdown("""
    **Payment Method Insights:**
    - **Crypto** accounts for the largest share of transactions at 25.7%, slightly edging out other methods.
    - **Gift Cards** follow closely at **25.3%**, indicating high usage of prepaid balances or store credits.
    - **Credit Cards** and **PayPal** are equally popular at **24.5%** each.
    - Overall distribution is balanced, suggesting multiple well-utilized options.

    **Recommendation:** Consider prioritizing preferred payment methods in the checkout flow or offering promotions tied to underutilized ones.
    """)
    st.markdown("")
    st.markdown("")

    # Revenue by Product Category
    st.image(load_image("KPI_analysis", "revenue_contribution_by_category.png"), caption="Revenue by Product Category")
    st.markdown("""
    **Insights:**
    - **Beauty** leads in both volume and revenue, suggesting high demand and value.
    - **Electronics** and **Clothing** follow closely, indicating competitive segments.
    - Balanced revenue-to-volume ratios suggest well-aligned pricing across top categories.

    **Strategic Focus:** Invest in Beauty promotions and continue tracking Electronics and Clothing as core revenue drivers.
    """)
    st.markdown("")
    st.markdown("")


    # Purchase Amount Histogram
    st.image(load_image("KPI_analysis", "distribution_of_purchase_amounts.png"), caption="Purchase Amount Distribution")
    st.markdown("""
    **Histogram Highlights:**
    - Heavily right-skewed — dominated by low-value transactions.
    - Most purchases range from **$0–$100**, peaking at **$20–$40**.
    - Long tail confirms rare but extreme high-value orders.

    **Business Insight:** Tailor fraud detection and customer segmentation logic to differentiate enterprise from retail spenders.
    """)

    st.markdown("")

    st.markdown("---")

# A/B Testing (Single Run)
elif selected == "A/B Testing (Single Run)":
    st.markdown("<h1 style='text-align: center; color: MediumSeaGreen;'>A/B Testing: Single Run</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; '>View conversion rates and lift from a single experiment run</h5>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("The A/B test was performed across **5** product categories to evaluate whether the treatment (Group B) significantly affected conversion rates compared to the control (Group A). A **z-test** for proportions was applied to each category to measure lift, statistical confidence, and significance.")
    st.text("")
    st.image(load_image("ab_testing", "ab_single_run_conversion_rates.png"), caption="Conversion Rates by Group")
    st.image(load_image("ab_testing", "ab_single_run_lift_by_category.png"), caption="Lift by Category")
    st.markdown("""
    **Key Results:**

    - **Clothing, Electronics, and Home Goods** showed strong positive lift and extremely high z-scores with **p-values < 0.001**, indicating a **statistically significant improvement** in conversion rates for Group B
    - **Toys** demonstrated a **statistically significant negative lift** (-16.85%), suggesting the treatment may have adversely impacted conversions in this segment
    - **Beauty** had an insignificant lift (~0.2%) with a **p-value of 0.9959**, suggesting **no meaningful difference** between control and variant

    **Interpretation:**

    - The **statistically significant uplift** in key categories supports a positive business impact of the treatment
    - The **Toys category may require re-evaluation**, as the treatment had a detrimental effect
    - The **Beauty segment's result may be due to random noise**, and does not warrant campaign changes

    **Recommendation:**

    - **Roll out** the treatment across Clothing, Electronics, and Home Goods
    - **Investigate** the negative response in Toys for possible UX or targeting issues
    - **No action** needed for Beauty until further data confirms a trend
    """)

    st.markdown("---")

# A/B Testing (Simulation)
elif selected == "A/B Testing (Simulation)":
    st.markdown("<h1 style='text-align: center; color: MediumSeaGreen;'>A/B Testing: Simulation Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; '>Analyze the distribution of outcomes across multiple A/B test simulations</h5>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h6 style='text-align: center; '>Lift variability visualization across simulations</h6>", unsafe_allow_html=True)
    st.image(load_image("ab_testing", "ab_simulation_lift_distribution.png"), caption="Lift Distribution Over 100 Simulations")
    st.markdown("""
    **Key Results:**

    - **Clothing, Electronics, and Home Goods** showed **consistently strong positive lift** across 100 simulations, with narrow distribution ranges indicating **robust improvements** in conversion under treatment
    - **Toys** demonstrated a **consistently negative lift** distribution, reinforcing that the treatment likely **harmed conversion rates** in this segment
    - **Beauty** showed a **wide, centered distribution** around zero, suggesting **high variability** and **no reliable impact** from the treatment

    **Interpretation:**

    - Simulation results validate the **stability and statistical reliability** of lift observed in Clothing, Electronics, and Home Goods 
    - The **persistent negative lift** in Toys highlights a **potential UX or campaign flaw** in the treatment group for that category  
    - Beauty's **inconclusive distribution** indicates the result may be due to **random noise**, and further data is needed before adjusting strategies

    **Recommendation:**

    - **Greenlight rollout** of the treatment for Clothing, Electronics, and Home Goods where the lift is reliable and positive
    - **Pause rollout** in Toys and investigate the **root causes** behind its underperformance
    - **Continue monitoring** the Beauty category; run additional A/B tests or segment-level deep dives to gather more evidence before making campaign changes 
    """)

    st.markdown("---")

# Customer Segmentation
elif selected == "Customer Segmentation":
    st.markdown("<h1 style='text-align: center; color: Lightblue;'>Customer Segmentation</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; '>Group users by behavioral patterns</h5>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("Group customers based on behavioral patterns such as total spend, order frequency, and activity span. These segments help uncover distinct purchasing habits and enable targeted marketing strategies, loyalty programs, or personalized promotions.")
    st.text("")
    st.markdown("<h6 style='text-align: center; '>Relationship between features (e.g., total spend, order count) across clusters</h6>", unsafe_allow_html=True)
    st.image(load_image("customer_analytics", "customer_segments_by_behavior_clusters.png"), caption="Customer Segments (Clusters)")
    st.markdown("""
    This pairplot reveals clear separation between customer clusters based on KPIs like total spend, order count, and activity. The diagonal histograms and scatter plots show how different clusters dominate distinct behavioral patterns.
    """)
    st.text(" ")
    st.text(" ")
    st.markdown("<h6 style='text-align: center; '>Cluster separation visualization in a 2D space</h6>", unsafe_allow_html=True)
    st.image(load_image("customer_analytics", "pca_projection_of_customer_segments.png"), caption="PCA Projection")
    st.markdown("""
    Principal Component Analysis (PCA) reduces dimensionality for visualizing cluster separation. Each point represents a customer, colored by their assigned cluster — showing distinct groupings and overlaps that guide targeting strategy.
    """)
    st.text(" ")
    st.text(" ")
    st.markdown("""
    **Key Insights:**  
    - High-spending customers form a tight and distinct cluster — ideal for loyalty or upsell campaigns.
    - A large cluster of low-activity users may be dormant or at risk of churn.
    - Some clusters have frequent purchases but low spend, suggesting low-margin frequent buyers (good for bundling offers).
    """)

    st.markdown("---")

# Customer Lifetime Value
elif selected == "Customer Lifetime Value (CLV) Modeling":
    st.markdown("<h1 style='text-align: center; color: Lightblue;'>Customer Lifetime Value (CLV) Modeling</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; '>Predict long-term customer revenue</h5>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("Estimate the total future revenue a customer is likely to bring over their lifetime. This supports ROI forecasting, customer prioritization, and marketing budget allocation.")
    st.text("")
    st.markdown("<h6 style='text-align: center; '>Customer features that strongly predict CLV</h6>", unsafe_allow_html=True)
    st.image(load_image("customer_analytics", "feature_importance_plot.png"), caption="Feature Importance")
    st.markdown("""
    This chart highlights the top predictors of Customer Lifetime Value, such as average order value, recency, and order count. These insights guide acquisition targeting and lifecycle strategy.
    """)
    st.text(" ")
    st.text(" ")
    st.markdown("<h6 style='text-align: center; '>Actual spend distribution across the customer base</h6>", unsafe_allow_html=True)
    st.image(load_image("KPI_analysis", "total_spend_per_customer.png"), caption="Total Spend per Customer")
    st.markdown("""
    The total spend plot reveals a right-skewed distribution — a small group of customers drive a large portion of revenue. This reinforces the need to focus on top-value segments.
    """)
    st.text(" ")
    st.text(" ")
    st.markdown("""
    **Key Findings:**  
    - A small % of customers generate a disproportionately high share of revenue — these are high-LTV customers worth building.
    - Order frequency and average order value are the most important CLV drivers.
    - Predictive modeling can help estimate CLV early in a customer's journey and personalize touchpoints accordingly.
    """)

    st.markdown("---")

# 📊 Sales Forecasting Module
elif selected == "Sales Forecasting":
    st.markdown("<h1 style='text-align: center; color: Orange;'>Sales Forecasting</h1>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; '>Forecast daily sales using Prophet time series modeling for better demand planning and resource allocation</h6>", unsafe_allow_html=True)
    st.markdown("---")

    # Metrics section
    st.markdown("### Model Evaluation Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Mean Absolute Error (MAE)", value="455.45")
    with col2:
        st.metric(label="Root Mean Squared Error (RMSE)", value="540.91")

    # Expandable interpretation box
    with st.expander("Interpretation and Strategic Insights"):
        st.markdown("""
        - **Prophet** captured **weekly cycles**, **holidays**, and **mild upward growth trends** in the data.
        - Forecasts align closely with historical sales, validating the model's reliability.
        - **Suitable for:**  
          - Inventory restocking  
          - Revenue projections  
          - Seasonal campaign planning  
        - Forecast uncertainty intervals indicate confidence range and potential volatility.

        **Recommendation:**  
        Use the forecast to guide **quarterly planning**, check **demand smoothing**, and anticipate **supply chain bottlenecks** during peak seasons.
        """)

    # Display raw time series
    st.subheader("Historical Sales Time Series")
    st.image(load_image("forecasting", "daily_total_sales_time_series.png"), caption="Daily Sales Time Series", use_container_width=True)

    # Decomposition plot
    st.subheader("STL Decomposition")
    st.image(load_image("forecasting", "daily_total_sales_decomposition.png"), caption="Seasonality + Trend + Residual Breakdown", use_container_width=True)

    # Forecasted sales
    st.subheader("Forecasted Sales (Prophet Model)")
    st.image(load_image("forecasting", "daily_sales_forecast_prophet.png"), caption="Prophet Forecast (with Uncertainty Interval)", use_container_width=True)

    st.markdown("---")


    
