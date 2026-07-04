import re

INVALID_CHARS = r'<>:"/\|?*'


def sanitize_filename(name: str, max_length: int = 150) -> str:
    if not name:
        name = "video"
    cleaned = re.sub(f"[{re.escape(INVALID_CHARS)}]", "_", name)
    cleaned = cleaned.strip().strip(".")
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned or "video"
