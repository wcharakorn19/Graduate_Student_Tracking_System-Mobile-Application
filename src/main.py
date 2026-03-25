# src/main.py
import logging
import flet as ft
from core.config import APP_TITLE
from core.app_router import AppRouter

# ตั้งค่า Logging สำหรับทั้ง Application
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

# Setup App
def main(page: ft.Page):
    page.title = APP_TITLE
    page.window.width = 402
    page.window.height = 874

    # Setup Navigation and Routing with AppRouter
    AppRouter(page)

    page.go("/")


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
