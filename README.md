# Ecommerce Intelligence Dashboard

**:rocket: Live Demo:** [https://ecommerce-intelligence-dashboard.streamlit.app/](https://ecommerce-intelligence-dashboard.streamlit.app/)  
**Tech Stack:** Python · Streamlit · Plotly · scikit-learn · Prophet · pandas · numpy · PIL

---

## :bar_chart: Overview

The **Ecommerce Intelligence Dashboard** is a production-ready, modular analytics app that simulates a real-world data analytics workflow across five core modules:

- KPI Monitoring
- A/B Testing (single + simulation)
- Customer Segmentation
- CLV Modeling
- Time Series Forecasting

This project is designed to showcase end-to-end **data analysis**, **machine learning**, and **business intelligence** in a single interactive experience.

---

## :triangular_ruler: Key Features

### 1. KPI Dashboard
- Real-time filtering of transactional data
- KPIs: Total Revenue, Average Order Value, Transactions
- Visuals: Revenue over time, payment method distribution, revenue by category
- Actionable insights around pricing strategy and product performance

### 2. A/B Testing
- **Single Experiment Module**: Conversion lift, confidence intervals, z-test results
- **Simulation Module**: 100-run variability simulation of statistical lift
- Category-level interpretation and rollout recommendations

### 3. Customer Segmentation
- K-means clustering based on total spend, frequency, recency
- PCA visualization of behavioral clusters
- Strategic implications for marketing, churn prevention, and campaign targeting

### 4. Customer Lifetime Value (CLV) Modeling
- Predictive modeling of customer revenue potential
- Feature importance: avg order value, frequency, recency
- Visual breakdown of high-value vs low-value customer base

### 5. Sales Forecasting
- Daily revenue forecasts using Prophet
- Seasonal-trend decomposition and uncertainty intervals
- Practical use cases for supply chain, budget planning, and marketing timing

---

## :dart: Skills & Concepts Demonstrated

- **Statistical Testing**: z-tests, confidence intervals, simulated experiment runs  
- **Machine Learning**: customer clustering, predictive modeling for CLV  
- **Time Series Forecasting**: Prophet for demand prediction  
- **Data Visualization**: custom layouts using Plotly and Streamlit  
- **Dashboard Development**: modular, scalable, UX-optimized design  
- **Business Strategy**: data-driven recommendations tied to real KPIs

---

## :file_folder: Project Structure

```
ecommerce-data-analytics-case-study/
│
├── app.py                          # Streamlit application
├── README.md                       # Project documentation
├── requirements.txt                # Python dependencies
├── .gitignore                      # Ignored files/folders
│
├── assets/                         # Static visuals
│   ├── ab_testing/
│   ├── KPI_analysis/
│   └── customer_analytics/
│
├── notebooks/                      # Data analysis notebooks
│   ├── AB_Testing_Single_Run_Analysis.ipynb
│   ├── AB_Testing_Simulation_Analysis.ipynb
│   ├── Customer_Lifetime_Value_Modeling.ipynb
│   └── Customer_Segmentation_KPIs_Analysis.ipynb
```

---

## :bulb: Highlights

- Full-stack dashboard deployment using Streamlit Cloud  
- Project simulates stakeholder deliverables: metrics, analysis, insights, and recommendations  
- Built with reusability, extensibility, and business alignment in mind  
- Focused on communication of insights, not just technical complexity

---

## :link: Try the Live App

👉 [App](https://ecommerce-intelligence-dashboard.streamlit.app/)

---

## :bust_in_silhouette: About

This project was built to demonstrate practical analytics capabilities to hiring managers and recruiters. It serves as a complete walkthrough of applied **data science and business intelligence** in an ecommerce setting.

---
