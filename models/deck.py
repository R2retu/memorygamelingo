from __future__ import annotations
import random
from dataclasses import dataclass
from typing import List

from models.card import Card
from services.asset_service import AssetItem


@dataclass
class Deck:
    cards: List[Card]

    @staticmethod
    def build_from_items(items: List[AssetItem]) -> "Deck":
        """
        Construye un mazo de 20 cartas a partir de 10 items (pares).
        """
        cards: List[Card] = []
        cid = 0
        for it in items:
            cards.append(Card(id=cid, key=it.key, image_src=it.image_src, audio_src=it.audio_src)); cid += 1
            cards.append(Card(id=cid, key=it.key, image_src=it.image_src, audio_src=it.audio_src)); cid += 1

        random.shuffle(cards)

        # re-asignar ids secuenciales (útil para indexar y click)
        for i, c in enumerate(cards):
            c.id = i

        return Deck(cards=cards)