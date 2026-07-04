import re

YOUTUBE_PATTERNS = [
    r"(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+",
    r"(https?://)?(www\.)?youtube\.com/shorts/[\w-]+",
    r"(https?://)?youtu\.be/[\w-]+",
]

INSTAGRAM_PATTERNS = [
    r"(https?://)?(www\.)?instagram\.com/(reel|p|tv)/[\w-]+",
]


def detect_platform(url: str) -> str:
    if not url or not isinstance(url, str):
        return "Invalid URL"
    url = url.strip()
    for pattern in YOUTUBE_PATTERNS:
        if re.search(pattern, url):
            return "YouTube"
    for pattern in INSTAGRAM_PATTERNS:
        if re.search(pattern, url):
            return "Instagram"
    return "Invalid URL"


def is_valid_url(url: str) -> bool:
    return detect_platform(url) != "Invalid URL"
