# src/screens/student/student_home.py
import flet as ft
from controllers.student_controller import StudentController
from components.shared_navbar import SharedNavBar
from components.base_card import BaseCard
from components.error_banner import ErrorBanner
from core.auth_guard import require_auth


def StudentHome(page: ft.Page):
    controller = StudentController()

    # 🌟 ดึงข้อมูลจาก Session มาเตรียมไว้ให้พร้อม
    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route="/student_home", controls=[ft.Text("Redirecting to login...")]
        )

    user_name = page.session.get("user_full_name") or "นักศึกษา"

    # --- 1. เตรียมตัวแปร UI ---
    name_text = ft.Text(user_name, size=20, weight=ft.FontWeight.BOLD, color="black")
    doc_name_text = ft.Text(
        "Doc Name: Loading...", weight=ft.FontWeight.BOLD, color="black"
    )
    status_label_text = ft.Text("สถานะ :", color="black54")
    status_value_text = ft.Text(
        "Loading...", size=16, weight=ft.FontWeight.BOLD, color="black"
    )

    activities_list = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)
    error_container = ft.Column(spacing=0)  # กล่องสำหรับใส่ ErrorBanner (ถ้ามี)

    # --- 2. ฟังก์ชันโหลดข้อมูล (จุดที่แก้ไข) ---
    async def load_data(e=None):
        error_container.controls.clear()

        # แสดง Spinner ระหว่างโหลด (ทั้งรอบแรกและ refresh)
        activities_list.controls.clear()
        activities_list.controls.append(
            ft.Container(
                content=ft.ProgressRing(), alignment=ft.alignment.center, padding=20
            )
        )
        page.update()

        # 🌟 แก้ไข: เรียกแบบ Async และอเวก
        result = await controller.get_dashboard_data(user_id, user_name)

        if result["success"]:
            data = result["data"]

            # อัปเดตชื่อบนหน้าจอ (เผื่อมีการเปลี่ยนแปลง)
            name_text.value = data.user_name

            doc_name_text.value = f"Doc Name: {data.current_doc.doc_name}"
            status_label_text.value = data.current_doc.status_label
            status_value_text.value = data.current_doc.status_text

            # จำแนกสีสถานะ Status Card
            status_txt = data.current_doc.status_text
            if "อนุมัติ" in status_txt:
                status_value_text.color = "#4CAF50"  # เขียว
            elif "ปฏิเสธ" in status_txt or "แก้ไข" in status_txt:
                status_value_text.color = "#F44336"  # แดง
            else:
                status_value_text.color = "#FF9800"  # ส้ม (รอดำเนินการ)

            activities_list.controls.clear()
            for act in data.activities:
                form_type = getattr(act, "form_type", "form1")
                sub_id = getattr(act, "submission_id", "")
                target_route = f"/{form_type}/{sub_id}"

                # จำแนกสีตามสถานะ
                if "อนุมัติ" in act.status:
                    status_color = "#4CAF50"  # เขียว
                elif "ปฏิเสธ" in act.status or "แก้ไข" in act.status:
                    status_color = "#F44336"  # แดง
                else:
                    status_color = "#FF9800"  # ส้ม (รอดำเนินการ)

                act_item = ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.FOLDER_OUTLINED, color="black54", size=20
                                ),
                                bgcolor="#F0F0F0",
                                padding=10,
                                border_radius=10,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        act.title,
                                        size=14,
                                        color="black",
                                        weight=ft.FontWeight.W_500,
                                    ),
                                    ft.Text(
                                        f"Status : {act.status}",
                                        size=12,
                                        color=status_color,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                        ]
                    ),
                    bgcolor="white",
                    padding=15,
                    border_radius=10,
                    border=ft.border.all(1, "#E5E5E5"),
                    on_click=lambda e, route=target_route: page.go(route),
                )
                activities_list.controls.append(act_item)

            page.update()
        else:
            # ล้างอันเดิมเผื่อมี error ค้างอยู่ แล้วยัด ErrorBanner เข้าไป
            activities_list.controls.clear()  # clear spinner
            error_msg = result.get("message", "Unknown Error")
            error_container.controls.append(
                ErrorBanner(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {error_msg}")
            )
            page.update()

    # --- 3. สร้าง UI Components ---
    status_card = BaseCard(
        content=ft.Column(
            [
                doc_name_text,
                ft.Container(height=10),
                status_label_text,
                status_value_text,
            ]
        )
    )

    activities_card = BaseCard(content=activities_list, expand=True)

    # รันฟังก์ชันโหลดข้อมูลแบบไม่บล็อก UI
    page.run_task(load_data)

    # --- 4. ประกอบร่าง Layout ---
    main_content = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        name_text,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                error_container,  # วางแจ้งเตือนไว้ใต้ชื่อ
                ft.Container(height=10),
                status_card,
                ft.Container(height=20),
                ft.Text(
                    "Latest Activities",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="black",
                ),
                activities_card,
            ],
            expand=True,
        ),
        padding=ft.padding.only(left=20, right=20, top=50),
        expand=True,
    )

    return ft.View(
        route="/student_home",
        bgcolor="#FFF6FE",
        padding=0,
        controls=[main_content],
        # 🌟 เรียกใช้ SharedNavBar แล้วบอกว่าเราอยู่หน้า "/student_home"
        bottom_appbar=SharedNavBar(page, current_route="/student_home"),
    )
