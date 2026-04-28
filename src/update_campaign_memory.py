from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .campaigns import (
        DEFAULT_CAMPAIGNS_DIR,
        copy_current_output_to_pack,
        load_campaign,
        pack_id_from_number,
        update_memory_from_pack,
        campaign_memory_path,
        campaign_summary_path,
    )
except ImportError:
    from campaigns import (
        DEFAULT_CAMPAIGNS_DIR,
        copy_current_output_to_pack,
        load_campaign,
        pack_id_from_number,
        update_memory_from_pack,
        campaign_memory_path,
        campaign_summary_path,
    )


def default_pack_id(campaign: dict[str, object]) -> str:
    packs = campaign.get("packs") or []
    if isinstance(packs, list) and packs:
        last = packs[-1]
        if isinstance(last, dict) and last.get("pack_id"):
            return str(last["pack_id"])
    next_pack_number = int(campaign.get("next_pack_number") or 1)
    return pack_id_from_number(max(1, next_pack_number - 1))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update persistent campaign memory from a completed pack.")
    parser.add_argument("campaign_id")
    parser.add_argument("--pack", dest="pack_id", default="", help="Pack id, for example pack_001. Default: latest pack.")
    parser.add_argument(
        "--from-output",
        action="store_true",
        help="Copy current input/output pipeline files into the pack before reading memory.",
    )
    parser.add_argument("--campaigns-dir", type=Path, default=DEFAULT_CAMPAIGNS_DIR)
    args = parser.parse_args(argv)

    campaign = load_campaign(args.campaign_id, args.campaigns_dir)
    pack_id = args.pack_id or default_pack_id(campaign)
    copied: list[str] = []
    if args.from_output:
        copied = copy_current_output_to_pack(args.campaign_id, pack_id, args.campaigns_dir)

    memory = update_memory_from_pack(args.campaign_id, pack_id, args.campaigns_dir)
    print(f"campaign id: {args.campaign_id}")
    print(f"pack id: {pack_id}")
    if args.from_output:
        print(f"files copied from output: {len(copied)}")
    print(f"used garbage: {len(memory.get('used_garbage', {}))}")
    print(f"used collections: {len(memory.get('used_collections', {}))}")
    print(f"used flowers: {len(memory.get('used_flowers', {}))}")
    print(f"used locations: {len(memory.get('used_locations', {}))}")
    print(f"memory written: {campaign_memory_path(args.campaign_id, args.campaigns_dir)}")
    print(f"summary written: {campaign_summary_path(args.campaign_id, args.campaigns_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
