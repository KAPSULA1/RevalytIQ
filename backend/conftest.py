from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

for path in (PROJECT_ROOT, BASE_DIR):
    str_path = str(path)
    if str_path not in sys.path:
        sys.path.insert(0, str_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.revalyt.settings.base")
sqlite_db_path = BASE_DIR / "test.sqlite3"
os.environ.setdefault("DATABASE_URL", f"sqlite:///{sqlite_db_path}")


def pytest_configure(config):  # noqa: D401
    """Prepare a predictable environment before Django initialises."""

    env_file = BASE_DIR / ".env"
    example_file = BASE_DIR / ".env.example"
    if not env_file.exists() and example_file.exists():
        shutil.copy(example_file, env_file)
