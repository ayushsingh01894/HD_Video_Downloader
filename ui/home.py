import streamlit as st

from config import DOWNLOAD_DIR
from database_manager.db import add_entry
from downloader.downloader import download_video
from downloader.metadata import extract_metadata
from downloader.quality import get_available_qualities
from ui.cards import render_format_table, render_video_card
from utils.internet import is_connected
from utils.logger import get_logger
from utils.validator import is_valid_url

logger = get_logger(__name__)


def render_home():
    st.title("📥 HD Video Downloader Studio")
    st.caption("Paste a YouTube or Instagram URL to get started.")

    url = st.text_input("Video URL", placeholder="https://www.youtube.com/watch?v=...")
    analyze = st.button("🔍 Analyze", type="primary")

    if analyze:
        if not url:
            st.warning("Please paste a URL first.")
        elif not is_connected():
            st.error("No internet connection detected.")
        elif not is_valid_url(url):
            st.error("Unsupported or invalid URL. Only YouTube and Instagram are supported.")
        else:
            with st.spinner("Fetching metadata..."):
                try:
                    video = extract_metadata(url)
                    st.session_state["video"] = video
                except Exception as e:  # noqa: BLE001
                    logger.error("Metadata extraction failed: %s", e)
                    st.error(f"Failed to fetch metadata: {e}")
                    st.session_state.pop("video", None)

    video = st.session_state.get("video")
    if video:
        st.markdown("---")
        render_video_card(video)

        with st.expander("Available formats"):
            render_format_table(video)

        qualities = get_available_qualities(video)
        quality = st.selectbox("Select quality", qualities)

        download_clicked = st.button("⬇️ Download", type="primary")

        if download_clicked:
            progress_bar = st.progress(0)
            status_text = st.empty()

            def progress_callback(d):
                if d.get("status") == "downloading":
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
                    downloaded = d.get("downloaded_bytes", 0)
                    pct = min(downloaded / total, 1.0)
                    progress_bar.progress(pct)
                    speed = d.get("speed")
                    eta = d.get("eta")
                    speed_str = f"{speed / 1024 / 1024:.2f} MB/s" if speed else "N/A"
                    status_text.text(
                        f"Downloading... {pct * 100:.1f}% | Speed: {speed_str} | ETA: {eta or 'N/A'}s"
                    )
                elif d.get("status") == "finished":
                    status_text.text("Finalizing (merging/converting)...")

            success, message = download_video(
                url=video.url,
                quality=quality,
                title=video.title,
                progress_callback=progress_callback,
            )

            if success:
                progress_bar.progress(1.0)
                status_text.success("✅ Download complete! Saved to: " + str(DOWNLOAD_DIR))
                add_entry(
                    url=video.url,
                    title=video.title,
                    platform=video.platform,
                    quality=quality,
                    location=str(DOWNLOAD_DIR),
                    status="Completed",
                )
            else:
                status_text.error(f"❌ Download failed: {message}")
                add_entry(
                    url=video.url,
                    title=video.title,
                    platform=video.platform,
                    quality=quality,
                    location=str(DOWNLOAD_DIR),
                    status=f"Failed: {message}",
                )
