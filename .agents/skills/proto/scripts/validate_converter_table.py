"""Use the project validator from both project-local and personal skill installs."""
from pathlib import Path
import os
import sys


def project_root():
    if '--project-root' in sys.argv:
        index = sys.argv.index('--project-root')
        if index + 1 >= len(sys.argv):
            raise SystemExit('--project-root needs a path')
        supplied = Path(sys.argv[index + 1]).resolve()
        del sys.argv[index:index + 2]
        candidates = [supplied]
    else:
        configured = os.environ.get('QUEST_DATA_BUILDER_ROOT')
        candidates = ([Path(configured)] if configured else [])
        candidates += [Path.cwd(), *Path.cwd().parents, *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (candidate / 'src/converter_tables.py').is_file():
            return candidate
    raise SystemExit('Run from quest-data-builder or pass --project-root <project directory>')


sys.path.insert(0, str(project_root()))
from src.converter_tables import validate, main

if __name__ == "__main__":
    raise SystemExit(main())
