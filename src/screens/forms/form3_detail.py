# ==============================================================================
# src/screens/forms/form3_detail.py — หน้ารายละเอียดฟอร์ม 3
# ==============================================================================
# แบบเสนอหัวข้อและเค้าโครงวิทยานิพนธ์ เล่ม 1
# ข้อมูลที่แสดง: ข้อมูลนักศึกษา + หัวข้อวิทยานิพนธ์ที่อนุมัติ + อาจารย์ผู้รับผิดชอบ
# Route: "/form3/{submission_id}"
# ==============================================================================
import flet as ft
from controllers.form_controller import FormController
from core.auth_guard import require_auth
from core.config import APP_COLORS
from components.form_helpers import (
    create_form_row, FormDetailCard, FormDetailAppBar, form_text_value,
)


def FormThreeDetailScreen(page: ft.Page, submission_id: str):
    """สร้างหน้าจอรายละเอียด Form 3 (เค้าโครงวิทยานิพนธ์ เล่ม 1)"""
    controller = FormController()

    user_id = require_auth(page)
    if not user_id:
        return ft.View(route=f"/form3/{submission_id}", controls=[ft.Text("Redirecting to login...")])
    user_role = page.session.get("user_role")

    # ── สร้างตัวแปร UI ──
    student_name_val = form_text_value("Loading...")
    student_id_val = form_text_value("Loading...")
    degree_val = form_text_value()
    program_val = form_text_value()
    dept_val = form_text_value()

    approve_date_val = form_text_value()    # วันที่อนุมัติหัวข้อ
    title_th_val = form_text_value()        # ชื่อเรื่อง (ภาษาไทย)
    title_en_val = form_text_value()        # ชื่อเรื่อง (ภาษาอังกฤษ)

    chair_val = form_text_value()           # ประธานกรรมการสอบ
    main_advisor_val = form_text_value()
    co_advisor_val = form_text_value()

    # ── โหลดข้อมูลแบบ Async ──
    async def load_data(e=None):
        result = await controller.get_form3_detail(submission_id)

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

            chair_val.value = data["chair"]
            main_advisor_val.value = data["main_advisor"]
            co_advisor_val.value = data["co_advisor"]
        else:
            student_name_val.value = result["message"]
            student_name_val.color = "red"

        page.update()

    # ── ประกอบร่าง Layout ──
    student_card = FormDetailCard(
        content=ft.Column(spacing=12, controls=[
            ft.Text("ข้อมูลนักศึกษา", size=16, weight="bold", color=APP_COLORS["black"]),
            ft.Divider(height=10, color="transparent"),
            create_form_row("ชื่อ-นามสกุล:", student_name_val),
            create_form_row("รหัสนักศึกษา:", student_id_val),
            create_form_row("ระดับปริญญา:", degree_val),
            create_form_row("หลักสูตรและสาขาวิชา:", program_val),
            create_form_row("ภาควิชา:", dept_val),
        ])
    )

    # การ์ดหัวข้อวิทยานิพนธ์ + อาจารย์ผู้รับผิดชอบ
    thesis_card = FormDetailCard(
        content=ft.Column(spacing=12, controls=[
            ft.Text("ข้อมูลหัวข้อวิทยานิพนธ์ (ที่ได้อนุมัติ)", size=16, weight="bold", color=APP_COLORS["black"]),
            ft.Divider(height=10, color="transparent"),
            create_form_row("วันที่อนุมัติหัวข้อ:", approve_date_val),
            create_form_row("ชื่อเรื่อง (TH):", title_th_val),
            create_form_row("ชื่อเรื่อง (ENG):", title_en_val),
            ft.Divider(height=20, color=APP_COLORS["divider"]),
            ft.Text("อาจารย์ผู้รับผิดชอบ", size=16, weight="bold", color=APP_COLORS["black"]),
            create_form_row("ประธานกรรมการสอบ:", chair_val),
            create_form_row("อาจารย์ที่ปรึกษาหลัก:", main_advisor_val),
            create_form_row("อาจารย์ที่ปรึกษาร่วม 1:", co_advisor_val),
        ])
    )

    page.run_task(load_data)

    return ft.View(
        route=f"/form3/{submission_id}",
        bgcolor=APP_COLORS["form_background"],
        scroll=ft.ScrollMode.AUTO,
        appbar=FormDetailAppBar(page, user_role),
        controls=[ft.Column(controls=[
            ft.Container(
                padding=ft.padding.only(left=20, right=20, bottom=10, top=20),
                content=ft.Text("แบบเสนอหัวข้อ\nและเค้าโครงวิทยานิพนธ์ เล่ม 1", size=18, weight="bold", color=APP_COLORS["black"], text_align="center"),
                alignment=ft.alignment.center,
            ),
            student_card, ft.Container(padding=5), thesis_card, ft.Container(padding=20),
        ])],
    )
