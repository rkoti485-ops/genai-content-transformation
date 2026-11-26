import pandas as pd
from modules.database import get_history

def get_analytics():
    rows = get_history(limit=10000)
    columns = ["id", "created_at", "source_name", "task", "word_count", "output", "model"]
    df = pd.DataFrame(rows, columns=columns)
    if df.empty:
        return {
            "total": 0, "words": 0, "top_task": "—",
            "by_task": pd.DataFrame(columns=["task", "count"]),
            "recent": df, "csv": "id,created_at,source_name,task,word_count,model\n"
        }
    grouped = df.groupby("task").size().reset_index(name="count").sort_values("count", ascending=False)
    return {
        "total": len(df),
        "words": int(df["word_count"].fillna(0).sum()),
        "top_task": str(grouped.iloc[0]["task"]),
        "by_task": grouped,
        "recent": df[["created_at", "source_name", "task", "word_count", "model"]].head(20),
        "csv": df.drop(columns=["output"]).to_csv(index=False)
    }
