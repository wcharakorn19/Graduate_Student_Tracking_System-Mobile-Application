# src/screens/advisor/advisor_home.py
import flet as ft
from controllers.advisor_controller import AdvisorController
from components.my_card import MyCard 

def AdvisorHome(page: ft.Page):
    controller = AdvisorController()
    
    # 🌟 Logic: ดึงค่าพื้นฐาน
    user_id = page.session.get("user_id")
    user_full_name = page.session.get("user_full_name") or "อาจารย์"
    
    # 🌟 UI Component: สร้างพื้นที่รอรับข้อมูล
    cards_list = ft.Column(spacing=35)

    # 🌟 Event Logic: แยกฟังก์ชันการนำทาง
    def navigate(route):
        page.go(route)

    cards_list = ft.Column([ft.ProgressBar(color="#EF3961")])

    # 🌟 State Logic: ฟังก์ชันอัปเดตข้อมูลบนจอ
    def load_data():
        # เรียก ViewModel ที่แต่งตัวเสร็จแล้วมาจาก Controller
        result = controller.get_dashboard_view_model(user_id, user_full_name)
        
        if result["success"]:
            # Logic: วนลูปวาดการ์ดแบบ Dynamic
            cards_list.controls = [
                MyCard(
                    item["title"], 
                    item["subtitle"], 
                    item["icon"], 
                    lambda _, r=item["route"]: navigate(r)
                ) for item in result["view_model"]
            ]
            page.update()

    # 🌟 UI Structure: ส่วนแสดงผลเพียวๆ
    load_data() # เรียกใช้ Logic โหลดข้อมูล

    return ft.View(
        route="/teacher_home",
        bgcolor="#FFF6FE",
        controls=[
            ft.AppBar(
                title=ft.Text("หน้าหลักอาจารย์", color="white"),
                center_title=True,
                bgcolor="#EF3961",
                automatically_imply_leading=False, 
                actions=[ft.IconButton(ft.Icons.LOGOUT, icon_color="white", on_click=lambda _: navigate("/"))]
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(f"สวัสดี, {user_full_name}", size=22, weight=ft.FontWeight.BOLD),
                    ft.Container(height=25),
                    cards_list
                ]),
                padding=ft.padding.only(top=30, left=20, right=20)
            )
        ]
    )