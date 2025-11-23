import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def dau_mau_chart(dau: pd.DataFrame, mau: pd.DataFrame):
    fig = go.Figure()
    if not dau.empty:
        fig.add_trace(go.Scatter(x=dau["date"], y=dau["dau"], mode="lines", name="DAU"))
    if not mau.empty:
        fig.add_trace(go.Scatter(x=mau["month"], y=mau["mau"], mode="lines", name="MAU"))
    fig.update_layout(title="Daily & Monthly Active Users", xaxis_title="Date", yaxis_title="Users")
    return fig

def retention_heatmap(matrix: pd.DataFrame):
    if matrix.empty:
        return go.Figure()
    fig = px.imshow(
        matrix.values,
        labels=dict(x="Months since signup", y="Cohort (signup month)", color="Retention"),
        x=matrix.columns,
        y=[d.strftime("%Y-%m") for d in matrix.index],
        color_continuous_scale="Blues",
    )
    fig.update_layout(title="Cohort Retention Heatmap")
    return fig

def feature_usage_bar(feature_usage_df: pd.DataFrame):
    if feature_usage_df.empty:
        return go.Figure()
    fig = px.bar(feature_usage_df, x="feature_name", y="event_count", title="Feature Usage (Events)")
    fig.update_layout(xaxis_title="Feature", yaxis_title="Event count")
    return fig

def funnel_chart(funnel_df: pd.DataFrame):
    if funnel_df.empty:
        return go.Figure()
    fig = go.Figure(
        go.Funnel(
            y=funnel_df["step"],
            x=funnel_df["count"],
            textinfo="value+percent initial",
        )
    )
    fig.update_layout(title="Signup → Activation → Paying → Retained Funnel")
    return fig

def mrr_trend_chart(mrr_df: pd.DataFrame):
    if mrr_df.empty:
        return go.Figure()
    fig = px.line(mrr_df, x="month", y="mrr", title="Monthly Recurring Revenue (MRR)")
    fig.update_layout(xaxis_title="Month", yaxis_title="MRR")
    return fig

def churn_trend_chart(revenue_df: pd.DataFrame):
    if revenue_df.empty or "churn_mrr" not in revenue_df.columns:
        return go.Figure()
    fig = px.line(revenue_df, x="month", y="churn_mrr", title="Churn MRR Trend")
    fig.update_layout(xaxis_title="Month", yaxis_title="Churn MRR")
    return fig
