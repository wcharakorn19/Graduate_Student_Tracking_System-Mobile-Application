# ==============================================================================
# src/components/inputs.py — Component ช่องกรอกข้อมูล (Text Field)
# ==============================================================================
# ไฟล์นี้สร้าง AppTextField ที่ใช้ร่วมกันทั้งแอป
# รวมสไตล์ไว้ที่เดียว ไม่ต้องกำหนดซ้ำทุกหน้าจอ
# รองรับโหมดรหัสผ่าน (ซ่อนตัวอักษร + ปุ่มเปิด-ปิดตา)
# ==============================================================================
import flet as ft


class AppTextField(ft.TextField):
    """
    Component ช่องกรอกข้อมูลมาตรฐาน — สืบทอดจาก ft.TextField
    ตั้งค่า Default Styling ให้ทุกช่องกรอกมีหน้าตาเหมือนกัน

    Parameters:
        label (str) — ข้อความที่แสดงใน label
        is_password (bool) — ถ้า True จะเปิดโหมดรหัสผ่าน (ซ่อนตัวอักษร + ปุ่มตา)
    """
    def __init__(self, label: str, is_password: bool = False, **kwargs):

        # ส่ง kwargs อื่นๆ ให้คลาสแม่จัดการ (เช่น width, on_change)
        super().__init__(**kwargs)

        # 1. รับข้อความ Label ไปแสดงผล
        self.label = label

        # 2. โหมดรหัสผ่าน: ถ้า is_password เป็น True → ซ่อนตัวอักษร + แสดงปุ่มลูกตา
        self.password = is_password
        self.can_reveal_password = is_password

        # 3. กำหนดสไตล์ตายตัวที่ใช้เหมือนกันทุกช่อง
        self.border_radius = 10         # ขอบมน
        self.bgcolor = "#FFFFFF"        # พื้นหลังขาว
        self.border_color = "transparent"   # ไม่แสดงเส้นขอบ
        self.text_size = 16             # ขนาดตัวอักษร
        self.color = "#000000"          # สีตัวอักษร (ดำ)