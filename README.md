
<img src="https://raw.githubusercontent.com/rodrigo-bravo/ecommerce-data-analytics-case-study/main/assets/banner.png" alt="Ecommerce Intelligence Dashboard" style="width:100%;">

<p align="center">
<a href="https://ecommerce-intelligence-dashboard.streamlit.app/"><strong>🔗 Launch Live App</strong></a> 
</p>

<p align="center">
A modular, production-grade dashboard for e-commerce data analytics, machine learning, and decision-making.
</p>

<p align="center">
<a href="https://img.shields.io/github/license/rodrigo-bravo/ecommerce-data-analytics-case-study"><img src="https://img.shields.io/github/license/rodrigo-bravo/ecommerce-data-analytics-case-study?style=flat-square" alt="MIT License"></a>
<a href="https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat-square"><img src="https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat-square" alt="Python Version"></a>
<a href="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn%20%7C%20Prophet-orange?style=flat-square"><img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn%20%7C%20Prophet-orange?style=flat-square" alt="ML Libraries"></a>
</p>

---

## Overview

The **E-commerce Intelligence Dashboard** simulates a full-stack analytics workflow:

- End-to-end **data processing**, **exploratory analysis**, and **business storytelling**
- Integrated **machine learning** for segmentation and CLV prediction
- Interactive visuals for A/B testing, forecasting, and product insights

---

## Installation

Use a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Then run the app locally with:

```bash
streamlit run app.py
```
> **Note:** Python version is 3.9+ 
---

## Stack

* **Python** (`pandas`, `scikit-learn`, `plotly`, `prophet`, `streamlit`)
* **Machine Learning** • A/B testing, clustering, predictive modeling
* **Visualization** • Interactive graphs + static analysis

---

## Purpose & Motivation

This dashboard showcases:

* Real business insights from messy data
* Effective A/B testing analysis
* Production-ready forecasting
* ML-powered customer intelligence

---

Key Features / Modules

### KPI Dashboard

> Analyze core revenue drivers across categories and time

- Time-series visualizations for daily sales
- Dynamic filtering by date range
- Revenue breakdown by product and payment method
- Distribution of purchase amounts

##

### A/B Testing

> Simulate and analyze experimental results across multiple verticals

#### Single Run
- Conversion rate delta between control/treatment groups
- Z-scores and p-values per product category

#### Simulation
- Bootstrapped lift distributions across 100 simulations
- Confidence intervals for treatment effect consistency

**Code Snippet:**

```python
from statsmodels.stats.proportion import proportions_ztest

# Perform z-test
count = np.array([success_A, success_B])
nobs = np.array([total_A, total_B])
zstat, pval = proportions_ztest(count, nobs)
````

##

### Customer Segmentation

> Behavioral clustering with visual explanations

* KMeans clustering on Recency, Frequency, Monetary (RFM) data
* Dimensionality reduction via PCA
* Strategic marketing suggestions per cluster

**Code Snippet:**

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)
kmeans = KMeans(n_clusters=4, random_state=42).fit(rfm_scaled)
```

##

### Customer Lifetime Value (CLV) Modeling

> Predict customer revenue potential using regression

* ML model using `scikit-learn` (Random Forest Regressor)
* Feature importance via `model.feature_importances_`
* Visualization of high-value customers

**Model Highlights:**

* MAE: 85.3
* RMSE: 111.7

```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor()
model.fit(X_train, y_train)
predicted_clv = model.predict(X_test)
```

##

### Sales Forecasting

> Anticipate future demand using time-series ML

* Time series modeling using Facebook’s **Prophet**
* Decomposition of trend, seasonality, and noise
* Forecasting with uncertainty bands

**Forecast Output:**

* Quarterly planning insights
* Inventory balancing
* Seasonal marketing timing

---


## License

This project is under the [MIT License](LICENSE).

---





