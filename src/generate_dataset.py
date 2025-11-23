import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

def ensure_dirs(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def random_dates(start: datetime, end: datetime, n: int) -> np.ndarray:
    delta = end - start
    return np.array([start + timedelta(days=random.randint(0, delta.days)) for _ in range(n)])

def generate_users(n_users: int, start_date: str, end_date: str) -> pd.DataFrame:
    countries = ["DE", "IT", "CH", "TR", "US", "FR", "NL", "SE"]
    channels = ["ads", "organic", "referral", "partner"]
    plans = ["free", "pro", "enterprise"]

    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    user_ids = [f"U{idx:05d}" for idx in range(1, n_users + 1)]
    signup_dates = random_dates(start, end, n_users)

    df = pd.DataFrame(
        {
            "user_id": user_ids,
            "country": np.random.choice(countries, size=n_users, p=[0.2, 0.15, 0.1, 0.15, 0.15, 0.1, 0.1, 0.05]),
            "signup_date": signup_dates,
            "acquisition_channel": np.random.choice(channels, size=n_users, p=[0.35, 0.4, 0.2, 0.05]),
            "initial_plan": np.random.choice(plans, size=n_users, p=[0.6, 0.3, 0.1]),
        }
    )
    return df

def generate_subscriptions(users: pd.DataFrame) -> pd.DataFrame:
    convert_prob = {"free": 0.35, "pro": 0.7, "enterprise": 0.9}
    churn_prob = 0.12
    plan_mrr = {"free": 0.0, "pro": 49.0, "enterprise": 199.0}

    records = []
    for _, row in users.iterrows():
        user_id = row["user_id"]
        signup_date = row["signup_date"]
        plan = row["initial_plan"]

        p_conv = convert_prob[plan]
        converted = np.random.rand() < p_conv

        if not converted and plan == "free":
            records.append(
                {
                    "user_id": user_id,
                    "subscription_start_date": signup_date,
                    "subscription_end_date": None,
                    "plan_type": "free",
                    "is_churned": False,
                    "mrr": 0.0,
                }
            )
            continue

        start_date = signup_date + timedelta(days=np.random.randint(0, 60))
        max_months = 18
        months_active = np.random.geometric(p=churn_prob)
        months_active = min(months_active, max_months)
        end_date = start_date + timedelta(days=30 * months_active)

        today = datetime.utcnow()
        if end_date > today:
            end_date = None
            is_churned = False
        else:
            is_churned = True

        current_plan = plan
        if current_plan == "pro" and np.random.rand() < 0.2:
            current_plan = "enterprise"

        mrr = plan_mrr.get(current_plan, 0.0)

        records.append(
            {
                "user_id": user_id,
                "subscription_start_date": start_date,
                "subscription_end_date": end_date,
                "plan_type": current_plan,
                "is_churned": is_churned,
                "mrr": mrr,
            }
        )

    return pd.DataFrame(records)

def generate_events(
    users: pd.DataFrame,
    start_date: str,
    end_date: str,
    avg_events_per_user: int = 40,
) -> pd.DataFrame:
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    delta_days = (end - start).days

    event_types = [
        "login",
        "session_start",
        "feature_open",
        "create_project",
        "share_item",
        "download_report",
        "session_end",
    ]
    feature_names = [
        "dashboard",
        "analytics_page",
        "billing_page",
        "reports",
        "workspace",
        "team_settings",
    ]

    records = []
    event_id_counter = 1

    for _, row in users.iterrows():
        user_id = row["user_id"]
        n_events = np.random.poisson(lam=avg_events_per_user)
        n_events = max(5, n_events)

        for _ in range(n_events):
            day_offset = np.random.randint(0, delta_days + 1)
            ts = start + timedelta(days=int(day_offset), hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))
            etype = np.random.choice(event_types, p=[0.25, 0.15, 0.25, 0.1, 0.1, 0.05, 0.1])
            feature = None
            if etype in ["feature_open", "create_project", "share_item", "download_report"]:
                feature = np.random.choice(feature_names)

            records.append(
                {
                    "event_id": f"E{event_id_counter:07d}",
                    "user_id": user_id,
                    "event_type": etype,
                    "event_timestamp": ts,
                    "feature_name": feature,
                }
            )
            event_id_counter += 1

    return pd.DataFrame(records)

def generate_revenue(subscriptions: pd.DataFrame) -> pd.DataFrame:
    if subscriptions.empty:
        return pd.DataFrame(columns=["month", "mrr", "expansion_mrr", "contraction_mrr", "churn_mrr", "new_mrr"])

    min_date = subscriptions["subscription_start_date"].min().replace(day=1)
    max_date = datetime.utcnow().replace(day=1)
    months = pd.date_range(min_date, max_date, freq="MS")

    records = []
    for month_start in months:
        month_end = (month_start + pd.offsets.MonthEnd(0)).to_pydatetime()
        active_mask = (subscriptions["subscription_start_date"] <= month_end) & (
            (subscriptions["subscription_end_date"].isna()) | (subscriptions["subscription_end_date"] >= month_start)
        )
        active_subs = subscriptions[active_mask]
        mrr = active_subs["mrr"].sum()

        churned_mask = subscriptions["subscription_end_date"].between(month_start, month_end, inclusive="both")
        churn_mrr = subscriptions[churned_mask]["mrr"].sum()

        expansion_mrr = mrr * np.random.uniform(0.05, 0.15)
        contraction_mrr = mrr * np.random.uniform(0.01, 0.08)
        new_mrr = max(0.0, mrr - (mrr - churn_mrr))

        records.append(
            {
                "month": month_start,
                "mrr": float(mrr),
                "expansion_mrr": float(expansion_mrr),
                "contraction_mrr": float(contraction_mrr),
                "churn_mrr": float(churn_mrr),
                "new_mrr": float(new_mrr),
            }
        )

    return pd.DataFrame(records)

def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    raw_dir = os.path.join(base_dir, "data", "raw")
    ensure_dirs(raw_dir)

    n_users = 20000
    start_date = "2023-01-01"
    end_date = "2024-06-30"

    print(f"Generating {n_users} users...")
    users = generate_users(n_users, start_date, end_date)
    users.to_csv(os.path.join(raw_dir, "users.csv"), index=False)

    print("Generating subscriptions...")
    subs = generate_subscriptions(users)
    subs.to_csv(os.path.join(raw_dir, "subscriptions.csv"), index=False)

    print("Generating events...")
    events = generate_events(users, start_date, end_date, avg_events_per_user=35)
    events.to_csv(os.path.join(raw_dir, "events.csv"), index=False)

    print("Generating revenue...")
    revenue = generate_revenue(subs)
    revenue.to_csv(os.path.join(raw_dir, "revenue.csv"), index=False)

    print("Done. Files saved under data/raw/.")

if __name__ == "__main__":
    main()
