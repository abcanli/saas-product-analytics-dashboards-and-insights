import pandas as pd

def monthly_mrr(revenue: pd.DataFrame) -> pd.DataFrame:
    df = revenue.copy().sort_values("month")
    return df[["month", "mrr"]]

def net_mrr_growth(revenue: pd.DataFrame) -> pd.DataFrame:
    df = revenue.copy().sort_values("month")
    df["prev_mrr"] = df["mrr"].shift(1)
    df["net_mrr_growth"] = df["mrr"] - df["prev_mrr"].fillna(0)
    return df[["month", "net_mrr_growth"]]

def arpu(subscriptions: pd.DataFrame, revenue: pd.DataFrame) -> pd.DataFrame:
    df_rev = revenue.copy().sort_values("month")
    subs = subscriptions.copy()
    records = []
    for _, row in df_rev.iterrows():
        month = row["month"]
        month_end = (month + pd.offsets.MonthEnd(0)).to_pydatetime()
        active_mask = (subs["subscription_start_date"] <= month_end) & (
            subs["subscription_end_date"].isna() | (subs["subscription_end_date"] >= month)
        )
        active_users = subs[active_mask]["user_id"].nunique()
        mrr = row["mrr"]
        arpu_val = mrr / active_users if active_users > 0 else 0.0
        records.append({"month": month, "arpu": arpu_val})
    return pd.DataFrame(records)

def ltv_estimate(subscriptions: pd.DataFrame, revenue: pd.DataFrame) -> float:
    if subscriptions.empty:
        return 0.0
    subs = subscriptions.copy()
    subs["end"] = subs["subscription_end_date"].fillna(pd.Timestamp.utcnow())
    subs["lifetime_months"] = (subs["end"] - subs["subscription_start_date"]) / pd.Timedelta(days=30)
    avg_lifetime = subs["lifetime_months"].mean()
    avg_mrr = subs["mrr"].mean()
    return float(avg_mrr * avg_lifetime)
