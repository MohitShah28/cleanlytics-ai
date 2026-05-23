import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_iqr_outliers(df):
    outlier_report = []

    numeric_columns = df.select_dtypes(include=["int64", "float64", "Int64"]).columns

    for col in numeric_columns:
        series = pd.to_numeric(df[col], errors="coerce").dropna()

        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_count = ((series < lower_bound) | (series > upper_bound)).sum()

        if outlier_count > 0:
            outlier_report.append({
                "Column": col,
                "Method": "IQR",
                "Outliers Found": int(outlier_count),
                "Lower Bound": round(lower_bound, 2),
                "Upper Bound": round(upper_bound, 2),
                "Suggested Action": "Review extreme values or cap them"
            })

    return pd.DataFrame(outlier_report)


def detect_zscore_outliers(df, threshold=3):
    outlier_report = []

    numeric_columns = df.select_dtypes(include=["int64", "float64", "Int64"]).columns

    for col in numeric_columns:
        series = pd.to_numeric(df[col], errors="coerce").dropna()

        if series.empty or series.std() == 0:
            continue

        z_scores = (series - series.mean()) / series.std()

        outlier_count = (abs(z_scores) > threshold).sum()

        if outlier_count > 0:
            outlier_report.append({
                "Column": col,
                "Method": "Z-Score",
                "Outliers Found": int(outlier_count),
                "Threshold": threshold,
                "Suggested Action": "Review statistically extreme values"
            })

    return pd.DataFrame(outlier_report)


def detect_isolation_forest_outliers(df):
    numeric_df = df.select_dtypes(include=["int64", "float64", "Int64"]).copy()

    numeric_df = numeric_df.apply(pd.to_numeric, errors="coerce")
    numeric_df = numeric_df.dropna()

    if numeric_df.empty or numeric_df.shape[0] < 10:
        return pd.DataFrame()

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    predictions = model.fit_predict(numeric_df)

    outlier_count = (predictions == -1).sum()

    if outlier_count == 0:
        return pd.DataFrame()

    return pd.DataFrame([{
        "Column": "Multiple Numeric Columns",
        "Method": "Isolation Forest",
        "Outliers Found": int(outlier_count),
        "Suggested Action": "Review suspicious rows detected by ML model"
    }])


def fix_iqr_outliers(df, strategy="cap"):
    fixed_df = df.copy()
    fix_log = []

    numeric_columns = fixed_df.select_dtypes(
        include=["int64", "float64", "Int64"]
    ).columns

    for col in numeric_columns:
        series = pd.to_numeric(fixed_df[col], errors="coerce")

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_mask = (series < lower_bound) | (series > upper_bound)
        outlier_count = outlier_mask.sum()

        if outlier_count == 0:
            continue

        if strategy == "cap":
            fixed_df.loc[series < lower_bound, col] = lower_bound
            fixed_df.loc[series > upper_bound, col] = upper_bound
            action = "Capped outliers"

        elif strategy == "remove":
            fixed_df = fixed_df.loc[~outlier_mask]
            action = "Removed outlier rows"

        elif strategy == "median":
            median_value = series.median()
            fixed_df.loc[outlier_mask, col] = median_value
            action = "Replaced outliers with median"

        else:
            action = "No action (unknown strategy)"

        fix_log.append({
            "Column": col,
            "Outliers Fixed": int(outlier_count),
            "Strategy": strategy,
            "Action": action
        })

    return fixed_df, pd.DataFrame(fix_log)


def fix_zscore_outliers(df, strategy="cap", threshold=3):
    fixed_df = df.copy()
    fix_log = []

    numeric_columns = fixed_df.select_dtypes(
        include=["int64", "float64", "Int64"]
    ).columns

    for col in numeric_columns:
        series = pd.to_numeric(fixed_df[col], errors="coerce")

        if series.std() == 0:
            continue

        z_scores = (series - series.mean()) / series.std()
        outlier_mask = abs(z_scores) > threshold
        outlier_count = outlier_mask.sum()

        if outlier_count == 0:
            continue

        lower_bound = series.mean() - threshold * series.std()
        upper_bound = series.mean() + threshold * series.std()

        if strategy == "cap":
            fixed_df.loc[series < lower_bound, col] = lower_bound
            fixed_df.loc[series > upper_bound, col] = upper_bound
            action = "Capped outliers"

        elif strategy == "remove":
            fixed_df = fixed_df.loc[~outlier_mask]
            action = "Removed outlier rows"

        elif strategy == "median":
            median_value = series.median()
            fixed_df.loc[outlier_mask, col] = median_value
            action = "Replaced outliers with median"

        else:
            action = "No action (unknown strategy)"

        fix_log.append({
            "Column": col,
            "Outliers Fixed": int(outlier_count),
            "Strategy": strategy,
            "Action": action
        })

    return fixed_df, pd.DataFrame(fix_log)
