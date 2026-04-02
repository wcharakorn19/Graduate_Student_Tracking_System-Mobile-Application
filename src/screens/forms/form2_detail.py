# ==============================================================================
# src/screens/forms/form2_detail.py — หน้ารายละเอียดฟอร์ม 2
# ==============================================================================
# แบบเสนอหัวข้อและเค้าโครงวิทยานิพนธ์
# ข้อมูลที่แสดง: ข้อมูลนักศึกษา + อาจารย์ที่ปรึกษา + คณะกรรมการสอบ + กรรมการสำรอง
# โครงสร้างเหมือน Form 1 (Auth Guard → สร้าง UI → Async Load → Update)
# Route: "/form2/{submission_id}"
# ==============================================================================
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


def FormTwoDetailScreen(page: ft.Page, submission_id: str):
    """สร้างหน้าจอรายละเอียด Form 2 (เสนอหัวข้อวิทยานิพนธ์)"""
    controller = FormController()

    # Auth Guard
    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route=f"/form2/{submission_id}",
            controls=[ft.Text("Redirecting to login...")],
        )
    user_role = page.session.get("user_role")

    # ── สร้างตัวแปร UI รอรับข้อมูล ──
    student_name_val = form_text_value("Loading...")
    student_id_val = form_text_value("Loading...")
    degree_val = form_text_value()
    program_val = form_text_value()
    dept_val = form_text_value()

    # ตัวแปรสำหรับอาจารย์ที่ปรึกษาและคณะกรรมการสอบ
    main_advisor_val = form_text_value("Loading...")
    co_advisor_val = form_text_value()
    chair_val = form_text_value()           # ประธานกรรมการสอบ
    committee_val = form_text_value()       # กรรมการ (ที่ปรึกษาร่วม 2)
    member5_val = form_text_value()         # กรรมการสอบ คนที่ 5
    reserve_ext_val = form_text_value()     # กรรมการสำรอง (ภายนอก)
    reserve_int_val = form_text_value()     # กรรมการสำรอง (ภายใน)

    # ── ฟังก์ชันโหลดข้อมูลแบบ Async ──
    async def load_data(e=None):
        result = await controller.get_form2_detail(submission_id)

        if result["success"]:
            data = result["data"]
            student_name_val.value = data["student_name"]
            student_id_val.value = data["student_id"]
            degree_val.value = data["degree"]
            program_val.value = data["program_name"]
            dept_val.value = data["department_name"]

            main_advisor_val.value = data["main_advisor"]
            co_advisor_val.value = data["co_advisor"]
            chair_val.value = data["chair"]
            committee_val.value = data["committee"]
            member5_val.value = data["member5"]
            reserve_ext_val.value = data["reserve_ext"]
            reserve_int_val.value = data["reserve_int"]
        else:
            student_name_val.value = result["message"]
            student_name_val.color = "red"

        page.update()

    # ── ประกอบร่าง Layout ──

    # การ์ดข้อมูลนักศึกษา
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

    # การ์ดอาจารย์ที่ปรึกษาและคณะกรรมการสอบ
    committee_card = FormDetailCard(
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text(
                    "อาจารย์ที่ปรึกษาและคณะกรรมการสอบ",
                    size=16,
                    weight="bold",
                    color=APP_COLORS["black"],
                ),
                ft.Divider(height=10, color="transparent"),
                create_form_row("อาจารย์ที่ปรึกษาหลัก:", main_advisor_val),
                create_form_row("อาจารย์ที่ปรึกษาร่วม:", co_advisor_val),
                ft.Divider(height=20, color=APP_COLORS["divider"]),
                # ส่วนคณะกรรมการสอบ
                ft.Text(
                    "ชื่อคณะกรรมการสอบ",
                    size=15,
                    weight="bold",
                    color=APP_COLORS["black"],
                ),
                create_form_row("ประธานกรรมการสอบ:", chair_val),
                create_form_row("กรรมการ (ที่ปรึกษาร่วม 2):", committee_val),
                create_form_row("กรรมการสอบ (คนที่ 5):", member5_val),
                ft.Divider(height=20, color=APP_COLORS["divider"]),
                # ส่วนกรรมการสำรอง
                ft.Text(
                    "ชื่อคณะกรรมการสำรอง",
                    size=15,
                    weight="bold",
                    color=APP_COLORS["black"],
                ),
                create_form_row("กรรมการสำรอง (ภายนอก):", reserve_ext_val),
                create_form_row("กรรมการสำรอง (ภายใน):", reserve_int_val),
            ],
        )
    )

    page.run_task(load_data)

    return ft.View(
        route=f"/form2/{submission_id}",
        bgcolor=APP_COLORS["form_background"],
        scroll=ft.ScrollMode.AUTO,
        appbar=FormDetailAppBar(page, user_role),
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, bottom=10, top=20),
                        content=ft.Text(
                            "แบบเสนอหัวข้อและเค้าโครงวิทยานิพนธ์",
                            size=18,
                            weight="bold",
                            color=APP_COLORS["black"],
                            text_align="center",
                        ),
                        alignment=ft.alignment.center,
                    ),
                    student_card,
                    ft.Container(padding=5),
                    committee_card,
                    ft.Container(padding=20),
                ]
            )
        ],
    )
