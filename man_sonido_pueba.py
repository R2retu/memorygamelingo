import asyncio
import flet as ft
import flet_audio as fta  # pip install flet-audio

ANIMALS = [
    "parrot",
    "dolphin",
    "panda",
    "turtles",
    "hummingbird",
    "rabbit",
    "duck",
    "eagle",
    "cat",
    "leopard",
]

GAP_SECONDS = 3.0


def main(page: ft.Page):
    page.title = "Test audio secuencial (estilo original)"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    status = ft.Text("Listo.", size=22, color=ft.Colors.YELLOW, weight=ft.FontWeight.BOLD)

    # Mantener referencias vivas (igual que tu juego)
    active_audios: list[fta.Audio] = []

    async def play_sequence():
        start_btn.disabled = True
        status.value = "Iniciando secuencia..."
        page.update()

        for animal in ANIMALS:
            src = f"audio/{animal}.mp3"  # assets/audio/<animal>.mp3

            status.value = f"🔊 Sonando: {animal}"
            page.update()

            try:
                a = fta.Audio(
                    src=src,
                    autoplay=True,  # igual que tu original
                    volume=1,
                    balance=0,
                    release_mode=fta.ReleaseMode.STOP,
                    on_state_change=lambda e: None,
                )
                active_audios.append(a)

                # limitar cantidad de instancias vivas para no acumular demasiado
                if len(active_audios) > 8:
                    active_audios.pop(0)

            except Exception as ex:
                status.value = f"❌ Error creando audio {animal}: {ex}"
                page.update()
                break

            await asyncio.sleep(GAP_SECONDS)

        status.value = "✅ Terminé."
        start_btn.disabled = False
        page.update()

    def on_start_click(e):
        # run_task requiere coroutine function (sin args)
        page.run_task(play_sequence)

    start_btn = ft.Button(
        "EMPEZAR",
        on_click=on_start_click,
        style=ft.ButtonStyle(bgcolor=ft.Colors.YELLOW, color=ft.Colors.BLACK),
        width=220,
        height=55,
    )

    page.add(
        ft.Column(
            [
                ft.Text("TEST AUDIO (assets/audio)", size=28, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                start_btn,
                ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                status,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.run(
        main,
        assets_dir="assets",
        host="0.0.0.0",
        port=8080,
    )