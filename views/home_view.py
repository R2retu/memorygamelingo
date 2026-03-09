import flet as ft

TOPIC_IMAGES = [
    ("parrot", "imagesp/parrot.png"),
    ("dolphin", "imagesp/dolphin.png"),
    ("panda", "imagesp/panda.png"),
    ("turtles", "imagesp/turtles.png"),
    ("hummingbird", "imagesp/hummingbird.png"),
    ("rabbit", "imagesp/rabbit.png"),
    ("duck", "imagesp/duck.png"),
    ("eagle", "imagesp/eagle.png"),
    ("cat", "imagesp/cat.png"),
    ("leopard", "imagesp/leopard.png"),
]


class HomeView(ft.View):
    def __init__(self, on_start, on_exit):
        super().__init__(route="/", bgcolor=ft.Colors.BLACK)

        self._on_start = on_start
        self._on_exit = on_exit

        self.difficulty = "1"

        # paginación de temas (4 por página)
        self.page_start = 0
        self.page_size = 4

        self.selected_index = 0
        self.selected_topic_key = TOPIC_IMAGES[self.selected_index][0]

        # --------- helpers ----------
        def start_click(_):
            self._on_start(self.difficulty)

        def _set_dialog_open(v: bool):
            try:
                if self.page.dialog:
                    self.page.dialog.open = v
                    self.page.update()
            except Exception:
                pass

        def help_click(_):
            self.page.dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Ayuda", weight=ft.FontWeight.BOLD),
                content=ft.Text(
                    "• Elige dificultad\n"
                    "• Usa ◀ ▶ para ver temas (4 por página)\n"
                    "• Selecciona un tema\n"
                    "• Encuentra las parejas\n"
                    "• Si fallas, juega el Robot AI"
                ),
                actions=[ft.TextButton("Cerrar", on_click=lambda __: _set_dialog_open(False))],
            )
            self.page.dialog.open = True
            self.page.update()

        # --------- difficulty circles (pequeños) ----------
        def set_difficulty(v: str):
            self.difficulty = v

            easy_box.bgcolor = ft.Colors.GREEN if v == "1" else ft.Colors.GREY_800
            mid_box.bgcolor = ft.Colors.AMBER if v == "2" else ft.Colors.GREY_800
            hard_box.bgcolor = ft.Colors.RED if v == "3" else ft.Colors.GREY_800

            easy_txt.color = ft.Colors.BLACK if v == "1" else ft.Colors.WHITE
            mid_txt.color = ft.Colors.BLACK if v == "2" else ft.Colors.WHITE
            hard_txt.color = ft.Colors.BLACK if v == "3" else ft.Colors.WHITE

            try:
                self.update()
            except Exception:
                pass

        def diff_circle(label: str, value: str, active_color: str):
            txt = ft.Text(label, color=ft.Colors.WHITE, size=10, weight=ft.FontWeight.BOLD)
            box = ft.Container(
                width=54,
                height=54,
                alignment=ft.Alignment(0, 0),
                border_radius=999,
                bgcolor=active_color if self.difficulty == value else ft.Colors.GREY_800,
                border=ft.border.all(2, ft.Colors.WHITE24),
                content=txt,
                on_click=lambda _: set_difficulty(value),
            )
            return box, txt

        easy_box, easy_txt = diff_circle("Fácil", "1", ft.Colors.GREEN)
        mid_box, mid_txt = diff_circle("Medio", "2", ft.Colors.AMBER)
        hard_box, hard_txt = diff_circle("Difícil", "3", ft.Colors.RED)

        # --------- topics (4 por página) ----------
        selected_text = ft.Text(
            f"Tema seleccionado: {self.selected_topic_key.capitalize()}",
            color=ft.Colors.WHITE70,
            size=12,
        )

        topics_row = ft.Row(spacing=10, alignment=ft.MainAxisAlignment.CENTER)

        def make_topic_tile(idx: int, key: str, img_src: str):
            label = ft.Text(key.capitalize(), color=ft.Colors.WHITE70, size=11)
            img = ft.Image(src=img_src, width=56, height=56, fit="contain")
            selected = (idx == self.selected_index)

            return ft.Container(
                width=88,
                padding=8,
                border_radius=14,
                bgcolor=ft.Colors.GREY_900,
                border=ft.border.all(2, ft.Colors.GREEN if selected else ft.Colors.WHITE24),
                content=ft.Column([img, label], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
                on_click=lambda _: select_topic(idx),
            )

        def rebuild_topics_page():
            topics_row.controls.clear()
            end = min(len(TOPIC_IMAGES), self.page_start + self.page_size)
            for i in range(self.page_start, end):
                k, src = TOPIC_IMAGES[i]
                topics_row.controls.append(make_topic_tile(i, k, src))

            while len(topics_row.controls) < self.page_size:
                topics_row.controls.append(ft.Container(width=88, height=88))

        def select_topic(i: int):
            self.selected_index = i
            self.selected_topic_key = TOPIC_IMAGES[i][0]
            selected_text.value = f"Tema seleccionado: {self.selected_topic_key.capitalize()}"
            rebuild_topics_page()
            try:
                self.update()
            except Exception:
                pass

        def prev_page(_):
            self.page_start = max(0, self.page_start - self.page_size)
            if not (self.page_start <= self.selected_index < self.page_start + self.page_size):
                select_topic(self.page_start)
            else:
                rebuild_topics_page()
                self.update()

        def next_page(_):
            max_start = max(0, len(TOPIC_IMAGES) - self.page_size)
            self.page_start = min(max_start, self.page_start + self.page_size)
            if not (self.page_start <= self.selected_index < self.page_start + self.page_size):
                select_topic(self.page_start)
            else:
                rebuild_topics_page()
                self.update()

        arrow_left = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            icon_color=ft.Colors.WHITE,
            tooltip="Anterior",
            on_click=prev_page,
        )
        arrow_right = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            icon_color=ft.Colors.WHITE,
            tooltip="Siguiente",
            on_click=next_page,
        )

        rebuild_topics_page()

        carousel = ft.Row(
            [arrow_left, ft.Container(width=400, content=topics_row), arrow_right],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        )

        # --------- UI ----------
        title = ft.Text(
            "Juego de Memoria & Curso de Ingles",
            size=24,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        subtitle = ft.Text(
            "Humano vs AI Robot",
            size=16,
            color=ft.Colors.WHITE70,
            text_align=ft.TextAlign.CENTER,
        )

        diff_title = ft.Text("Dificultad", size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
        topics_title = ft.Text("TEMA", size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)

        start_btn = ft.ElevatedButton(
            "Empezar",
            on_click=start_click,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            width=220,
            height=42,
        )

        exit_btn = ft.OutlinedButton(
            "Salir",
            on_click=lambda _: self._on_exit(),
            width=220,
            height=38,
        )

        # Help + copyright centrados
        footer = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.HELP_OUTLINE,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Ayuda",
                    on_click=help_click,
                ),
                ft.Text("El Rincon de Olga Lucia © 2026", color=ft.Colors.WHITE70, size=12),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        self.controls = [
            ft.SafeArea(
                ft.Column(
                    [
                        ft.Container(height=8),
                        title,
                        ft.Container(height=4),
                        subtitle,

                        ft.Container(height=14),
                        diff_title,
                        ft.Container(height=8),
                        ft.Row([easy_box, mid_box, hard_box],
                               alignment=ft.MainAxisAlignment.CENTER, spacing=10, wrap=True),

                        ft.Container(height=14),
                        topics_title,
                        selected_text,
                        ft.Container(height=6),
                        carousel,

                        ft.Container(height=14),
                        start_btn,

                        ft.Container(expand=True),

                        exit_btn,
                        ft.Container(height=18),
                        footer,
                        ft.Container(height=10),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.START,
                    expand=True,
                )
            )
        ]

        set_difficulty("1")