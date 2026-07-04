from models.video import Video

STANDARD_HEIGHTS = [144, 240, 360, 480, 720, 1080, 1440, 2160]


def get_available_qualities(video: Video):
    heights = set()
    for f in video.formats:
        if f.resolution and "p" in f.resolution and "x" not in f.resolution.split("p")[0]:
            try:
                h = int(f.resolution.split("p")[0])
                heights.add(h)
            except ValueError:
                continue
        elif f.resolution and "x" in f.resolution:
            try:
                h = int(f.resolution.lower().split("x")[-1])
                heights.add(h)
            except ValueError:
                continue

    qualities = sorted({h for h in heights}, reverse=False)
    qualities = [f"{h}p" for h in qualities]
    qualities.append("Audio only")

    if len(qualities) <= 1:
        qualities = ["best", "Audio only"]

    return qualities


def quality_to_format_selector(quality: str) -> str:
    if quality == "Audio only":
        return "bestaudio/best"
    if quality.endswith("p"):
        height = quality.replace("p", "")
        return f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
    return "best"
