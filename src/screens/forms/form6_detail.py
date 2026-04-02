# ==============================================================================
# src/screens/forms/form6_detail.py — ฟอร์ม 6: แต่งตั้งกรรมการสอบสุดท้าย
# Route: "/form6/{submission_id}"
# ==============================================================================
import flet as ft
from controllers.form_controller import FormController
from core.auth_guard import require_auth
from core.config import APP_COLORS
from components.form_helpers import (
    create_form_row, FormDetailCard, FormDetailAppBar, form_text_value,
)


def FormSixDetailScreen(page: ft.Page, submission_id: str):
    controller = FormController()
    user_id = require_auth(page)
    if not user_id:
        return ft.View(route=f"/form6/{submission_id}", controls=[ft.Text("Redirecting...")])
    user_role = page.session.get("user_role")

    # ── ตัวแปร UI ──
    student_name_val = form_text_value("Loading...")
    student_id_val = form_text_value("Loading...")
    degree_val = form_text_value()
    program_val = form_text_value()
    dept_val = form_text_value()
    start_semester_val = form_text_value()
    start_year_val = form_text_value()
    phone_val = form_text_value()
    address_val = form_text_value()
    workplace_val = form_text_value()
    thesis_th_val = form_text_value()
    thesis_en_val = form_text_value()
    main_advisor_val = form_text_value()
    co_advisor_val = form_text_value()
    chair_val = form_text_value()
    committee_val = form_text_value()
    member5_val = form_text_value()
    reserve_ext_val = form_text_value()
    reserve_int_val = form_text_value()

    # ── โหลดข้อมูล Async ──
    async def load_data(e=None):
        result = await controller.get_form6_detail(submission_id)
        if result["success"]:
            d = result["data"]
            student_name_val.value = d["student_name"]
            student_id_val.value = d["student_id"]
            degree_val.value = d["degree"]
            program_val.value = d["program_name"]
            dept_val.value = d["department_name"]
            phone_val.value = d["phone"]
            start_semester_val.value = d["start_semester"]
            start_year_val.value = d["start_year"]
            address_val.value = d["address"]
            workplace_val.value = d["workplace"]
            thesis_th_val.value = d["thesis_th"]
            thesis_en_val.value = d["thesis_en"]
            main_advisor_val.value = d["main_advisor"]
            co_advisor_val.value = d["co_advisor"]
            chair_val.value = d["chair"]
            committee_val.value = d["committee"]
            member5_val.value = d["member5"]
            reserve_ext_val.value = d["reserve_ext"]
            reserve_int_val.value = d["reserve_int"]
        else:
            student_name_val.value = result["message"]
            student_name_val.color = "red"
        page.update()

    lw = 130
    info_card = FormDetailCard(content=ft.Column(spacing=12, controls=[
        ft.Text("ข้อมูลผู้ยื่นคำร้อง", size=16, weight="bold", color=APP_COLORS["black"]),
        ft.Divider(height=10, color="transparent"),
        create_form_row("ชื่อ-สกุล:", student_name_val, label_width=lw),
        create_form_row("รหัสประจำตัว:", student_id_val, label_width=lw),
        create_form_row("ระดับปริญญา:", degree_val, label_width=lw),
        create_form_row("สาขาวิชา:", program_val, label_width=lw),
        create_form_row("ภาควิชา:", dept_val, label_width=lw),
        create_form_row("เริ่มศึกษาภาคเรียนที่:", start_semester_val, label_width=lw),
        create_form_row("ปีการศึกษา:", start_year_val, label_width=lw),
        create_form_row("เบอร์โทร:", phone_val, label_width=lw),
        create_form_row("ที่อยู่ปัจจุบัน:", address_val, label_width=lw),
        create_form_row("สถานที่ทำงาน:", workplace_val, label_width=lw),
        ft.Divider(height=10, color=APP_COLORS["divider"]),
        create_form_row("ชื่อวิทยานิพนธ์ (TH):", thesis_th_val, label_width=lw),
        create_form_row("ชื่อวิทยานิพนธ์ (EN):", thesis_en_val, label_width=lw),
    ]))

    committee_card = FormDetailCard(content=ft.Column(spacing=12, controls=[
        ft.Text("คณะกรรมการสอบและอาจารย์ที่ปรึกษา", size=16, weight="bold", color=APP_COLORS["black"]),
        ft.Divider(height=10, color="transparent"),
        create_form_row("ที่ปรึกษาหลัก:", main_advisor_val, label_width=lw),
        create_form_row("ที่ปรึกษาร่วม 1:", co_advisor_val, label_width=lw),
        ft.Divider(height=20, color=APP_COLORS["divider"]),
        ft.Text("คณะกรรมการสอบ", size=15, weight="bold", color=APP_COLORS["black"]),
        create_form_row("ประธานกรรมการสอบ:", chair_val, label_width=lw),
        create_form_row("กรรมการ (ร่วม 2):", committee_val, label_width=lw),
        create_form_row("กรรมการสอบ (คนที่ 5):", member5_val, label_width=lw),
        ft.Divider(height=20, color=APP_COLORS["divider"]),
        ft.Text("กรรมการสำรอง", size=15, weight="bold", color=APP_COLORS["black"]),
        create_form_row("สำรอง (ภายนอก):", reserve_ext_val, label_width=lw),
        create_form_row("สำรอง (ภายใน):", reserve_int_val, label_width=lw),
    ]))

    page.run_task(load_data)

    return ft.View(
        route=f"/form6/{submission_id}",
        bgcolor=APP_COLORS["form_background"],
        scroll=ft.ScrollMode.AUTO,
        appbar=FormDetailAppBar(page, user_role),
        controls=[ft.Column(controls=[
            ft.Container(
                padding=ft.padding.only(left=20, right=20, bottom=10, top=20),
                content=ft.Text("บันทึกข้อความ: ขอแต่งตั้งคณะกรรมการ\nสอบวิทยานิพนธ์ขั้นสุดท้าย",
                    size=18, weight="bold", color=APP_COLORS["black"], text_align="center"),
                alignment=ft.alignment.center,
            ),
            info_card, ft.Container(padding=5), committee_card, ft.Container(padding=20),
        ])],
    )
