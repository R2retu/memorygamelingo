import flet as ft
from shared.theme import Theme

def create_menu_button(text: str, on_click) -> ft.Button:
    btn_style = ft.ButtonStyle(
        color={
            ft.ControlState.DEFAULT: ft.Colors.BLACK,
            ft.ControlState.HOVERED: ft.Colors.BLACK,
        },
        bgcolor={
            ft.ControlState.DEFAULT: ft.Colors.YELLOW,
            ft.ControlState.HOVERED: ft.Colors.WHITE,
        },
        shape={ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=10)},
        animation_duration=300,
    )
    return ft.Button(text, width=300, height=50, style=btn_style, on_click=on_click)

def create_circle_button(text: str, on_click) -> ft.Container:
    return ft.Container(
        width=90,
        height=90,
        bgcolor=ft.Colors.YELLOW,
        border_radius=45,
        alignment=ft.Alignment(0, 0),
        ink=True,
        on_click=on_click,
        content=ft.Text(text, size=16, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
    )
