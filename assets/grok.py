import flet as ft

AUDIO_MAP = {
    "cat": "assets/audio/cat.wav"
}

def main(page: ft.Page):
    page.title = "Sonido Cat con WebView"

    def play_cat_sound(e):
        # HTML incrustado dentro de un WebView
        html = f"""
        <html>
        <body>
            <audio autoplay>
                <source src="{AUDIO_MAP['cat']}" type="audio/wav">
            </audio>
        </body>
        </html>
        """

        # WebView con contenido inline (data URL)
        webview = ft.WebView(
            src="data:text/html," + html.replace("\n", "").replace(" ", "%20"),
            width=0,
            height=0
        )

        page.overlay.append(webview)
        page.update()

    page.add(
        ft.Button("Sonar gato", on_click=play_cat_sound)
    )

if __name__ == "__main__":
    ft.run(main)
