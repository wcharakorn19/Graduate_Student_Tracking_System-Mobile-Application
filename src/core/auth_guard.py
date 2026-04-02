# ==============================================================================
# src/core/auth_guard.py — ระบบตรวจสอบสิทธิ์การเข้าถึง (Authentication Guard)
# ==============================================================================
# ไฟล์นี้มีฟังก์ชัน require_auth() ที่ทุกหน้าจอเรียกใช้ก่อนแสดงผล
# เพื่อตรวจสอบว่าผู้ใช้ได้ Login แล้วหรือยัง
#
# การทำงาน:
#   - ถ้า Login แล้ว   → คืนค่า user_id เพื่อให้หน้าจอนำไปใช้ต่อ
#   - ถ้ายังไม่ Login  → Redirect กลับไปหน้า Login ทันที + คืนค่า None
#
# ใช้ Pattern "Guard" เพื่อป้องกันไม่ให้ผู้ใช้เข้าถึงหน้าจอที่ต้อง Login ก่อน
# ==============================================================================
import flet as ft


def require_auth(page: ft.Page):
    """ตรวจ session — คืนค่า user_id ถ้า login แล้ว, คืน None + redirect ถ้ายัง"""
    # ดึง user_id จาก Session ที่เก็บไว้ตอน Login สำเร็จ
    user_id = page.session.get("user_id")
    if not user_id:
        # ถ้าไม่พบ user_id แสดงว่ายังไม่ได้ Login → บังคับ Redirect ไปหน้า Login
        page.go("/login")
        return None
    # ถ้ามี user_id → คืนค่ากลับไปให้หน้าจอใช้งาน
    return user_id
