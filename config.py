from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DOWNLOAD_DIR = BASE_DIR / "downloads"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "history.db"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"
STYLE_PATH = BASE_DIR / "styles" / "style.css"
ASSETS_DIR = BASE_DIR / "assets"

for _d in (DOWNLOAD_DIR, DATABASE_DIR, LOG_DIR):
    _d.mkdir(parents=True, exist_ok=True)

APP_NAME = "HD Video Downloader Studio"
DEFAULT_QUALITY = "best"
DEFAULT_THEME = "dark"
HISTORY_LIMIT = 200
DOWNLOAD_THREADS = 1
