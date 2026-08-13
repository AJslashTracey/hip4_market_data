#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parent
SAMPLES_ROOT = REPO_ROOT / "data" / "samples"
VISUALS_ROOT = REPO_ROOT / "docs" / "assets" / "visuals"


def configure_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#374151",
            "axes.grid": True,
            "grid.color": "#d7dde5",
            "grid.linewidth": 0.8,
            "grid.alpha": 0.7,
            "font.size": 10,
            "axes.titlesize": 10,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "savefig.dpi": 180,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def load_metadata(sample_dir: Path) -> dict[str, object]:
    with (sample_dir / "metadata.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                return json.loads(line)
    raise ValueError(f"No metadata found in {sample_dir}")


def load_mids(sample_dir: Path) -> pd.DataFrame:
    mids = pd.read_csv(sample_dir / "rest_mid_samples.csv")
    mids["ts"] = pd.to_datetime(mids["ts"], utc=True, format="mixed")
    mids["mid_price"] = pd.to_numeric(mids["mid_price"], errors="coerce")
    return mids


def load_bbo_series(sample_dir: Path, coin: str) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    with (sample_dir / "ws_bbo.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            obj = json.loads(line)
            data = obj.get("payload", {}).get("data", {})
            if data.get("coin") != coin:
                continue
            bbo = data.get("bbo") or [None, None]
            bid, ask = bbo
            if not bid or not ask:
                continue
            bid_px = float(bid["px"])
            ask_px = float(ask["px"])
            rows.append(
                {
                    "ts": pd.to_datetime(obj["ts"], utc=True),
                    "mid": (bid_px + ask_px) / 2.0,
                }
            )
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    frame = frame.sort_values("ts").drop_duplicates("ts", keep="last").reset_index(drop=True)
    frame["dmid"] = frame["mid"].diff()
    return frame


def lag_curve(game_bbo: pd.DataFrame, champion_bbo: pd.DataFrame, max_lag_s: int = 15) -> pd.DataFrame:
    if game_bbo.empty or champion_bbo.empty:
        return pd.DataFrame(columns=["lag_s", "corr", "samples"])
    game_ret = game_bbo.set_index("ts")["mid"].resample("1s").last().ffill().diff().rename("game_ret")
    champ_ret = champion_bbo.set_index("ts")["mid"].resample("1s").last().ffill().diff().rename("champ_ret")
    joined = pd.concat([game_ret, champ_ret], axis=1).dropna()
    rows: list[dict[str, object]] = []
    for lag_s in range(-max_lag_s, max_lag_s + 1):
        shifted = joined["champ_ret"].shift(-lag_s)
        sample = pd.concat([joined["game_ret"], shifted.rename("champ_shifted")], axis=1).dropna()
        if len(sample) < 20:
            continue
        rows.append(
            {
                "lag_s": lag_s,
                "corr": float(sample["game_ret"].corr(sample["champ_shifted"])),
                "samples": int(len(sample)),
            }
        )
    return pd.DataFrame(rows)


def event_responses(game_bbo: pd.DataFrame, champion_bbo: pd.DataFrame) -> pd.DataFrame:
    if game_bbo.empty or champion_bbo.empty:
        return pd.DataFrame(columns=["jump_bps", "champ_move_5s_bps", "response_s"])

    threshold = max(float(game_bbo["dmid"].abs().quantile(0.9)), 0.01)
    response_threshold = max(float(champion_bbo["mid"].diff().abs().quantile(0.75)), 0.0015)
    events = game_bbo[game_bbo["dmid"].abs() >= threshold].copy()
    rows: list[dict[str, object]] = []
    for _, event in events.iterrows():
        ts = event["ts"]
        direction = 1.0 if event["dmid"] > 0 else -1.0
        champion_pre = champion_bbo[champion_bbo["ts"] < ts].tail(1)
        champion_post = champion_bbo[
            (champion_bbo["ts"] >= ts) & (champion_bbo["ts"] <= ts + pd.Timedelta(seconds=8))
        ].copy()
        if champion_pre.empty or champion_post.empty:
            continue
        baseline = float(champion_pre.iloc[0]["mid"])
        champion_post["move"] = champion_post["mid"] - baseline
        move_5s = champion_post[champion_post["ts"] <= ts + pd.Timedelta(seconds=5)]
        same_direction = champion_post[champion_post["move"] * direction > response_threshold]
        rows.append(
            {
                "jump_bps": float(event["dmid"] * 10_000),
                "champ_move_5s_bps": None
                if move_5s.empty
                else float(move_5s.iloc[-1]["move"] * 10_000),
                "response_s": None
                if same_direction.empty
                else float((same_direction.iloc[0]["ts"] - ts).total_seconds()),
            }
        )
    return pd.DataFrame(rows)


def add_panel_label(ax: plt.Axes, text: str) -> None:
    ax.text(0.0, 1.03, text, transform=ax.transAxes, ha="left", va="bottom", fontweight="bold")


def format_time_axis(ax: plt.Axes) -> None:
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))


