# ==============================================================================
# src/components/buttons.py — Component ปุ่มกดหลัก (Primary Button)
# ==============================================================================
# ไฟล์นี้สร้าง PrimaryButton ที่ใช้ร่วมกันทั้งแอป
# ทำให้ทุกปุ่มมีสไตล์เดียวกัน (สีชมพูแดง + พื้นหลังอ่อน)
# ไม่ต้องกำหนดสีและสไตล์ซ้ำทุกหน้าจอ
# ==============================================================================
import flet as ft
from core.config import APP_COLORS      # นำเข้าชุดสีกลาง


class PrimaryButton(ft.ElevatedButton):
    """
    ปุ่มหลักของแอป — สืบทอดจาก ft.ElevatedButton
    สไตล์:
    - สีตัวอักษร: สี background (ชมพูอ่อน)
    - สีพื้นหลัง: สี primary (ชมพูแดง)
    - padding + weight สามารถกำหนดเพิ่มได้ตอนเรียกใช้
    """
    def __init__(self, text: str, on_click=None, padding=None, weight=None, **kwargs):

        super().__init__(**kwargs)

        self.text = text            # ข้อความบนปุ่ม
        self.on_click = on_click    # ฟังก์ชันที่เรียกเมื่อกดปุ่ม
        # กำหนดสไตล์ปุ่มจากชุดสีกลาง
        self.style = ft.ButtonStyle(
            color=APP_COLORS["background"],     # สีตัวอักษร (ชมพูอ่อน)
            bgcolor=APP_COLORS["primary"],      # สีพื้นหลังปุ่ม (ชมพูแดง)
            padding=padding,                    # ระยะห่างภายใน
            text_style=ft.TextStyle(weight=weight),  # น้ำหนักตัวอักษร (เช่น bold)
        )