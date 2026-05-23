import pandas as pd


def clean_data(
    df,
    dtype_changes,
    remove_duplicates,
    fill_missing,
    drop_missing,
    standardize_columns
):
    cleaned_df = df.copy()
    cleaning_log = []

    # APPLY USER SELECTED DATA TYPES
    for col, selected_dtype in dtype_changes.items():
        if selected_dtype == "int":
            cleaned_df[col] = pd.to_numeric(
                cleaned_df[col],
                errors="coerce"
            ).astype("Int64")

        elif selected_dtype == "float":
            cleaned_df[col] = pd.to_numeric(
                cleaned_df[col],
                errors="coerce"
            )

        elif selected_dtype == "datetime":
            cleaned_df[col] = pd.to_datetime(
                cleaned_df[col],
                errors="coerce"
            )

        elif selected_dtype == "category":
            cleaned_df[col] = cleaned_df[col].astype("category")

        elif selected_dtype == "bool":
            cleaned_df[col] = cleaned_df[col].astype("bool")

        else:
            cleaned_df[col] = cleaned_df[col].astype("object")

    # REMOVE DUPLICATES
    if remove_duplicates:
        before_count = cleaned_df.shape[0]
        cleaned_df = cleaned_df.drop_duplicates()
        after_count = cleaned_df.shape[0]
        removed = before_count - after_count
        cleaning_log.append({
            "Action": "Removed Duplicates",
            "Rows Affected": removed
        })

    # FILL MISSING VALUES
    if fill_missing:
        for col in cleaned_df.columns:
            missing_before = cleaned_df[col].isnull().sum()

            if cleaned_df[col].dtype == "object":
                cleaned_df[col] = (
                    cleaned_df[col]
                    .fillna("Unknown")
                )
            else:
                cleaned_df[col] = (
                    cleaned_df[col]
                    .fillna(cleaned_df[col].median())
                )

            cleaning_log.append({
                "Action": f"Filled Missing Values in {col}",
                "Rows Affected": missing_before
            })

    # DROP MISSING ROWS
    if drop_missing:
        before_rows = cleaned_df.shape[0]
        cleaned_df = cleaned_df.dropna()
        after_rows = cleaned_df.shape[0]
        dropped_rows = before_rows - after_rows
        cleaning_log.append({
            "Action": "Dropped Missing Rows",
            "Rows Affected": dropped_rows
        })

    # STANDARDIZE COLUMN NAMES
    if standardize_columns:
        cleaned_df.columns = [
            col.strip()
            .lower()
            .replace(" ", "_")
            for col in cleaned_df.columns
        ]
        cleaning_log.append({
            "Action": "Standardized Column Names",
            "Rows Affected": len(cleaned_df.columns)
        })

    return cleaned_df, cleaning_log