def render_argentina_egypt() -> Path:
    sample_dir = SAMPLES_ROOT / "argentina_egypt_live"
    mids = load_mids(sample_dir)

    sides = {
        "Argentina": {"game": "#7510", "champion": "#1730", "color": "#0f4c81"},
        "Egypt": {"game": "#7511", "champion": "#c65d21", "color": "#c65d21"},
    }

    bbo = {
        side: {
            market: load_bbo_series(sample_dir, coin)
            for market, coin in (("game", cfg["game"]), ("champion", cfg["champion"]))
        }
        for side, cfg in sides.items()
    }

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax_moves, ax_lag, ax_scatter, ax_response = axes.flat

    for side, cfg in sides.items():
        color = cfg["color"]
        for market, linestyle in (("game", "-"), ("champion", (0, (4, 2)))):
            series = mids[mids["coin"] == cfg[market]].sort_values("ts").copy()
            if series.empty:
                continue
            series["move_bps"] = (series["mid_price"] - series["mid_price"].iloc[0]) * 10_000
            ax_moves.plot(
                series["ts"],
                series["move_bps"],
                color=color,
                linestyle=linestyle,
                linewidth=1.8,
                label=f"{side} {market}",
            )
    add_panel_label(ax_moves, "Moves from sample start")
    ax_moves.set_ylabel("bps")
    format_time_axis(ax_moves)
    ax_moves.legend(frameon=False, ncol=2, loc="upper left")

    for side, cfg in sides.items():
        curve = lag_curve(bbo[side]["game"], bbo[side]["champion"])
        if curve.empty:
            continue
        ax_lag.plot(curve["lag_s"], curve["corr"], color=cfg["color"], linewidth=2.0, label=side)
        best = curve.iloc[curve["corr"].abs().idxmax()]
        ax_lag.scatter([best["lag_s"]], [best["corr"]], color=cfg["color"], s=28, zorder=3)
    ax_lag.axvline(0, color="#6b7280", linestyle="--", linewidth=1.0)
    add_panel_label(ax_lag, "Lag curve")
    ax_lag.set_xlabel("champion lag vs game (seconds)")
    ax_lag.set_ylabel("corr")
    ax_lag.legend(frameon=False, loc="upper left")

    for side, cfg in sides.items():
        responses = event_responses(bbo[side]["game"], bbo[side]["champion"])
        if responses.empty:
            continue
        ax_scatter.scatter(
            responses["jump_bps"],
            responses["champ_move_5s_bps"],
            color=cfg["color"],
            alpha=0.8,
            s=28,
            label=side,
        )
        response_times = responses.dropna(subset=["response_s"])
        if not response_times.empty:
            ax_response.scatter(
                response_times["jump_bps"].abs(),
                response_times["response_s"],
                color=cfg["color"],
                alpha=0.8,
                s=28,
                label=side,
            )
    ax_scatter.axhline(0, color="#6b7280", linestyle="--", linewidth=1.0)
    ax_scatter.axvline(0, color="#6b7280", linestyle="--", linewidth=1.0)
    add_panel_label(ax_scatter, "Event jump vs 5s champion move")
    ax_scatter.set_xlabel("game jump (bps)")
    ax_scatter.set_ylabel("champion move after 5s (bps)")
    ax_scatter.legend(frameon=False, loc="upper left")

    add_panel_label(ax_response, "Jump size vs response time")
    ax_response.set_xlabel("|game jump| (bps)")
    ax_response.set_ylabel("response time (s)")
    ax_response.legend(frameon=False, loc="upper left")

    fig.tight_layout()
    out_path = VISUALS_ROOT / "argentina_egypt_cross_market_lag_detail.png"
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return out_path


