from config import DOWNLOAD_DIR
from utils.filename import sanitize_filename
from utils.logger import get_logger
from downloader.quality import quality_to_format_selector

logger = get_logger(__name__)


class DownloadCancelled(Exception):
    pass


def download_video(url: str, quality: str, title: str = "video", progress_callback=None, cancel_flag=None):
    """
    Downloads a video using yt-dlp.

    progress_callback(dict): receives yt-dlp progress-hook dicts.
    cancel_flag(): optional callable returning True to abort the download.
    """
    import yt_dlp

    safe_title = sanitize_filename(title)
    out_template = str(DOWNLOAD_DIR / f"{safe_title}.%(ext)s")

    def hook(d):
        if cancel_flag and cancel_flag():
            raise DownloadCancelled("Download cancelled by user")
        if progress_callback:
            progress_callback(d)

    ydl_opts = {
        "format": quality_to_format_selector(quality),
        "outtmpl": out_template,
        "progress_hooks": [hook],
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logger.info("Downloaded: %s (%s)", title, quality)
        return True, "Download completed"
    except DownloadCancelled:
        logger.info("Download cancelled: %s", url)
        return False, "Cancelled"
    except Exception as e:  # noqa: BLE001
        logger.error("Download failed for %s: %s", url, e)
        return False, str(e)
