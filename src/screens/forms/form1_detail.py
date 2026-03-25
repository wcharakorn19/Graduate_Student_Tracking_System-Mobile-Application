# src/screens/forms/form1_detail.py
import flet as ft
from controllers.form_controller import FormController
from core.auth_guard import require_auth
from core.config import APP_COLORS
from components.form_helpers import (
    create_form_row,
    FormDetailCard,
    FormDetailAppBar,
    form_text_value,
)


def FormOneDetailScreen(page: ft.Page, submission_id: str):
    controller = FormController()

    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route=f"/form1/{submission_id}",
            controls=[ft.Text("Redirecting to login...")],
        )
    user_role = page.session.get("user_role")

    # UI Components (รอรับข้อมูล)
    student_name_val = form_text_value("Loading...")
    student_id_val = form_text_value("Loading...")
    degree_val = form_text_value()
    program_val = form_text_value()
    dept_val = form_text_value()
    faculty_val = form_text_value()
    plan_val = form_text_value()
    phone_val = form_text_value()
    email_val = form_text_value()
    main_advisor_val = form_text_value("Loading...")
    co_advisor_val = form_text_value()

    # 🌟 ฟังก์ชันโหลดข้อมูลแบบ Async
    async def load_data(e=None):
        result = await controller.get_form1_detail(submission_id)

        if result["success"]:
            data = result["data"]
            student_name_val.value = data["student_name"]
            student_id_val.value = data["student_id"]
            degree_val.value = data["degree"]
            program_val.value = data["program_name"]
            dept_val.value = data["department_name"]
            faculty_val.value = data["faculty"]
            plan_val.value = data["plan"]
            phone_val.value = data["phone"]
            email_val.value = data["email"]
            main_advisor_val.value = data["main_advisor"]
            co_advisor_val.value = data["co_advisor"]
        else:
            student_name_val.value = result["message"]
            student_name_val.color = "red"

        page.update()

    # --- ประกอบร่าง Layout ---
    student_card = FormDetailCard(
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text(
                    "ข้อมูลนักศึกษา", size=16, weight="bold", color=APP_COLORS["black"]
                ),
                ft.Divider(height=10, color="transparent"),
                create_form_row("ชื่อ-นามสกุล:", student_name_val, label_width=120),
                create_form_row("รหัสนักศึกษา:", student_id_val, label_width=120),
                create_form_row("ระดับการศึกษา:", degree_val, label_width=120),
                create_form_row("หลักสูตร:", program_val, label_width=120),
                create_form_row("ภาควิชา:", dept_val, label_width=120),
                create_form_row("คณะ:", faculty_val, label_width=120),
                create_form_row("แผนการเรียน:", plan_val, label_width=120),
                create_form_row("เบอร์โทรศัพท์:", phone_val, label_width=120),
                create_form_row("อีเมล:", email_val, label_width=120),
            ],
        )
    )

    advisor_card = FormDetailCard(
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text(
                    "อาจารย์ที่ปรึกษา",
                    size=16,
                    weight="bold",
                    color=APP_COLORS["black"],
                ),
                ft.Divider(height=10, color="transparent"),
                create_form_row(
                    "อาจารย์ที่ปรึกษาหลัก:", main_advisor_val, label_width=120
                ),
                ft.Divider(height=1, color=APP_COLORS["divider"]),
                create_form_row(
                    "อาจารย์ที่ปรึกษาร่วม:", co_advisor_val, label_width=120
                ),
            ],
        )
    )

    page.run_task(load_data)

    return ft.View(
        route=f"/form1/{submission_id}",
        bgcolor=APP_COLORS["form_background"],
        scroll=ft.ScrollMode.AUTO,
        appbar=FormDetailAppBar(page, user_role),
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, bottom=10, top=20),
                        content=ft.Text(
                            "แบบฟอร์มขอรับรองการเป็นอาจารย์\nที่ปรึกษาวิทยานิพนธ์ หลัก/ร่วม",
                            size=18,
                            weight="bold",
                            color=APP_COLORS["black"],
                            text_align="center",
                        ),
                        alignment=ft.alignment.center,
                    ),
                    student_card,
                    ft.Container(padding=5),
                    advisor_card,
                    ft.Container(padding=20),
                ]
            )
        ],
    )
