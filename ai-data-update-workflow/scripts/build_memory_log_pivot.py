#!/usr/bin/env python3
"""Build pivot-style Excel summaries from raw memory and operation log CSV files.

This script is intentionally small and explicit so beginners can adapt the
field names to their own exports.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


MEMORY_REQUIRED = {
    "memory_id",
    "user_id",
    "created_at",
    "scene",
    "intent_level",
    "risk_flag",
    "tags",
}

LOG_REQUIRED = {
    "log_id",
    "user_id",
    "created_at",
    "operator",
    "channel",
    "event_type",
}


def require_columns(frame: pd.DataFrame, required: set[str], name: str) -> list[str]:
    missing = sorted(required - set(frame.columns))
    if missing:
        raise SystemExit(f"{name} missing columns: {missing}")
    return sorted(required)


def add_date(frame: pd.DataFrame, source_name: str) -> pd.DataFrame:
    frame = frame.copy()
    frame["created_at"] = pd.to_datetime(frame["created_at"], errors="coerce")
    bad_dates = frame["created_at"].isna().sum()
    if bad_dates:
        raise SystemExit(f"{source_name} has {bad_dates} bad created_at values")
    frame["date"] = frame["created_at"].dt.date.astype(str)
    return frame


def filter_period(frame: pd.DataFrame, start: str | None, end: str | None) -> pd.DataFrame:
    if not start and not end:
        return frame
    created = frame["created_at"]
    mask = pd.Series(True, index=frame.index)
    if start:
        mask &= created >= pd.to_datetime(start)
    if end:
        mask &= created < pd.to_datetime(end) + pd.Timedelta(days=1)
    return frame.loc[mask].copy()


def build_memory_by_scene(memory: pd.DataFrame) -> pd.DataFrame:
    grouped = memory.groupby(["date", "scene"], dropna=False)
    result = grouped.agg(
        memory_count=("memory_id", "nunique"),
        active_users=("user_id", "nunique"),
        high_intent_users=(
            "user_id",
            lambda s: s[memory.loc[s.index, "intent_level"].eq("high")].nunique(),
        ),
        risk_users=(
            "user_id",
            lambda s: s[memory.loc[s.index, "risk_flag"].astype(str).isin(["1", "true", "True"])].nunique(),
        ),
    )
    return result.reset_index()


def build_logs_by_operator(logs: pd.DataFrame) -> pd.DataFrame:
    pivot = pd.pivot_table(
        logs,
        index=["date", "operator", "channel"],
        columns="event_type",
        values="log_id",
        aggfunc="nunique",
        fill_value=0,
    )
    pivot.columns = [str(col) for col in pivot.columns]
    pivot["total_logs"] = pivot.sum(axis=1)
    return pivot.reset_index()


def build_tag_frequency(memory: pd.DataFrame) -> pd.DataFrame:
    tag_rows = memory[["date", "scene", "user_id", "tags"]].copy()
    tag_rows["tag"] = tag_rows["tags"].fillna("").astype(str).str.split(",")
    tag_rows = tag_rows.explode("tag")
    tag_rows["tag"] = tag_rows["tag"].str.strip()
    tag_rows = tag_rows[tag_rows["tag"] != ""]
    if tag_rows.empty:
        return pd.DataFrame(columns=["date", "scene", "tag", "tag_count", "tag_users"])
    return (
        tag_rows.groupby(["date", "scene", "tag"], dropna=False)
        .agg(tag_count=("tag", "size"), tag_users=("user_id", "nunique"))
        .reset_index()
        .sort_values(["date", "scene", "tag_count"], ascending=[True, True, False])
    )


def build_quality_checks(memory: pd.DataFrame, logs: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {"check": "memory_rows", "value": len(memory)},
        {"check": "log_rows", "value": len(logs)},
        {"check": "memory_users", "value": memory["user_id"].nunique()},
        {"check": "log_users", "value": logs["user_id"].nunique()},
        {"check": "duplicate_memory_id", "value": memory["memory_id"].duplicated().sum()},
        {"check": "duplicate_log_id", "value": logs["log_id"].duplicated().sum()},
        {"check": "memory_date_min", "value": memory["date"].min() if len(memory) else ""},
        {"check": "memory_date_max", "value": memory["date"].max() if len(memory) else ""},
        {"check": "log_date_min", "value": logs["date"].min() if len(logs) else ""},
        {"check": "log_date_max", "value": logs["date"].max() if len(logs) else ""},
    ]
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", required=True, help="Raw memory CSV path")
    parser.add_argument("--logs", required=True, help="Raw operation log CSV path")
    parser.add_argument("--output", default="memory_log_pivot.xlsx", help="Output Excel path")
    parser.add_argument("--start", help="Inclusive start date, e.g. 2026-07-01")
    parser.add_argument("--end", help="Inclusive end date, e.g. 2026-07-07")
    args = parser.parse_args()

    memory = pd.read_csv(args.memory)
    logs = pd.read_csv(args.logs)
    require_columns(memory, MEMORY_REQUIRED, "memory")
    require_columns(logs, LOG_REQUIRED, "logs")

    memory = filter_period(add_date(memory, "memory"), args.start, args.end)
    logs = filter_period(add_date(logs, "logs"), args.start, args.end)

    output = Path(args.output)
    with pd.ExcelWriter(output) as writer:
        build_memory_by_scene(memory).to_excel(writer, sheet_name="memory_by_scene", index=False)
        build_logs_by_operator(logs).to_excel(writer, sheet_name="logs_by_operator", index=False)
        build_tag_frequency(memory).to_excel(writer, sheet_name="tag_frequency", index=False)
        build_quality_checks(memory, logs).to_excel(writer, sheet_name="quality_checks", index=False)

    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
