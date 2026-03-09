import os
import traceback
import flet as ft
from app import main as app_main


def safe_main(page: ft.Page):
    try:
        print("✅ safe_main: app_main() starting...")
        app_main(page)
        print("✅ safe_main: app_main() finished setup.")
    except Exception:
        print("❌ EXCEPCIÓN dentro de app_main(page):")
        traceback.print_exc()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print(f"🚀 Starting Flet on port {port}...")
    ft.run(
        safe_main,
        assets_dir="assets",
        host="0.0.0.0",
        port=port,
    )
