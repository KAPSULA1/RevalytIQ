from __future__ import annotations

import os
from pathlib import Path

if "DATABASE_URL" not in os.environ:
    sqlite_path = Path(__file__).resolve().parent / "test.sqlite3"
    os.environ["DATABASE_URL"] = f"sqlite:///{sqlite_path}"
