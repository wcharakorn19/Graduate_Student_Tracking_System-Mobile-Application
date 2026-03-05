# src/components/inputs.py
import flet as ft

class AppTextField(ft.TextField):
    def __init__(self, label: str, is_password: bool = False, **kwargs):
        
        # ส่ง kwargs อื่นๆ ให้คลาสแม่จัดการเผื่อคุณอยากส่ง width หรือ on_change เข้ามา
        super().__init__(**kwargs) 
        
        # 1. รับข้อความ Label ไปแสดงผล
        self.label = label
        
        # 2. เวทมนตร์ทางลัด: ถ้า is_password เป็น True ให้เปิดโหมดรหัสผ่านและปุ่มลูกตาเลย
        self.password = is_password
        self.can_reveal_password = is_password
        
        # 3. กำหนดสไตล์ตายตัวที่ใช้เหมือนกันทุกช่อง (ไม่ต้องไปพิมพ์ซ้ำที่หน้าจอแล้ว)
        self.border_radius = 10
        self.bgcolor = "#FFFFFF"
        self.border_color = "transparent"
        self.text_size = 16
        self.color = "#000000"
        