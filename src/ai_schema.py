import pandas as pd


def ai_dtype_suggestion(series, column_name):
    non_null = series.dropna()

    if non_null.empty:
        return {
            "suggested_type": "object",
            "confidence": 0,
            "reason": "Column is empty, so object is safest."
        }

    sample = non_null.astype(str).str.strip()
    total = len(sample)
    col_lower = column_name.lower()

    if "id" in col_lower or col_lower.endswith("_id"):
        return {
            "suggested_type": "object",
            "confidence": 95,
            "reason": "Column name looks like an ID. IDs should usually stay as text."
        }

    bool_values = {"true", "false", "yes", "no", "y", "n", "0", "1"}
    bool_ratio = sample.str.lower().isin(bool_values).mean()

    if bool_ratio > 0.9 and sample.nunique() <= 2:
        return {
            "suggested_type": "bool",
            "confidence": round(bool_ratio * 100, 2),
            "reason": "Most values are boolean-like."
        }

    cleaned_numeric = (
        sample
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
    )

    numeric_values = pd.to_numeric(cleaned_numeric, errors="coerce")
    numeric_ratio = numeric_values.notna().mean()

    if numeric_ratio > 0.9:
        numeric_non_null = numeric_values.dropna()

        if not numeric_non_null.empty:
            if (numeric_non_null % 1 == 0).all():
                return {
                    "suggested_type": "int",
                    "confidence": round(numeric_ratio * 100, 2),
                    "reason": "Most values are numeric whole numbers."
                }

            return {
                "suggested_type": "float",
                "confidence": round(numeric_ratio * 100, 2),
                "reason": "Most values are numeric with decimal values."
            }

    date_keywords = [
        "date", "created", "updated",
        "dob", "birth", "joined", "timestamp"
    ]

    looks_like_date_column = any(word in col_lower for word in date_keywords)

    date_patterns = sample.str.contains(
        r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}|[A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4}",
        regex=True,
        na=False
    ).mean()

    if looks_like_date_column:
        datetime_values = pd.to_datetime(sample, errors="coerce")
        datetime_ratio = datetime_values.notna().mean()

        if datetime_ratio > 0.75 or date_patterns > 0.6:
            return {
                "suggested_type": "datetime",
                "confidence": round(max(datetime_ratio, date_patterns) * 100, 2),
                "reason": "Column name and values look like dates."
            }

    unique_ratio = sample.nunique() / total

    if unique_ratio < 0.3:
        return {
            "suggested_type": "category",
            "confidence": round((1 - unique_ratio) * 100, 2),
            "reason": "Column has repeated limited values."
        }

    return {
        "suggested_type": "object",
        "confidence": 80,
        "reason": "Column contains general text or mixed values."
    }
