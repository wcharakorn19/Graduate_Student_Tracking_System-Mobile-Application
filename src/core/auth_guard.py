# src/core/auth_guard.py
import flet as ft


def require_auth(page: ft.Page):
    """ตรวจ session — คืนค่า user_id ถ้า login แล้ว, คืน None + redirect ถ้ายัง"""
    user_id = page.session.get("user_id")
    if not user_id:
        page.go("/login")
        return None
    return user_id
