from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Format:
    format_id: str
    ext: str
    resolution: str
    filesize: Optional[int]
    vcodec: str
    acodec: str
    note: str = ""


@dataclass
class Video:
    url: str
    title: str = "Unknown"
    uploader: str = "Unknown"
    duration: int = 0
    thumbnail: str = ""
    platform: str = "Unknown"
    upload_date: str = ""
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    formats: List[Format] = field(default_factory=list)
    raw_info: dict = field(default_factory=dict)
