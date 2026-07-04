# HD Video Downloader Studio

A Streamlit desktop-style web app for downloading videos (YouTube, and
best-effort public Instagram posts/reels) with metadata preview, quality
selection, progress tracking, and download history — built on top of
[yt-dlp](https://github.com/yt-dlp/yt-dlp).

> ⚠️ **Use responsibly.** Only download content you own, that is public
> domain, or that you have explicit permission to download. Downloading
> copyrighted material without permission may violate a platform's Terms of
> Service and copyright law. Instagram support is best-effort — yt-dlp only
> reliably handles **public** posts/reels and Instagram frequently changes
> its site, which can break extraction without notice.

## Features

- Paste a YouTube or Instagram URL, auto-detect the platform
- Metadata preview: thumbnail, title, uploader, duration, views, likes
- Quality selection (144p–1080p+ depending on source, or audio-only)
- Live download progress (%, speed, ETA)
- SQLite-backed download history with search, delete, and clear-all
- Clean, modular Python architecture (easy to extend)

## Requirements

- Python 3.10+
- [FFmpeg](https://ffmpeg.org/download.html) installed and on your PATH
  (needed to merge separate video/audio streams into one file)

## Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Make sure FFmpeg is installed
ffmpeg -version
```

### Installing FFmpeg

- **Windows:** download a build from https://ffmpeg.org/download.html and
  add the `bin` folder to your PATH.
- **macOS:** `brew install ffmpeg`
- **Linux (Debian/Ubuntu):** `sudo apt install ffmpeg`

## Run

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## Project structure

```text
HD_Video_Downloader/
├── app.py                  # Entry point / page router
├── config.py                # Paths & default settings
├── requirements.txt
├── downloader/
│   ├── downloader.py         # Core yt-dlp download logic
│   ├── youtube.py            # YouTube wrapper
│   ├── instagram.py          # Instagram wrapper (best-effort)
│   ├── quality.py             # Quality list + format-selector logic
│   └── metadata.py            # Metadata extraction
├── ui/
│   ├── sidebar.py, home.py, cards.py, history.py, footer.py
├── database_manager/
│   └── db.py                  # SQLite history CRUD
├── utils/
│   ├── logger.py, validator.py, filename.py, helper.py, internet.py
├── models/
│   └── video.py                # Video / Format dataclasses
├── styles/style.css
├── downloads/                  # Downloaded files land here
├── database/history.db         # Created automatically on first run
└── logs/app.log                # Created automatically on first run
```

## Notes & known limitations

- **Instagram** downloads only work reliably for **public** posts/reels.
  Private accounts, age-restricted content, or Instagram API changes can
  cause failures — this is a yt-dlp/Instagram limitation, not a bug in this
  app.
- Settings page is currently informational (values aren't persisted yet) —
  wire it into `config.py` if you want persistence across runs.
- Streamlit reruns the whole script on each interaction; download progress
  is shown per-run via `st.progress` / `st.empty`, not a background thread,
  so keep the browser tab open during a download.

## Extending

- Add a new platform: create `downloader/<platform>.py`, extend
  `utils/validator.py`'s pattern list, and route to it from
  `downloader/downloader.py` if you need platform-specific yt-dlp options.
- Add authentication/cookies for private content by passing a `cookiefile`
  option into the `ydl_opts` dict in `downloader/downloader.py` and
  `downloader/metadata.py`.
