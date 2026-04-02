# ==============================================================================
# src/components/form_helpers.py — ฟังก์ชันช่วยสร้าง UI สำหรับหน้า Form Detail
# ==============================================================================
# ไฟล์นี้รวม Reusable Functions ที่ใช้ร่วมกันในหน้า Form Detail ทั้ง 7 หน้า
# ช่วยลดโค้ดซ้ำอย่างมาก เพราะทุกฟอร์มมีโครงสร้าง UI คล้ายกัน
#
# ประกอบด้วย 4 ฟังก์ชัน:
#   1. form_text_value()   → สร้าง Text widget สำหรับแสดงค่าในฟอร์ม
#   2. create_form_row()   → สร้างแถว label-value (เช่น "ชื่อ: นายสมชาย")
#   3. FormDetailCard()    → สร้างการ์ดมาตรฐาน (กล่องขาวมีเงา)
#   4. FormDetailAppBar()  → สร้าง AppBar พร้อมปุ่มย้อนกลับ
# ==============================================================================
import flet as ft
from core.config import APP_COLORS


def form_text_value(initial: str = "-") -> ft.Text:
    """
    สร้าง Text widget สำหรับแสดงค่าในฟอร์ม
    ค่า default เป็น "-" เผื่อยังไม่มีข้อมูล

    ถูกสร้างแยกเป็นตัวแปร เพื่อให้สามารถเปลี่ยนค่า (.value = "xxx")
    ได้ภายหลังเมื่อ API ส่งข้อมูลกลับมา
    """
    return ft.Text(initial, size=14, color=APP_COLORS["text_dark"])


def create_form_row(label: str, value_control: ft.Control, label_width: int = 140):
    """
    สร้างแถวข้อมูลแบบ label-value สำหรับ Form Detail Screen
    ตัวอย่าง: "ชื่อ-นามสกุล:    นายสมชาย ใจดี"

    Parameters:
        label (str)              — ข้อความ label ด้านซ้าย
        value_control (Control)  — Widget แสดงค่าด้านขวา
        label_width (int)        — ความกว้างของ label (default: 140px)
    """
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            # ส่วน Label (ด้านซ้าย) — กว้างคงที่ตาม label_width
            ft.Container(
                width=label_width,
                content=ft.Text(label, size=14, color=APP_COLORS["text_muted"]),
            ),
            # ส่วน Value (ด้านขวา) — ขยายเต็มพื้นที่ที่เหลือ
            ft.Container(expand=True, content=value_control),
        ],
    )


def FormDetailCard(content: ft.Control):
    """
    สร้างการ์ดมาตรฐานสำหรับ Form Detail Screen
    ใช้แทน inline Container ที่เขียนซ้ำกันทุกฟอร์ม
    สไตล์: กล่องขาว, ขอบมน 20px, มีเงา, padding 25px
    """
    return ft.Container(
        bgcolor=APP_COLORS["white"],
        border_radius=20,
        padding=25,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=APP_COLORS["card_shadow"],    # เงาโปร่งใส
            offset=ft.Offset(0, 4),             # เงาลงด้านล่าง 4px
        ),
        content=content,
    )


def FormDetailAppBar(page: ft.Page, user_role: str):
    """
    สร้าง AppBar มาตรฐานสำหรับ Form Detail Screen
    มีปุ่มย้อนกลับ (Arrow Back) ที่นำทางตาม Role:
    - advisor → กลับไปหน้า advisor_activities
    - student → กลับไปหน้า student_home
    """
    return ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=APP_COLORS["black"],
            on_click=lambda _: page.go(
                "/advisor_home" if user_role == "advisor" else "/student_home"
            ),
        ),
        title=ft.Text("KMITL", color=APP_COLORS["black"], weight="bold"),
        center_title=True,
        bgcolor=APP_COLORS["form_background"],
        elevation=0,       # ไม่มีเงาใต้ AppBar
    )
