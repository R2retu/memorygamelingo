from __future__ import annotations
import asyncio
from typing import Callable, Optional

from models.deck import Deck
from models.game_state import GameState
from services.asset_service import AssetService
from services.audio_service import AudioService
from controllers.robokob_controller import RobokobController


class GameController:
    def __init__(
        self,
        state: GameState,
        asset_service: AssetService,
        audio_service: AudioService,
        robokob: RobokobController,
        navigate: Callable[[str], None],
    ):
        self.state = state
        self.assets = asset_service
        self.audio = audio_service
        self.robokob = robokob
        self.navigate = navigate

        self._task: Optional[asyncio.Task] = None

    def start_game(self, difficulty: str):
        self.state.difficulty = str(difficulty)
        self.state.reset_scores()
        self.state.turn = "human"
        self.state.locked = False
        self.state.clear_flips()
        self.robokob.reset()

        items = self.assets.get_items("animals")
        self.state.deck = Deck.build_from_items(items)

        for c in self.state.cards:
            c.is_face_up = False
            c.is_matched = False

        self.state.notify()

    def reset_game(self):
        self.start_game(self.state.difficulty)
        self.navigate("/")

    def on_card_click(self, card_id: int):
        if self.state.locked or not self.state.deck:
            return
        if self.state.turn != "human":
            return

        card = self.state.cards[card_id]
        if card.is_matched or card.is_face_up:
            return

        card.is_face_up = True
        self.state.flipped_ids.append(card_id)
        self.state.notify()

        # Robokob memoriza lo que ve (según dificultad)
        self.robokob.remember(card_id, card.key, self.state)

        if card.audio_src:
            asyncio.create_task(self.audio.play(card.audio_src))

        if len(self.state.flipped_ids) == 2:
            asyncio.create_task(self._compare_two())

    async def _compare_two(self):
        if not self.state.deck:
            return

        self.state.locked = True
        self.state.notify()

        a_id, b_id = self.state.flipped_ids[0], self.state.flipped_ids[1]
        a = self.state.cards[a_id]
        b = self.state.cards[b_id]

        await asyncio.sleep(0.8)

        matched = (a.key == b.key)

        if matched:
            a.is_matched = True
            b.is_matched = True
            if self.state.turn == "human":
                self.state.human_score += 1
            else:
                self.state.robokob_score += 1
        else:
            a.is_face_up = False
            b.is_face_up = False

        self.state.clear_flips()

        # fin del juego
        if self.state.all_matched():
            self.state.locked = False
            self.state.notify()
            self.navigate("/results")
            return

        # Regla clásica:
        # - si haces pareja, repites turno
        # - si fallas, cambias turno
        if matched:
            # mantiene turno
            pass
        else:
            self.state.turn = "robokob" if self.state.turn == "human" else "human"

        self.state.locked = False
        self.state.notify()

        # si ahora es turno robokob, juega
        if self.state.turn == "robokob":
            asyncio.create_task(self._robokob_turn())

    async def _robokob_turn(self):
        """
        Robokob con tiempos del main.py original:
        - 1.0s entre primera y segunda carta
        - 2.0s con ambas visibles
        - 1.2s antes de resolver

        Regla clásica aplicada (FIJA):
        - si Robokob hace pareja, juega otra vez
        - si falla, pasa al humano
        """
        if not self.state.deck:
            return

        self.state.locked = True
        self.state.notify()

        await asyncio.sleep(0.2)

        pair = self.robokob.pick_pair(self.state)
        if pair is None:
            a_id, b_id = self.robokob.pick_random_two(self.state)
        else:
            a_id, b_id = pair

        # 1) primera carta
        self._flip_for_robokob(a_id)
        await asyncio.sleep(1.0)

        # 2) segunda carta
        self._flip_for_robokob(b_id)
        await asyncio.sleep(2.0)

        # preparar comparación
        self.state.flipped_ids = [a_id, b_id]
        self.state.notify()

        await asyncio.sleep(1.2)

        a = self.state.cards[a_id]
        b = self.state.cards[b_id]
        matched = (a.key == b.key)

        if matched:
            a.is_matched = True
            b.is_matched = True
            self.state.robokob_score += 1
        else:
            a.is_face_up = False
            b.is_face_up = False

        self.state.clear_flips()

        # fin del juego
        if self.state.all_matched():
            self.state.locked = False
            self.state.notify()
            self.navigate("/results")
            return

        if matched:
            # ✅ Regla clásica: repite turno
            self.state.turn = "robokob"
            self.state.locked = False
            self.state.notify()

            await asyncio.sleep(0.6)
            await self._robokob_turn()
            return
        else:
            # falla -> turno humano
            self.state.turn = "human"
            self.state.locked = False
            self.state.notify()
            return

    def _flip_for_robokob(self, card_id: int):
        card = self.state.cards[card_id]
        if card.is_matched:
            return
        if card.is_face_up:
            return

        card.is_face_up = True
        self.robokob.remember(card_id, card.key, self.state)
        self.state.notify()

        if card.audio_src:
            asyncio.create_task(self.audio.play(card.audio_src))