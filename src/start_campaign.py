from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .campaigns import DEFAULT_CAMPAIGNS_DIR, create_campaign, campaign_dir
except ImportError:
    from campaigns import DEFAULT_CAMPAIGNS_DIR, create_campaign, campaign_dir


def split_characters(values: list[str]) -> list[str]:
    characters: list[str] = []
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                characters.append(item)
    return characters


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create or open a persistent quest campaign.")
    parser.add_argument("campaign_id", help="Stable campaign id, for example MeatballRain_2026.")
    parser.add_argument("--title", default="", help="Human-readable campaign title.")
    parser.add_argument("--tone", default="", help="Campaign tone, for example humor.")
    parser.add_argument(
        "--characters",
        nargs="*",
        default=[],
        help="Characters as separate values or comma-separated list.",
    )
    parser.add_argument("--campaigns-dir", type=Path, default=DEFAULT_CAMPAIGNS_DIR)
    parser.add_argument("--overwrite", action="store_true", help="Overwrite campaign metadata if it already exists.")
    args = parser.parse_args(argv)

    campaign = create_campaign(
        args.campaign_id,
        title=args.title or None,
        tone=args.tone or None,
        characters=split_characters(args.characters),
        campaigns_dir=args.campaigns_dir,
        overwrite=args.overwrite,
    )
    print(f"campaign id: {campaign['campaign_id']}")
    print(f"title: {campaign.get('title') or ''}")
    print(f"next pack number: {campaign.get('next_pack_number')}")
    print(f"campaign dir: {campaign_dir(args.campaign_id, args.campaigns_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
