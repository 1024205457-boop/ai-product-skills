#!/usr/bin/env python3
"""Build pivot-style Excel summaries from raw user-state and touch-history CSV files.

This script is intentionally small and explicit so beginners can adapt the
field names to their own exports.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


STATE_REQUIRED = {
    "state_id",
    "user_id",
    "created_at",
    "scene",
    "intent_level",
    "risk_flag",
    "tags",
}

TOUCH_REQUIRED = {
    "touch_id",
    "user_id",
    "created_at",
    "operator",
    "channel",
    "event_type",
}


def require_columns(frame: pd.DataFrame, required: set[str], name: str) -> None:
    missing = sorted(required - set(frame.columns))
    if missing:
        raise SystemExit(f"{name} missing columns: {missing}")


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


def build_state_by_scene(state: pd.DataFrame) -> pd.DataFrame:
    grouped = state.groupby(["date", "scene"], dropna=False)
    result = grouped.agg(
        state_count=("state_id", "nunique"),
        active_users=("user_id", "nunique"),
        high_intent_users=(
            "user_id",
            lambda s: s[state.loc[s.index, "intent_level"].eq("high")].nunique(),
        ),
        risk_users=(
            "user_id",
            lambda s: s[state.loc[s.index, "risk_flag"].astype(str).isin(["1", "true", "True"])].nunique(),
        ),
    )
    return result.reset_index()


def build_touch_by_operator(touch: pd.DataFrame) -> pd.DataFrame:
    pivot = pd.pivot_table(
        touch,
        index=["date", "operator", "channel"],
        columns="event_type",
        values="touch_id",
        aggfunc="nunique",
        fill_value=0,
    )
    pivot.columns = [str(col) for col in pivot.columns]
    pivot["total_touch"] = pivot.sum(axis=1)
    return pivot.reset_index()


def build_tag_frequency(state: pd.DataFrame) -> pd.DataFrame:
    tag_rows = state[["date", "scene", "user_id", "tags"]].copy()
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


def build_quality_checks(state: pd.DataFrame, touch: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {"check": "state_rows", "value": len(state)},
        {"check": "touch_rows", "value": len(touch)},
        {"check": "state_users", "value": state["user_id"].nunique()},
        {"check": "touch_users", "value": touch["user_id"].nunique()},
        {"check": "duplicate_state_id", "value": state["state_id"].duplicated().sum()},
        {"check": "duplicate_touch_id", "value": touch["touch_id"].duplicated().sum()},
        {"check": "state_date_min", "value": state["date"].min() if len(state) else ""},
        {"check": "state_date_max", "value": state["date"].max() if len(state) else ""},
        {"check": "touch_date_min", "value": touch["date"].min() if len(touch) else ""},
        {"check": "touch_date_max", "value": touch["date"].max() if len(touch) else ""},
    ]
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, help="Raw user-state CSV path")
    parser.add_argument("--touch", required=True, help="Raw touch-history CSV path")
    parser.add_argument("--output", default="detail_pivot.xlsx", help="Output Excel path")
    parser.add_argument("--start", help="Inclusive start date, e.g. 2026-07-01")
    parser.add_argument("--end", help="Inclusive end date, e.g. 2026-07-07")
    args = parser.parse_args()

    state = pd.read_csv(args.state)
    touch = pd.read_csv(args.touch)
    require_columns(state, STATE_REQUIRED, "state")
    require_columns(touch, TOUCH_REQUIRED, "touch")

    state = filter_period(add_date(state, "state"), args.start, args.end)
    touch = filter_period(add_date(touch, "touch"), args.start, args.end)

    output = Path(args.output)
    with pd.ExcelWriter(output) as writer:
        build_state_by_scene(state).to_excel(writer, sheet_name="state_by_scene", index=False)
        build_touch_by_operator(touch).to_excel(writer, sheet_name="touch_by_operator", index=False)
        build_tag_frequency(state).to_excel(writer, sheet_name="tag_frequency", index=False)
        build_quality_checks(state, touch).to_excel(writer, sheet_name="quality_checks", index=False)

    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
