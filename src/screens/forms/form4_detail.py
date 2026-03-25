# src/screens/forms/form4_detail.py
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


def FormFourDetailScreen(page: ft.Page, submission_id: str):
    controller = FormController()

    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route=f"/form4/{submission_id}",
            controls=[ft.Text("Redirecting to login...")],
        )
    user_role = page.session.get("user_role")

    # --- 1. สร้างตัวแปร UI รอรับข้อมูล ---
    student_name_val = form_text_value("Loading...")
    student_id_val = form_text_value("Loading...")
    degree_val = form_text_value()
    program_val = form_text_value()
    dept_val = form_text_value()

    approve_date_val = form_text_value()
    title_th_val = form_text_value()
    title_en_val = form_text_value()

    expert_title_val = form_text_value()
    expert_name_val = form_text_value()
    expert_surname_val = form_text_value()
    expert_org_val = form_text_value()
    expert_phone_val = form_text_value()
    expert_email_val = form_text_value()

    # --- 2. ฟังก์ชันดึงข้อมูลแบบ Async ---
    async def load_data(e=None):
        result = await controller.get_form4_detail(submission_id)

        if result["success"]:
            data = result["data"]
            student_name_val.value = data["student_name"]
            student_id_val.value = data["student_id"]
            degree_val.value = data["degree"]
            program_val.value = data["program_name"]
            dept_val.value = data["department_name"]

            approve_date_val.value = data["approve_date"]
            title_th_val.value = data["title_th"]
            title_en_val.value = data["title_en"]

            expert_title_val.value = data["expert_title"]
            expert_name_val.value = data["expert_name"]
            expert_surname_val.value = data["expert_surname"]
            expert_org_val.value = data["expert_org"]
            expert_phone_val.value = data["expert_phone"]
            expert_email_val.value = data["expert_email"]
        else:
            student_name_val.value = result["message"]
            student_name_val.color = "red"

        page.update()

    # --- 3. Layout ประกอบร่าง ---
    student_card = FormDetailCard(
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text(
                    "ข้อมูลนักศึกษา", size=16, weight="bold", color=APP_COLORS["black"]
                ),
                ft.Divider(height=10, color="transparent"),
                create_form_row("ชื่อ-นามสกุล:", student_name_val),
                create_form_row("รหัสนักศึกษา:", student_id_val),
                create_form_row("ระดับปริญญา:", degree_val),
                create_form_row("หลักสูตรและสาขาวิชา:", program_val),
                create_form_row("ภาควิชา:", dept_val),
            ],
        )
    )

    thesis_card = FormDetailCard(
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text(
                    "ข้อมูลหัวข้อวิทยานิพนธ์ (ที่ได้อนุมัติ)",
                    size=16,
                    weight="bold",
                    color=APP_COLORS["black"],
                ),
                ft.Divider(height=10, color="transparent"),
                create_form_row("วันที่เสนอเค้าโครงได้รับอนุมัติ:", approve_date_val),
                create_form_row("ชื่อเรื่อง (TH):", title_th_val),
                create_form_row("ชื่อเรื่อง (ENG):", title_en_val),
            ],
        )
    )

    expert_card = FormDetailCard(
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text(
                    "ข้อมูลผู้ทรงคุณวุฒิ คนที่ 1",
                    size=16,
                    weight="bold",
                    color=APP_COLORS["black"],
                ),
                ft.Divider(height=10, color="transparent"),
                create_form_row("คำนำหน้า/ ยศ(ตำแหน่ง):", expert_title_val),
                create_form_row("ชื่อ:", expert_name_val),
                create_form_row("นามสกุล:", expert_surname_val),
                create_form_row("สถาบัน/หน่วยงาน:", expert_org_val),
                create_form_row("เบอร์โทรศัพท์:", expert_phone_val),
                create_form_row("อีเมล:", expert_email_val),
            ],
        )
    )

    page.run_task(load_data)

    return ft.View(
        route=f"/form4/{submission_id}",
        bgcolor=APP_COLORS["form_background"],
        scroll=ft.ScrollMode.AUTO,
        appbar=FormDetailAppBar(page, user_role),
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, bottom=10, top=20),
                        content=ft.Text(
                            "แบบขอหนังสือเชิญเป็นผู้ทรงคุณวุฒิ\nตรวจและประเมิน...เพื่อวิจัย",
                            size=18,
                            weight="bold",
                            color=APP_COLORS["black"],
                            text_align="center",
                        ),
                        alignment=ft.alignment.center,
                    ),
                    student_card,
                    ft.Container(padding=5),
                    thesis_card,
                    ft.Container(padding=5),
                    expert_card,
                    ft.Container(padding=20),
                ]
            )
        ],
    )
