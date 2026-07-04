from downloader.downloader import download_video


def download_instagram(url, quality, title, progress_callback=None, cancel_flag=None):
    """
    Thin wrapper for Instagram downloads.

    Note: Instagram actively changes its site and only public posts/reels are
    reliably supported by yt-dlp. Private or restricted content will fail.
    """
    return download_video(url, quality, title, progress_callback, cancel_flag)
