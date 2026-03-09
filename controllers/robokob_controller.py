from __future__ import annotations
import random
from typing import Dict, List, Optional, Tuple

from models.game_state import GameState


class RobokobController:
    """
    Dificultad:
      "1" = aleatorio
      "2" = memoria parcial (solo recuerda algunas)
      "3" = memoria total (recuerda todo lo que ha visto)
    """

    def __init__(self):
        # key -> list of card_ids seen (not matched)
        self.memory: Dict[str, List[int]] = {}

    def reset(self):
        self.memory.clear()

    def remember(self, card_id: int, key: str, state: GameState):
        # No memorizar cartas ya encontradas
        card = state.cards[card_id]
        if card.is_matched:
            return

        # Dificultad 1 no memoriza
        if state.difficulty == "1":
            return

        # Dificultad 2 memoriza parcialmente (50% de las veces)
        if state.difficulty == "2":
            if random.random() < 0.5:
                return

        # Dificultad 3 memoriza todo (y dificultad 2 cuando pasa el filtro)
        self.memory.setdefault(key, [])
        if card_id not in self.memory[key]:
            self.memory[key].append(card_id)

        # limpiar ids que ya estén matched
        self.memory[key] = [cid for cid in self.memory[key] if not state.cards[cid].is_matched]

    def pick_pair(self, state: GameState) -> Optional[Tuple[int, int]]:
        """
        Si hay un par seguro en memoria (dos ids con la misma key), retorna (id1, id2).
        """
        if state.difficulty == "1":
            return None

        for key, ids in self.memory.items():
            valid = [cid for cid in ids if not state.cards[cid].is_matched]
            if len(valid) >= 2:
                return valid[0], valid[1]
        return None

    def pick_random_two(self, state: GameState) -> Tuple[int, int]:
        """
        Elige dos cartas al azar que no estén matched y que estén face-down (idealmente).
        """
        candidates = [c.id for c in state.cards if not c.is_matched]
        if len(candidates) < 2:
            return 0, 0
        a = random.choice(candidates)
        candidates.remove(a)
        b = random.choice(candidates)
        return a, b