import io
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class FormatReport:
    delimiter_name: str
    was_reformatted: bool
    original_columns: int
    formatted_columns: int
    message: str


def _read_candidate(file_bytes, delimiter_name, read_kwargs):
    buffer = io.BytesIO(file_bytes)
    df = pd.read_csv(buffer, **read_kwargs)
    df = df.dropna(axis=1, how="all")
    return delimiter_name, df


def _has_packed_text_column(df):
    if df.shape[1] != 1 or df.empty:
        return False

    column_name = str(df.columns[0])
    sample_values = df.iloc[:5, 0].astype(str).tolist()
    packed_values = sum(len(value.split()) > 3 for value in sample_values)

    return len(column_name.split()) > 3 or packed_values >= 2


def _score_candidate(df):
    if df.empty:
        return -100

    score = df.shape[1] * 12
    score += min(df.shape[0], 20)

    if _has_packed_text_column(df):
        score -= 80

    unnamed_columns = sum(str(col).lower().startswith("unnamed") for col in df.columns)
    score -= unnamed_columns * 8

    missing_ratio = df.isna().sum().sum() / max(df.shape[0] * df.shape[1], 1)
    score -= missing_ratio * 10

    return score


def read_csv_with_auto_format(uploaded_file):
    file_bytes = uploaded_file.getvalue()

    candidates = [
        ("comma", {"sep": ","}),
        ("semicolon", {"sep": ";"}),
        ("tab", {"sep": "\t"}),
        ("pipe", {"sep": "|"}),
        ("whitespace", {"sep": r"\s+", "engine": "python"}),
        ("auto-detected", {"sep": None, "engine": "python"}),
    ]

    parsed_candidates = []
    errors = []

    for delimiter_name, read_kwargs in candidates:
        try:
            parsed_candidates.append(
                _read_candidate(file_bytes, delimiter_name, read_kwargs)
            )
        except Exception as exc:
            errors.append(f"{delimiter_name}: {exc}")

    if not parsed_candidates:
        raise ValueError(
            "Could not read this CSV file with common separators. "
            + " | ".join(errors)
        )

    default_df = next(
        df for delimiter_name, df in parsed_candidates if delimiter_name == "comma"
    )

    best_delimiter, best_df = max(
        parsed_candidates,
        key=lambda candidate: _score_candidate(candidate[1])
    )

    was_reformatted = best_delimiter != "comma" or _has_packed_text_column(default_df)

    if was_reformatted:
        message = (
            f"Auto-formatted upload using {best_delimiter} separation. "
            f"Converted {default_df.shape[1]} raw column(s) into "
            f"{best_df.shape[1]} structured column(s)."
        )
    else:
        message = "File format looks structured. No automatic reformatting was needed."

    return best_df, FormatReport(
        delimiter_name=best_delimiter,
        was_reformatted=was_reformatted,
        original_columns=default_df.shape[1],
        formatted_columns=best_df.shape[1],
        message=message
    )
