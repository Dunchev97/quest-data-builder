"""Use the project validator so the skill and Stage 6 share one contract."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from src.converter_tables import validate, main

if __name__ == "__main__":
    raise SystemExit(main())