def render_france_sweden() -> Path:
    sample_dir = SAMPLES_ROOT / "france_sweden_orderbook_live"
    mids = load_mids(sample_dir)
    events = pd.read_csv(sample_dir / "orderbook_pressure_events.csv")
    events["ts"] = pd.to_datetime(events["ts"], utc=True, format="mixed")
    events["is_impulse"] = events["is_impulse"].astype(str).str.lower() == "true"
    events = events[events["is_impulse"]].copy()
    events["pressure_notional_k"] = (events["bid_top_notional_delta"] - events["ask_top_notional_delta"]) / 1000.0
    events["mid_move_bps"] = events["mid_move"] * 10_000

    focus = {
        "#6740": {"label": "France game", "color": "#0f4c81", "linestyle": "-"},
        "#6741": {"label": "Sweden game", "color": "#c65d21", "linestyle": "-"},
        "#1890": {"label": "France champion", "color": "#0f4c81", "linestyle": (0, (4, 2))},
        "#2130": {"label": "Sweden champion", "color": "#c65d21", "linestyle": (0, (4, 2))},
    }

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax_moves, ax_time, ax_box, ax_scatter = axes.flat

    for coin, cfg in focus.items():
        series = mids[mids["coin"] == coin].sort_values("ts").copy()
        if series.empty:
            continue
        series["move_bps"] = (series["mid_price"] - series["mid_price"].iloc[0]) * 10_000
        ax_moves.plot(
            series["ts"],
            series["move_bps"],
            color=cfg["color"],
            linestyle=cfg["linestyle"],
            linewidth=1.8,
            label=cfg["label"],
        )
    add_panel_label(ax_moves, "Moves from sample start")
    ax_moves.set_ylabel("bps")
    format_time_axis(ax_moves)
    ax_moves.legend(frameon=False, ncol=2, loc="upper left")

    for coin, cfg in focus.items():
        points = events[events["coin"] == coin]
        if points.empty:
            continue
        ax_time.scatter(
            points["ts"],
            points["pressure_notional_k"],
            color=cfg["color"],
            alpha=0.55 if "champion" in cfg["label"] else 0.8,
            s=18,
            label=cfg["label"],
        )
    ax_time.axhline(0, color="#6b7280", linestyle="--", linewidth=1.0)
    add_panel_label(ax_time, "Impulse pressure over time")
    ax_time.set_ylabel("signed notional change (k)")
    format_time_axis(ax_time)
    ax_time.legend(frameon=False, ncol=2, loc="upper left")

    box_data = []
    box_labels = []
    for coin, cfg in focus.items():
        values = events.loc[events["coin"] == coin, "pressure_notional_k"].dropna()
        if values.empty:
            continue
        box_data.append(values)
        box_labels.append(cfg["label"].replace(" ", "\n"))
    if box_data:
        ax_box.boxplot(box_data, tick_labels=box_labels, patch_artist=True)
    add_panel_label(ax_box, "Pressure distribution")
    ax_box.set_ylabel("signed notional change (k)")

    for coin, cfg in focus.items():
        points = events[events["coin"] == coin]
        if points.empty:
            continue
        ax_scatter.scatter(
            points["pressure_notional_k"],
            points["mid_move_bps"],
            color=cfg["color"],
            alpha=0.7,
            s=18,
            label=cfg["label"],
        )
    ax_scatter.axhline(0, color="#6b7280", linestyle="--", linewidth=1.0)
    ax_scatter.axvline(0, color="#6b7280", linestyle="--", linewidth=1.0)
    add_panel_label(ax_scatter, "Pressure vs immediate mid move")
    ax_scatter.set_xlabel("signed notional change (k)")
    ax_scatter.set_ylabel("mid move (bps)")
    ax_scatter.legend(frameon=False, ncol=2, loc="upper left")

    fig.tight_layout()
    out_path = VISUALS_ROOT / "france_sweden_orderbook_detail.png"
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> int:
    VISUALS_ROOT.mkdir(parents=True, exist_ok=True)
    configure_style()
    outputs = [render_argentina_egypt(), render_france_sweden()]
    for path in outputs:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
