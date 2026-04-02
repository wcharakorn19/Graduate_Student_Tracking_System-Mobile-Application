# ==============================================================================
# src/components/base_card.py — Component การ์ดพื้นฐาน (Reusable Card)
# ==============================================================================
# ไฟล์นี้สร้าง Component การ์ด (Card) ที่ใช้ร่วมกันทั้งแอป
# ทุกการ์ดที่แสดงเป็นกล่องขาวมีเงา ใช้ BaseCard เป็นตัวตั้งต้น
# ช่วยลดโค้ดซ้ำ: ไม่ต้องกำหนด bgcolor, padding, shadow ทุกครั้ง
#
# การใช้งาน: BaseCard(content=ft.Column([...]))
# ==============================================================================
import flet as ft


class BaseCard(ft.Container):
    """
    Component การ์ดพื้นฐาน — สืบทอดจาก ft.Container (กล่อง)
    ตั้งค่า Default Styling:
    - bgcolor: สีขาว
    - padding: ระยะห่างภายใน 20px
    - border_radius: ขอบมน 15px
    - width: เต็มความกว้าง
    - shadow: เงาสีดำจางๆ ให้ดูลอยขึ้นมา (Elevation Effect)
    """
    def __init__(self, content, **kwargs):
        # --- ตั้งค่า Default Styling ---
        # ใช้ setdefault เพื่อให้ผู้เรียกสามารถ override ค่าเหล่านี้ได้
        kwargs.setdefault("bgcolor", "white")
        kwargs.setdefault("padding", 20)
        kwargs.setdefault("border_radius", 15)
        kwargs.setdefault("width", float("inf"))   # เต็มความกว้าง
        kwargs.setdefault(
            "shadow",
            ft.BoxShadow(blur_radius=15, color="black12", offset=ft.Offset(0, 5)),
        )

        # ส่ง kwargs ให้ ft.Container (คลาสแม่) จัดการ
        super().__init__(**kwargs)
        # กำหนดเนื้อหาภายในการ์ด
        self.content = content
