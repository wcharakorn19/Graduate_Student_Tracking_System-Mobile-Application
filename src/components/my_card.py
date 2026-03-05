# src/components/my_card.py
import flet as ft

class MyCard(ft.Container):
    def __init__(self, title, subtitle, icon_name, on_click=None):
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self.icon_name = icon_name
        self.on_click = on_click
        
        # --- การตั้งค่าสไตล์ของ Card ---
        self.padding = 20
        self.border_radius = 15
        self.bgcolor = "white"
        self.width = float("inf") # ขยายเต็มความกว้างที่ใส่
        
        # ใส่เงาให้ดูมีมิติ (Shadow)
        self.shadow = ft.BoxShadow(
            blur_radius=15,
            color="black12",
            offset=ft.Offset(0, 5)
        )
        
        # เอฟเฟกต์ตอนเอาเมาส์ไปวางหรือกด
        self.animate = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        
        # --- ส่วนประกอบภายใน Card ---
        self.content = ft.Row(
            controls=[
                # ส่วนของ Icon วงกลมด้านซ้าย
                ft.Container(
                    content=ft.Icon(self.icon_name, color="#EF3961", size=28),
                    bgcolor="#FFF0F3",
                    padding=15,
                    border_radius=50,
                ),
                
                # ส่วนของข้อความตรงกลาง
                ft.Column(
                    controls=[
                        ft.Text(
                            value=self.title,
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="black",
                        ),
                        ft.Text(
                            value=self.subtitle,
                            size=14,
                            color="black54",
                        ),
                    ],
                    spacing=2,
                    expand=True, # ให้ข้อความกินพื้นที่ที่เหลือ
                ),
                
                # ลูกศรชี้ไปทางขวา (Chevron)
                ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color="black26")
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # เอฟเฟกต์ Hover (แถมให้เผื่อรันบนเว็บจะดูหรูมาก)
    def on_hover(self, e):
        self.scale = 1.02 if e.data == "true" else 1.0
        self.update()