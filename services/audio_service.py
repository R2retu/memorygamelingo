import flet as ft
import flet_audio as fta


class AudioService:
    def __init__(self, page: ft.Page):
        self.page = page
        # Igual que el original: mantener referencias vivas
        self.active_audios: list[fta.Audio] = []

    async def play(self, src: str):
        if not src:
            return
        try:
            audio = fta.Audio(
                src=src,
                autoplay=True,
                volume=1,
                balance=0,
                on_state_change=self._on_audio_state_changed,
            )

            # Mantener vivo (igual al original)
            self.active_audios.append(audio)
            if len(self.active_audios) > 5:
                self.active_audios.pop(0)

        except Exception as e:
            print(f"Error creando audio: {e}")

    def _on_audio_state_changed(self, e):
        # callback vacío como el original (evita errores)
        try:
            pass
        except Exception as ex:
            print(f"Error en callback de audio: {ex}")