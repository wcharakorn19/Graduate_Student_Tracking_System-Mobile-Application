# ==============================================================================
# src/components/error_banner.py — Component แบนเนอร์แสดง Error
# ==============================================================================
# ไฟล์นี้สร้าง ErrorBanner สำหรับแสดงข้อความแจ้งเตือนเมื่อเกิดข้อผิดพลาด
# ออกแบบเป็นกล่องสีแดงอ่อนพร้อมไอคอน Error
# ใช้ร่วมกันทุกหน้าจอ เพื่อให้ Error แสดงผลเหมือนกันหมด
# ==============================================================================
import flet as ft


class ErrorBanner(ft.Container):
    """
    Component แบนเนอร์แสดง Error — สืบทอดจาก ft.Container
    สไตล์:
    - พื้นหลังสีแดงอ่อน (RED_50)
    - ขอบสีแดง (RED_200)
    - ไอคอน Error สีแดงเข้ม + ข้อความ Error สีแดงเข้ม
    - มุมมน 10px + ระยะห่างด้านล่าง 15px
    """
    def __init__(self, message: str):
        super().__init__()
        # --- ตั้งค่าสไตล์กล่อง ---
        self.bgcolor = ft.Colors.RED_50               # พื้นหลังแดงอ่อน
        self.padding = 15                             # ระยะห่างภายใน
        self.border_radius = 10                       # ขอบมน
        self.border = ft.border.all(1, ft.Colors.RED_200)  # เส้นขอบแดง
        self.margin = ft.margin.only(bottom=15)       # ระยะห่างด้านล่าง

        # --- เนื้อหาภายใน: ไอคอน + ข้อความ เรียงแนวนอน ---
        self.content = ft.Row(
            controls=[
                # ไอคอน Error (วงกลมมีเครื่องหมายตกใจ)
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_700, size=24),
                # ข้อความ Error
                ft.Text(
                    message,
                    color=ft.Colors.RED_900,            # สีแดงเข้ม
                    weight=ft.FontWeight.W_500,         # น้ำหนักตัวอักษรปานกลาง
                    size=14,
                    expand=True,                        # ขยายเต็มพื้นที่ที่เหลือ
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
