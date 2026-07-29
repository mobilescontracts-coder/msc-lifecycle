#!/usr/bin/env python3
"""Patch an SPoS-MSC benchmark .cpn file for one five-policy benchmark block.

The benchmark model uses five isolated slots, one per policy:
  slot 1 = MSC_NATIVE       mode 10
  slot 2 = TRAD_POS         mode 20
  slot 3 = ROUND_ROBIN      mode 30
  slot 4 = RANDOM_COMMITTEE mode 40
  slot 5 = FULL_SPOS        mode 50

For statistical experiments, run one block at a time in CPN Tools, export
P_ResultArchive, then rewind/open the next patched model.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

MODES = [(1, 1, 10), (2, 2, 20), (3, 3, 30), (4, 4, 40), (5, 5, 50)]


def build_run_queue_marking(
    scenario: int, seed: int, expected_tx: int, ablation: int = 0
) -> str:
    parts = []
    for slot, run_id, mode in MODES:
        parts.append(f"1`({slot},{run_id},{scenario},{seed},{mode},{ablation},{expected_tx})")
    return " ++\n".join(parts)


def replace_place_initmark(xml: str, place_text: str, new_marking: str) -> str:
    place_pattern = re.compile(
        rf"(<place\b[^>]*>.*?<text>{re.escape(place_text)}</text>.*?</place>)",
        re.DOTALL,
    )
    match = place_pattern.search(xml)
    if not match:
        raise ValueError(f"Could not find place text {place_text!r}")
    place_block = match.group(1)

    init_pattern = re.compile(
        r"(<initmark\b[^>]*>.*?<text\b[^>]*>)(.*?)(</text>.*?</initmark>)",
        re.DOTALL,
    )
    init_match = init_pattern.search(place_block)
    if not init_match:
        raise ValueError(f"Could not find initmark for place {place_text!r}")
    escaped = html.escape(new_marking, quote=False)
    new_place_block = (
        place_block[: init_match.start(2)]
        + escaped
        + place_block[init_match.end(2) :]
    )
    return xml[: match.start(1)] + new_place_block + xml[match.end(1) :]


def patch_cpn(
    base_path: Path,
    output_path: Path,
    scenario: int,
    seed: int,
    expected_tx: int,
    ablation: int,
    timeout: int | None,
) -> None:
    xml = base_path.read_text(encoding="iso-8859-1")
    marking = build_run_queue_marking(scenario, seed, expected_tx, ablation)
    xml = replace_place_initmark(xml, "P_RunQueue", marking)
    xml = replace_place_initmark(xml, "P_RemainingRuns", "1`5")
    if timeout is not None:
        xml = re.sub(
            r"val\s+BENCH_TIMEOUT\s*:\s*int\s*=\s*\d+\s*;",
            f"val BENCH_TIMEOUT:int = {timeout};",
            xml,
        )
    output_path.write_text(xml, encoding="iso-8859-1", newline="\r\n")
    print(f"Wrote {output_path}")
    print("P_RunQueue initial marking:")
    print(marking)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="Base .cpn file")
    parser.add_argument("--out", required=True, help="Patched output .cpn file")
    parser.add_argument("--scenario", type=int, default=6)
    parser.add_argument("--seed", type=int, default=626)
    parser.add_argument("--expected-tx", type=int, default=2)
    parser.add_argument("--ablation", type=int, default=0)
    parser.add_argument(
        "--timeout", type=int, default=None, help="Optional replacement for BENCH_TIMEOUT"
    )
    args = parser.parse_args()
    if not 1 <= args.expected_tx <= 50:
        raise SystemExit("expected-tx must be in 1..50 for the current workload constructor")
    patch_cpn(
        Path(args.base),
        Path(args.out),
        args.scenario,
        args.seed,
        args.expected_tx,
        args.ablation,
        args.timeout,
    )


if __name__ == "__main__":
    main()
