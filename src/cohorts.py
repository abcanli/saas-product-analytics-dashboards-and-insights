import pandas as pd

def build_signup_cohorts(users: pd.DataFrame) -> pd.DataFrame:
    df = users.copy()
    df["signup_month"] = df["signup_date"].dt.to_period("M").dt.to_timestamp()
    cohorts = df.groupby("signup_month")["user_id"].nunique().reset_index(name="num_users")
    return cohorts

def cohort_retention_matrix(users: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    df_users = users.copy()
    df_events = events.copy()
    df_users["signup_month"] = df_users["signup_date"].dt.to_period("M").dt.to_timestamp()
    df_events["event_month"] = df_events["event_timestamp"].dt.to_period("M").dt.to_timestamp()
    merged = df_events.merge(df_users[["user_id", "signup_month"]], on="user_id", how="left")
    merged["months_since_signup"] = (
        (merged["event_month"].dt.to_period("M") - merged["signup_month"].dt.to_period("M")).apply(lambda p: p.n)
    )
    merged = merged[merged["months_since_signup"] >= 0]
    cohort_pivot = merged.groupby(["signup_month", "months_since_signup"])["user_id"].nunique().reset_index()
    cohort_sizes = df_users.groupby("signup_month")["user_id"].nunique().rename("cohort_size")
    cohort_pivot = cohort_pivot.merge(cohort_sizes, on="signup_month")
    cohort_pivot["retention"] = cohort_pivot["user_id"] / cohort_pivot["cohort_size"]
    matrix = cohort_pivot.pivot_table(index="signup_month", columns="months_since_signup", values="retention").fillna(0.0)
    matrix.columns = [f"m+{c}" for c in matrix.columns]
    return matrix
