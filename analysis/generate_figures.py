#!/usr/bin/env python3
"""Generate manuscript-supporting figures from reproduced scenario summaries."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_line(x, y, yerr, ylabel: str, title: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.errorbar(x, y, yerr=yerr, marker="o", capsize=4)
    ax.set_xlabel("Scenario")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.repo.resolve()
    input_dir = args.input or (root / "outputs" / "reproduced")
    output_dir = args.output or (input_dir / "figures")
    output_dir.mkdir(parents=True, exist_ok=True)

    cpn = pd.read_csv(input_dir / "cpn_proxy_scenario_summary.csv")
    proto = pd.read_csv(input_dir / "prototype_scenario_summary.csv")

    save_line(
        cpn["scenario"],
        cpn["throughput_logical_mean"],
        cpn["throughput_logical_ci95_half_width"],
        "Receipts per logical time unit",
        "CPN-proxy logical throughput",
        output_dir / "cpn_proxy_throughput_ci.png",
    )
    save_line(
        cpn["scenario"],
        cpn["receipt_success_percent_mean"],
        cpn["receipt_success_percent_ci95_half_width"],
        "Receipt success (%)",
        "CPN-proxy receipt success",
        output_dir / "cpn_proxy_receipt_success_ci.png",
    )
    save_line(
        proto["scenario"],
        proto["real_receipts_per_sec_mean"],
        proto["real_receipts_per_sec_ci95_half_width"],
        "Receipts/s",
        "Prototype lifecycle-processing rate",
        output_dir / "prototype_receipts_per_second_ci.png",
    )
    save_line(
        proto["scenario"],
        proto["receipt_success_rate_mean"],
        proto["receipt_success_rate_ci95_half_width"],
        "Receipt success (%)",
        "Prototype receipt success",
        output_dir / "prototype_receipt_success_ci.png",
    )
    save_line(
        proto["scenario"],
        proto["reward_gini_mean"],
        proto["reward_gini_ci95_half_width"],
        "Reward Gini",
        "Prototype reward concentration",
        output_dir / "prototype_reward_gini_ci.png",
    )

    print(f"Wrote figures to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
