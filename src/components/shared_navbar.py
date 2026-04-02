# ==============================================================================
# src/components/shared_navbar.py — Component แถบนำทางด้านล่าง (Bottom Navigation Bar)
# ==============================================================================
# ไฟล์นี้สร้าง SharedNavBar ที่ใช้ร่วมกันทุกหน้าจอ (ยกเว้น Login/Welcome)
# แสดงไอคอน 3 ตัว: [โปรไฟล์/กิจกรรม] [หน้าหลัก] [ติดต่อเจ้าหน้าที่]
#
# การทำงาน:
# - ดึง Role จาก Session เพื่อกำหนดเส้นทางที่ถูกต้อง
# - ไอคอนที่ active (หน้าปัจจุบัน) จะแสดงเป็นแบบ filled (ทึบ)
# - ไอคอนที่ไม่ active จะแสดงเป็นแบบ outlined (โครงร่าง)
# ==============================================================================
import logging
import flet as ft
from core.config import APP_COLORS

logger = logging.getLogger(__name__)


def SharedNavBar(page: ft.Page, current_route: str):
    """
    สร้าง Bottom Navigation Bar ที่ปรับเปลี่ยนตาม Role ของผู้ใช้

    Parameters:
        page (ft.Page)       — หน้าแอป (ใช้สำหรับดึง Session + นำทาง)
        current_route (str)  — Route ของหน้าปัจจุบัน (ใช้เพื่อ highlight ไอคอน active)
    """
    # ─── ส่วนที่ 1: ดึง Role เพื่อกำหนดเส้นทาง ───
    user_role = page.session.get("user_role")

    if user_role == "advisor":
        # อาจารย์: ไอคอนซ้าย = กิจกรรม, บ้าน = advisor_home
        home_route = "/advisor_home"
        left_route = "/advisor_activities"
    else:
        # นักศึกษา: ไอคอนซ้าย = โปรไฟล์, บ้าน = student_home
        home_route = "/student_home"
        left_route = "/profile"

    # ตรวจสอบว่าหน้าปัจจุบันตรงกับไอคอนไหน (เพื่อ highlight)
    is_home = current_route == home_route
    is_left_active = current_route == left_route

    # ─── ส่วนที่ 2: กำหนดไอคอนซ้ายตาม Role ───
    if user_role == "advisor":
        # Advisor: ใช้ไอคอน people เนื่องจากแสดงรายการนักศึกษาในความดูแล
        left_icon = ft.Icons.PEOPLE if is_left_active else ft.Icons.PEOPLE_OUTLINE
    else:
        # Student: ใช้ไอคอน person (คน)
        left_icon = ft.Icons.PERSON if is_left_active else ft.Icons.PERSON_OUTLINE

    # ─── ส่วนที่ 3: ไอคอนติดต่อเจ้าหน้าที่ (Chat) ───
    chat_route = "/contact_staff"
    is_chat_active = current_route == chat_route

    # ─── ส่วนที่ 4: สร้าง BottomAppBar พร้อมไอคอน 3 ตัว ───
    return ft.BottomAppBar(
        bgcolor=APP_COLORS["background"],       # สีพื้นหลังชมพูอ่อน
        content=ft.Row(
            controls=[
                # ไอคอนซ้าย: โปรไฟล์ (Student) / กิจกรรม (Advisor)
                ft.IconButton(
                    icon=left_icon,
                    icon_color=APP_COLORS["primary"],
                    icon_size=30,
                    on_click=lambda _: page.go(left_route),
                ),
                # ไอคอนกลาง: หน้าหลัก (Home)
                ft.IconButton(
                    icon=ft.Icons.HOME if is_home else ft.Icons.HOME_OUTLINED,
                    icon_color=APP_COLORS["primary"],
                    icon_size=30,
                    on_click=lambda _: page.go(home_route),
                ),
                # ไอคอนขวา: ติดต่อเจ้าหน้าที่ (Chat)
                ft.IconButton(
                    icon=ft.Icons.CHAT_BUBBLE if is_chat_active else ft.Icons.CHAT_BUBBLE_OUTLINE,
                    icon_color=APP_COLORS["primary"],
                    icon_size=30,
                    on_click=lambda _: page.go(chat_route),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,    # จัดไอคอนให้กระจายเท่าๆ กัน
        ),
    )
