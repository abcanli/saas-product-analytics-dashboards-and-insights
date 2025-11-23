# SaaS Product Analytics Dashboard – Retention, Churn, Feature Usage & Revenue

This project simulates a realistic **SaaS Product Analytics** stack and provides an interactive dashboard
for exploring user behavior, retention, churn, feature usage, and revenue trends.

It is designed as a portfolio-ready, production-style project for **Data Analysts**, **Product Analysts**,
and **ML/NLP Analysts** who want to demonstrate strong analytics and product thinking.

## 🚀 Features

- Synthetic SaaS dataset (~20k users, 18 months)
- Subscriptions, churn, upgrades
- Events for logins, sessions, feature usage
- Monthly revenue (MRR, churn MRR, expansion, contraction)
- Metric modules (DAU/MAU, cohorts, funnel, revenue)
- Plotly visualizations
- Streamlit dashboard with multiple pages

## 🧱 Project Structure

```text
saas-product-analytics-dashboard/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── generate_dataset.py
│   ├── analytics.py
│   ├── cohorts.py
│   ├── feature_usage.py
│   ├── revenue_metrics.py
│   ├── visualizations.py
│   └── utils.py
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

```bash
git clone <your-repo-url>.git
cd saas-product-analytics-dashboard

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

## 🧪 Generate Synthetic Dataset

```bash
python src/generate_dataset.py
```

This will create CSVs in `data/raw/`.

## 🚀 Run the Dashboard

```bash
streamlit run app.py
```

Then open the URL printed in the terminal (typically `http://localhost:8501`).

## 👀 Dashboard Pages

- **Overview**: KPIs (users, churn, activation, MRR), DAU/MAU trends, conversion funnel  
- **Cohorts**: Signup cohorts and retention heatmap  
- **Feature Usage**: Top features and usage by plan type  
- **Revenue**: MRR trend, churn MRR, ARPU, simple LTV estimate  

## 🧩 Skills Demonstrated

- SaaS data modeling
- Product & growth analytics
- Cohort & retention analysis
- Funnel analysis
- Revenue metrics (MRR, ARPU, LTV)
- Data visualization with Plotly
- Interactive dashboards with Streamlit
