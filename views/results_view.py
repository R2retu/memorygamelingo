import flet as ft


class ResultsView(ft.View):
    def __init__(self, state, on_play_again, on_home):
        super().__init__(route="/results", bgcolor=ft.Colors.BLACK)

        self.state = state
        self._on_play_again = on_play_again
        self._on_home = on_home

        # Determinar ganador
        if self.state.human_score > self.state.robokob_score:
            title = "¡Ganaste!"
            title_color = ft.Colors.GREEN
        elif self.state.human_score < self.state.robokob_score:
            title = "Robokob ganó"
            title_color = ft.Colors.RED
        else:
            title = "Empate"
            title_color = ft.Colors.AMBER

        title_txt = ft.Text(title, size=34, color=title_color, weight=ft.FontWeight.BOLD)
        score_txt = ft.Text(
            f"Humano: {self.state.human_score}    Robokob: {self.state.robokob_score}",
            size=20,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
        )

        play_again_btn = ft.ElevatedButton(
            "Jugar otra vez",
            on_click=lambda _: self._on_play_again(),
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            width=260,
            height=48,
        )

        home_btn = ft.OutlinedButton(
            "Inicio",
            on_click=lambda _: self._on_home(),
            width=260,
            height=44,
        )

        self.controls = [
            ft.SafeArea(
                ft.Column(
                    [
                        ft.Container(height=40),
                        title_txt,
                        ft.Container(height=14),
                        score_txt,
                        ft.Container(height=30),
                        play_again_btn,
                        ft.Container(height=10),
                        home_btn,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                )
            )
        ]