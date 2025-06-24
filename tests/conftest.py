import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# legacy entry: app.main:app (repo root); backend entry: src.main:backend_app (backend/)
for p in (ROOT, ROOT / "backend"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Keep the SQLite file out of the repo and point the backend at the repo's products.json.
os.environ.setdefault("DATA_DIR", str(ROOT / "data"))
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{Path(tempfile.mkdtemp(prefix='commerce-tests-'), 'app.db').as_posix()}"
