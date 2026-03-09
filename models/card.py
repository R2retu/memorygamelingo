from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Card:
    id: int
    key: str
    image_src: str
    audio_src: str
    is_face_up: bool = False
    is_matched: bool = False