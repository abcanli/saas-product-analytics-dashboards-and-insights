import pandas as pd

def feature_usage_counts(events: pd.DataFrame) -> pd.DataFrame:
    df = events.copy()
    df = df[df["feature_name"].notna()]
    counts = df.groupby("feature_name")["user_id"].count().reset_index(name="event_count")
    counts = counts.sort_values("event_count", ascending=False)
    return counts

def feature_usage_by_plan(events: pd.DataFrame, subscriptions: pd.DataFrame) -> pd.DataFrame:
    df = events.copy()
    df = df[df["feature_name"].notna()]
    latest_sub = subscriptions.sort_values("subscription_start_date").drop_duplicates("user_id", keep="last")
    df = df.merge(latest_sub[["user_id", "plan_type"]], on="user_id", how="left")
    grouped = df.groupby(["plan_type", "feature_name"])["user_id"].count().reset_index(name="event_count")
    return grouped

def top_features(events: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    counts = feature_usage_counts(events)
    return counts.head(n)
