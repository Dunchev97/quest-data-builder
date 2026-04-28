from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .campaigns import DEFAULT_CAMPAIGNS_DIR, create_pack, pack_dir
except ImportError:
    from campaigns import DEFAULT_CAMPAIGNS_DIR, create_pack, pack_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create the next pack folder inside a persistent campaign.")
    parser.add_argument("campaign_id")
    parser.add_argument("--title", default="", help="Optional pack title.")
    parser.add_argument("--notes", default="", help="Optional pack notes.")
    parser.add_argument("--pack-number", type=int, default=None, help="Explicit pack number. By default uses next_pack_number.")
    parser.add_argument("--campaigns-dir", type=Path, default=DEFAULT_CAMPAIGNS_DIR)
    args = parser.parse_args(argv)

    pack = create_pack(
        args.campaign_id,
        title=args.title or None,
        notes=args.notes or None,
        pack_number=args.pack_number,
        campaigns_dir=args.campaigns_dir,
    )
    print(f"campaign id: {args.campaign_id}")
    print(f"pack id: {pack['pack_id']}")
    print(f"pack dir: {pack_dir(args.campaign_id, pack['pack_id'], args.campaigns_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
