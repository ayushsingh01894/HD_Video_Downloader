import yt_dlp

from models.video import Video, Format
from utils.logger import get_logger
from utils.validator import detect_platform

logger = get_logger(__name__)


def extract_metadata(url: str) -> Video:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = []
    for f in info.get("formats", []) or []:
        if f.get("vcodec") == "none" and f.get("acodec") == "none":
            continue
        height = f.get("height")
        resolution = f.get("resolution") or (f"{height}p" if height else "audio only")
        formats.append(
            Format(
                format_id=f.get("format_id", ""),
                ext=f.get("ext", ""),
                resolution=resolution,
                filesize=f.get("filesize") or f.get("filesize_approx"),
                vcodec=f.get("vcodec", "none"),
                acodec=f.get("acodec", "none"),
                note=f.get("format_note", ""),
            )
        )

    video = Video(
        url=url,
        title=info.get("title", "Unknown"),
        uploader=info.get("uploader") or info.get("channel") or "Unknown",
        duration=info.get("duration") or 0,
        thumbnail=info.get("thumbnail", ""),
        platform=detect_platform(url),
        upload_date=info.get("upload_date", ""),
        view_count=info.get("view_count"),
        like_count=info.get("like_count"),
        formats=formats,
        raw_info=info,
    )
    return video
