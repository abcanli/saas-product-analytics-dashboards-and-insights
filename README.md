📊 SaaS Product Analytics Dashboards & Insights

Retention • Churn • Feature Usage • Revenue • Cohort Analysis (Streamlit + Plotly)

This project is a full end-to-end SaaS Product Analytics platform built with Python, Streamlit, Plotly, and Pandas.
It simulates realistic SaaS customer behavior and provides interactive dashboards that help Product, Growth, and Data teams answer core questions such as:

“How well are we retaining users?”

“Where do customers churn?”

“Which features drive engagement?”

“Which plans or acquisition channels perform best?”

“How is revenue evolving month-over-month?”

The project includes data generation, cleaning, transformations, and dynamic dashboards — structured exactly like a real product analytics workflow.

🚀 Live Features
✔ Interactive Filters

Filter dashboards by:

Country

Plan type (free, pro, enterprise)

Acquisition channel (organic, ads, referral, partner)

Date range

✔ Dashboards Included
Dashboard	Description
Overview	High-level KPIs (active users, signups, conversions, revenue)
Cohort Analysis	Full retention heatmap with cohort tracking
Feature Usage	Event-based feature adoption & usage intensity
Revenue Insights	Monthly recurring revenue, ARPU, plan-level breakdown

All charts render instantly and update based on filter selections.

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

🧪 Synthetic SaaS Dataset

The project includes a realistic, large-scale synthetic dataset that mimics:

Monthly signups

Feature usage events

Revenue patterns

Churn behavior

Plan upgrades / downgrades

Acquisition channels

To generate data:

python src/generate_data.py


This will create fresh randomized SaaS event logs and user-level data.

📈 Dashboards Preview
🔥 Cohort Retention Heatmap

Visualizes how well each signup cohort retains over time

Darker blue = higher retention

Fully dynamic based on filters

🔥 Feature Usage Dashboard

Event-level breakdown for key SaaS features

Perfect for understanding activation & adoption

🔥 Revenue Insights

Monthly Recurring Revenue (MRR)

Average Revenue Per User (ARPU)

Expansion vs contraction revenue

⚙️ Installation & Setup
git clone https://github.com/abcanli/saas-product-analytics-dashboards-and-insights.git
cd saas-product-analytics-dashboards-and-insights

python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt


Then run:

streamlit run app.py


Open your browser at:
👉 http://localhost:8501

🧩 Built With

Python

Streamlit

Plotly

Pandas / NumPy

Scikit-Learn (optional transformations)

Synthetic data generation

🧠 Why This Project Matters (For Your Portfolio)

This project demonstrates:

✔ Strong product analytics thinking

(cohort analysis, retention, revenue, funnel understanding)

✔ Ability to design dashboards used by real SaaS teams

(Product, Growth, CX, Revenue Ops)

✔ End-to-end data skills

(data generation → cleaning → processing → visualization → app)

✔ Streamlit + Plotly UI development

(clean, modern, highly interactive dashboards)

This is the exact type of project hiring managers LOVE to see for:
📌 Data Analyst
📌 Product Analyst
📌 Data Scientist
📌 Analytics Engineer
📌 Growth Analyst roles.

👤 Author

Ali Berk Canlı
Data Analytics & NLP Projects
GitHub: https://github.com/abcanli

LinkedIn: https://www.linkedin.com/in/aliberkcanlı
