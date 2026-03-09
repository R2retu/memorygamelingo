from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from models.card import Card
from models.deck import Deck


@dataclass
class GameState:
    # routing/game meta
    route: str = "/"
    difficulty: str = "1"  # 1=random, 2=memory partial, 3=memory full

    # gameplay
    deck: Optional[Deck] = None
    locked: bool = False
    turn: str = "human"  # "human" | "robokob"
    human_score: int = 0
    robokob_score: int = 0
    flipped_ids: List[int] = field(default_factory=list)

    # observers (views subscribe)
    _listeners: List[Callable[[], None]] = field(default_factory=list, repr=False)

    def subscribe(self, fn: Callable[[], None]) -> None:
        self._listeners.append(fn)

    def notify(self) -> None:
        for fn in list(self._listeners):
            try:
                fn()
            except Exception:
                pass

    @property
    def cards(self) -> List[Card]:
        return self.deck.cards if self.deck else []

    def reset_scores(self):
        self.human_score = 0
        self.robokob_score = 0

    def clear_flips(self):
        self.flipped_ids.clear()

    def all_matched(self) -> bool:
        return bool(self.deck) and all(c.is_matched for c in self.deck.cards)