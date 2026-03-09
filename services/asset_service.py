from __future__ import annotations
from dataclasses import dataclass
from typing import List


IMAGES = [
    "imagesp/parrot.png", "imagesp/dolphin.png", "imagesp/panda.png",
    "imagesp/turtles.png", "imagesp/hummingbird.png", "imagesp/rabbit.png",
    "imagesp/duck.png", "imagesp/eagle.png", "imagesp/cat.png",
    "imagesp/leopard.png",
]
CARD_BACK = "imagesp/card_back.png"

AUDIO_MAP = {
    "parrot": "audio/parrot.mp3",
    "dolphin": "audio/dolphin.mp3",
    "panda": "audio/panda.mp3",
    "turtles": "audio/turtles.mp3",
    "hummingbird": "audio/hummingbird.mp3",
    "rabbit": "audio/rabbit.mp3",
    "duck": "audio/duck.mp3",
    "eagle": "audio/eagle.mp3",
    "cat": "audio/cat.mp3",
    "leopard": "audio/leopard.mp3",
}


@dataclass(frozen=True)
class AssetItem:
    category: str
    key: str
    label: str
    image_src: str
    audio_src: str


class AssetService:
    def get_categories(self) -> List[str]:
        raise NotImplementedError

    def get_items(self, category: str) -> List[AssetItem]:
        raise NotImplementedError

    def get_card_back(self) -> str:
        raise NotImplementedError


class LocalAssetService(AssetService):
    def __init__(self):
        self._card_back = CARD_BACK
        self._animals = self._build_animals()

    def _build_animals(self) -> List[AssetItem]:
        items: List[AssetItem] = []
        for path in IMAGES:
            key = path.split("/")[-1].replace(".png", "")
            audio = AUDIO_MAP.get(key, "")
            items.append(
                AssetItem(
                    category="animals",
                    key=key,
                    label=key.capitalize(),
                    image_src=path,
                    audio_src=audio,
                )
            )
        return items

    def get_categories(self) -> List[str]:
        return ["animals"]  # listo para agregar "body_parts" luego

    def get_items(self, category: str) -> List[AssetItem]:
        if category == "animals":
            return list(self._animals)
        return []

    def get_card_back(self) -> str:
        return self._card_back