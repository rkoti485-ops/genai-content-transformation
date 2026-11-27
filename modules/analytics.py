"""Analytics for AI content transformation activity."""

import pandas as pd
from modules.database import get_history


def get_analytics():
    """Calculate writing analytics from saved history."""

    records = get_history()

    columns = [
        "id", "created_at", "source_name",
        "task", "word_count", "output", "model"
    ]

    df = pd.DataFrame(records, columns=columns)

    if df.empty:
        empty_tasks = pd.DataFrame(columns=["task", "count"])
        empty_recent = pd.DataFrame(
            columns=["created_at", "source_name", "task", "word_count"]
        )

        return {
            "total": 0,
            "words": 0,
            "top_task": "No activity yet",
            "by_task": empty_tasks,
            "recent": empty_recent,
            "csv": df.to_csv(index=False)
        }

    df["word_count"] = pd.to_numeric(
        df["word_count"], errors="coerce"
    ).fillna(0)

    df["task"] = df["task"].fillna("Unknown")

    by_task = (
        df.groupby("task")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    top_task = by_task.iloc[0]["task"]

    recent = df[
        ["created_at", "source_name", "task", "word_count"]
    ].head(10)

    return {
        "total": int(len(df)),
        "words": int(df["word_count"].sum()),
        "top_task": str(top_task),
        "by_task": by_task,
        "recent": recent,
        "csv": df.to_csv(index=False)
    }


def get_analytics_dataframe():
    """Return the complete history as a Pandas DataFrame."""
    records = get_history()
    return pd.DataFrame(records)