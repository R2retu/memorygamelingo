import flet as ft


class GameView(ft.View):
    def __init__(self, page: ft.Page, state, controller, on_home, on_reset):
        super().__init__(route="/game", bgcolor=ft.Colors.BLACK)

        self.page_ref = page
        self.state = state
        self.controller = controller
        self.on_home = on_home
        self.on_reset = on_reset

        # UI texts (como original)
        self.mode_text = ft.Text("", size=15, color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD)
        self.score_text = ft.Text("", size=30, color=ft.Colors.YELLOW, weight=ft.FontWeight.BOLD)
        self.turn_text = ft.Text("", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

        # Grid + cards (como original)
        self.grid: ft.GridView | None = None
        self.card_controls: list[ft.Container] = []

        # Botones (similar al original)
        self.back_btn = ft.TextButton(
            "VOLVER AL MENÚ",
            on_click=lambda _: self.on_home(),
            style=ft.ButtonStyle(color=ft.Colors.WHITE),
        )

        # Responsivo (igual al original)
        self.page_ref.on_resized = self._on_page_resized

        # Layout general centrado
        self.controls = [
            ft.SafeArea(
                ft.Column(
                    [
                        self.mode_text,
                        self.score_text,
                        self.turn_text,
                        ft.Row([], alignment=ft.MainAxisAlignment.CENTER),  # aquí insertamos grid
                        self.back_btn,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        ]

        # Suscribimos al estado
        self.state.subscribe(self.refresh)
        self.refresh()

    # ---------- RESPONSIVE LAYOUT (copiado del original) ----------
    def _on_page_resized(self, e):
        self.apply_responsive_layout()

    def apply_responsive_layout(self):
        """
        Ajusta tamaño de cartas y grid según page.width/page.height.
        Mantiene 4 columnas x 5 filas.
        (misma lógica del main.py original)
        """
        if not self.grid or not self.card_controls:
            return

        w = self.page_ref.width or 850
        h = self.page_ref.height or 950

        cols = 4
        rows = 5

        side_padding = 16
        top_area_estimate = 190
        bottom_area_estimate = 70

        spacing = int(max(6, min(14, w * 0.02)))
        available_w = max(200, w - (side_padding * 2))
        available_h = max(200, h - top_area_estimate - bottom_area_estimate)

        card_size = int((available_w - spacing * (cols - 1)) / cols)

        # límites
        card_size = max(55, min(130, card_size))

        grid_h = card_size * rows + spacing * (rows - 1)
        if grid_h > available_h:
            scale = available_h / grid_h
            card_size = int(card_size * scale)
            card_size = max(45, card_size)

        grid_w = card_size * cols + spacing * (cols - 1)
        grid_h = card_size * rows + spacing * (rows - 1)

        self.grid.runs_count = cols
        self.grid.max_extent = card_size
        self.grid.spacing = spacing
        self.grid.run_spacing = spacing
        self.grid.width = grid_w
        self.grid.height = grid_h

        radius = max(10, int(card_size * 0.12))
        for c in self.card_controls:
            c.width = card_size
            c.height = card_size
            c.border_radius = radius
            if isinstance(c.content, ft.Image):
                c.content.fit = ft.BoxFit.CONTAIN

        try:
            self.page_ref.update()
        except Exception:
            pass

    # ---------- UI refresh ----------
    def refresh(self):
        # textos
        self.mode_text.value = f"MODO: {str(self.state.difficulty).upper()}"
        self.score_text.value = f"Humano: {self.state.human_score}    Robokob: {self.state.robokob_score}"
        self.turn_text.value = f"Turno: {'Jugador' if self.state.turn == 'human' else 'Robokob'}"

        # construir grid si aún no existe o cambió el mazo
        if self.state.deck and (self.grid is None or len(self.card_controls) != len(self.state.cards)):
            self._build_grid()

        # actualizar cartas (front/back)
        if self.state.deck and self.card_controls:
            for card in self.state.cards:
                container = self.card_controls[card.id]
                img: ft.Image = container.content  # type: ignore
                img.src = card.image_src if (card.is_face_up or card.is_matched) else "imagesp/card_back.png"

                # borde verde si matched (como original)
                if card.is_matched:
                    container.border = ft.border.all(3, ft.Colors.GREEN)
                else:
                    container.border = ft.border.all(1, ft.Colors.WHITE24)

        # asegurar que la grid esté insertada centrada
        row_holder: ft.Row = self.controls[0].content.controls[3]  # SafeArea -> Column -> Row
        if self.grid and (len(row_holder.controls) == 0 or row_holder.controls[0] is not self.grid):
            row_holder.controls = [self.grid]

        try:
            self.update()
        except Exception:
            pass

        self.apply_responsive_layout()

    def _build_grid(self):
        # Grid como el original
        self.grid = ft.GridView(
            expand=False,
            runs_count=4,
            max_extent=110,
            spacing=10,
            run_spacing=10,
            width=500,
            height=500,
        )

        self.card_controls.clear()
        self.grid.controls.clear()

        # Crear contenedores de cartas como original (110x110, fit contain)
        for card in self.state.cards:
            def make_on_click(card_id: int):
                return lambda e: self.controller.on_card_click(card_id)

            c = ft.Container(
                content=ft.Image(src="imagesp/card_back.png", fit=ft.BoxFit.CONTAIN),
                width=110,
                height=110,
                bgcolor=ft.Colors.GREY_900,
                border_radius=12,
                border=ft.border.all(1, ft.Colors.WHITE24),
                on_click=make_on_click(card.id),
            )
            self.card_controls.append(c)
            self.grid.controls.append(c)