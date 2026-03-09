import flet as ft

from models.game_state import GameState
from services.asset_service import LocalAssetService
from services.audio_service import AudioService

from controllers.robokob_controller import RobokobController
from controllers.game_controller import GameController

from views.home_view import HomeView
from views.game_view import GameView
from views.results_view import ResultsView


def main(page: ft.Page):
    page.title = "El Rincón de Olga Lucia"
    page.bgcolor = ft.Colors.BLACK
    page.window_width = 850
    page.window_height = 950

    asset_service = LocalAssetService()
    audio_service = AudioService(page)

    state = GameState()
    robokob = RobokobController()
    controller = GameController(
        state=state,
        asset_service=asset_service,
        audio_service=audio_service,
        robokob=robokob,
        navigate=lambda path: page.go(path),
    )

    def render_route(route: str):
        r = route or "/"
        page.views.clear()

        if r == "/":
            page.views.append(
                HomeView(
                    on_start=lambda difficulty: (controller.start_game(difficulty), page.go("/game")),
                    on_exit=lambda: None,  # el botón Salir maneja el cierre en HomeView
                )
            )

        elif r == "/game":
            page.views.append(
                GameView(
                    page=page,  # ✅ necesario para el layout responsivo del tablero (como original)
                    state=state,
                    controller=controller,
                    on_home=lambda: page.go("/"),
                    on_reset=lambda: controller.reset_game(),
                )
            )

        elif r == "/results":
            page.views.append(
                ResultsView(
                    state=state,
                    on_play_again=lambda: (controller.start_game(state.difficulty), page.go("/game")),
                    on_home=lambda: page.go("/"),
                )
            )

        else:
            page.views.append(
                ft.View(
                    route=r,
                    controls=[ft.Text("Ruta no encontrada", color=ft.Colors.WHITE)],
                    bgcolor=ft.Colors.BLACK,
                )
            )

        page.update()

    def route_change(e: ft.RouteChangeEvent):
        render_route(e.route)

    def view_pop(e: ft.ViewPopEvent):
        if page.views:
            page.views.pop()
        if page.views:
            top = page.views[-1]
            page.go(top.route)
        else:
            page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Fuerza render inicial
    if not page.route:
        page.route = "/"
    render_route(page.route)