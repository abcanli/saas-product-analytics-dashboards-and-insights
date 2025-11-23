import pandas as pd

def daily_active_users(events: pd.DataFrame) -> pd.DataFrame:
    events = events.copy()
    events["date"] = events["event_timestamp"].dt.date
    dau = events.groupby("date")["user_id"].nunique().reset_index(name="dau")
    return dau

def monthly_active_users(events: pd.DataFrame) -> pd.DataFrame:
    events = events.copy()
    events["month"] = events["event_timestamp"].dt.to_period("M").dt.to_timestamp()
    mau = events.groupby("month")["user_id"].nunique().reset_index(name="mau")
    return mau

def churn_rate(subscriptions: pd.DataFrame) -> float:
    if subscriptions.empty:
        return 0.0
    churned = subscriptions["is_churned"].sum()
    total = len(subscriptions)
    return float(churned) / float(total)

def activation_rate(users: pd.DataFrame, events: pd.DataFrame) -> float:
    key_events = ["create_project", "share_item", "download_report"]
    activated_users = events[events["event_type"].isin(key_events)]["user_id"].unique()
    if len(users) == 0:
        return 0.0
    return float(len(activated_users)) / float(len(users))

def conversion_funnel(users: pd.DataFrame, events: pd.DataFrame, subscriptions: pd.DataFrame) -> pd.DataFrame:
    total_signed_up = len(users)
    key_events = ["create_project", "share_item", "download_report"]
    activated = events[events["event_type"].isin(key_events)]["user_id"].drop_duplicates().tolist()
    n_activated = len(activated)
    paying = subscriptions[subscriptions["mrr"] > 0]["user_id"].unique().tolist()
    n_paying = len(paying)
    retained = subscriptions[~subscriptions["is_churned"] & (subscriptions["mrr"] > 0)]["user_id"].unique()
    n_retained = len(retained)
    steps = ["Signed up", "Activated", "Paying", "Retained"]
    counts = [total_signed_up, n_activated, n_paying, n_retained]
    return pd.DataFrame({"step": steps, "count": counts})
