import os
import streamlit as st
import pandas as pd

from src.analytics import daily_active_users, monthly_active_users, churn_rate, activation_rate, conversion_funnel
from src.cohorts import build_signup_cohorts, cohort_retention_matrix
from src.feature_usage import feature_usage_counts, feature_usage_by_plan, top_features
from src.revenue_metrics import monthly_mrr, arpu, ltv_estimate
from src.visualizations import dau_mau_chart, retention_heatmap, feature_usage_bar, funnel_chart, mrr_trend_chart, churn_trend_chart

@st.cache_data
def load_data(base_dir: str):
    raw_dir = os.path.join(base_dir, "data", "raw")
    users = pd.read_csv(os.path.join(raw_dir, "users.csv"), parse_dates=["signup_date"])
    subs = pd.read_csv(os.path.join(raw_dir, "subscriptions.csv"), parse_dates=["subscription_start_date", "subscription_end_date"])
    events = pd.read_csv(os.path.join(raw_dir, "events.csv"), parse_dates=["event_timestamp"])
    revenue = pd.read_csv(os.path.join(raw_dir, "revenue.csv"), parse_dates=["month"])
    return users, subs, events, revenue

def apply_filters(users, subs, events, revenue, country, plan, channel, date_range):
    if country:
        users = users[users["country"].isin(country)]
    if channel:
        users = users[users["acquisition_channel"].isin(channel)]
    if plan:
        subs = subs[subs["plan_type"].isin(plan)]
    if date_range:
        start, end = date_range
        events = events[(events["event_timestamp"] >= start) & (events["event_timestamp"] <= end)]
        subs = subs[(subs["subscription_start_date"] <= end) & ((subs["subscription_end_date"].isna()) | (subs["subscription_end_date"] >= start))]
        revenue = revenue[(revenue["month"] >= start.to_period("M").to_timestamp()) & (revenue["month"] <= end.to_period("M").to_timestamp())]
    user_ids = users["user_id"].unique()
    subs = subs[subs["user_id"].isin(user_ids)]
    events = events[events["user_id"].isin(user_ids)]
    return users, subs, events, revenue

def main():
    st.set_page_config(page_title="SaaS Product Analytics Dashboard", layout="wide")
    st.title("📊 SaaS Product Analytics Dashboard")
    base_dir = os.path.dirname(__file__)
    users, subs, events, revenue = load_data(base_dir)

    st.sidebar.header("Filters")
    countries = sorted(users["country"].unique().tolist())
    plans = sorted(subs["plan_type"].unique().tolist())
    channels = sorted(users["acquisition_channel"].unique().tolist())

    selected_countries = st.sidebar.multiselect("Country", countries, default=countries)
    selected_plans = st.sidebar.multiselect("Plan type", plans, default=plans)
    selected_channels = st.sidebar.multiselect("Acquisition channel", channels, default=channels)

    min_date = events["event_timestamp"].min().date()
    max_date = events["event_timestamp"].max().date()
    date_range = st.sidebar.date_input("Date range", [min_date, max_date])
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        date_range = (pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
    else:
        date_range = None

    page = st.sidebar.radio("Page", ["Overview", "Cohorts", "Feature Usage", "Revenue"])

    users_f, subs_f, events_f, revenue_f = apply_filters(users, subs, events, revenue, selected_countries, selected_plans, selected_channels, date_range)

    if page == "Overview":
        st.subheader("Overview")
        col1, col2, col3, col4 = st.columns(4)

        dau_df = daily_active_users(events_f) if not events_f.empty else pd.DataFrame(columns=["date", "dau"])
        mau_df = monthly_active_users(events_f) if not events_f.empty else pd.DataFrame(columns=["month", "mau"])

        churn = churn_rate(subs_f) * 100 if not subs_f.empty else 0.0
        activation = activation_rate(users_f, events_f) * 100 if not users_f.empty else 0.0

        col1.metric("Users", len(users_f))
        col2.metric("Churn rate", f"{churn:.1f}%")
        col3.metric("Activation rate", f"{activation:.1f}%")
        if not revenue_f.empty:
            latest_mrr = revenue_f.sort_values("month")["mrr"].iloc[-1]
        else:
            latest_mrr = 0.0
        col4.metric("Latest MRR", f"${latest_mrr:,.0f}")

        st.plotly_chart(dau_mau_chart(dau_df, mau_df), use_container_width=True)
        funnel_df = conversion_funnel(users_f, events_f, subs_f)
        st.plotly_chart(funnel_chart(funnel_df), use_container_width=True)

    elif page == "Cohorts":
        st.subheader("Cohort Analysis")
        cohorts_df = build_signup_cohorts(users_f)
        matrix = cohort_retention_matrix(users_f, events_f)
        st.write("Signup cohorts (users per month):")
        st.dataframe(cohorts_df)
        st.plotly_chart(retention_heatmap(matrix), use_container_width=True)
        st.info("Each row is a signup month cohort; each column is retention after N months since signup.")

    elif page == "Feature Usage":
        st.subheader("Feature Usage")
        feats = feature_usage_counts(events_f)
        st.plotly_chart(feature_usage_bar(feats), use_container_width=True)
        by_plan = feature_usage_by_plan(events_f, subs_f)
        if not by_plan.empty:
            st.write("Feature usage by plan type")
            st.dataframe(by_plan)
        topf = top_features(events_f, n=10)
        st.write("Top features:")
        st.dataframe(topf)

    elif page == "Revenue":
        st.subheader("Revenue Intelligence")
        mrr_df = monthly_mrr(revenue_f)
        st.plotly_chart(mrr_trend_chart(mrr_df), use_container_width=True)
        st.plotly_chart(churn_trend_chart(revenue_f), use_container_width=True)
        arpu_df = arpu(subs_f, revenue_f) if not revenue_f.empty else pd.DataFrame(columns=["month", "arpu"])
        if not arpu_df.empty:
            st.line_chart(arpu_df.set_index("month"))
        ltv = ltv_estimate(subs_f, revenue_f) if not subs_f.empty else 0.0
        st.metric("Estimated LTV", f"${ltv:,.0f}")

if __name__ == "__main__":
    main()
