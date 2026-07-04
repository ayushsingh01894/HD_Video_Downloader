from downloader.downloader import download_video


def download_youtube(url, quality, title, progress_callback=None, cancel_flag=None):
    """Thin wrapper kept for module clarity / future YouTube-specific tweaks."""
    return download_video(url, quality, title, progress_callback, cancel_flag)
