# ==============================================================================
# src/screens/forms/exam_result_detail.py — หน้ารายละเอียดผลสอบ
# ==============================================================================
# แบบฟอร์มยื่นผลการสอบ
# ข้อมูลที่แสดง: ข้อมูลนักศึกษา + ข้อมูลผลสอบ + ไฟล์แนบ (กดดูได้)
# ฟอร์มนี้มีส่วนไฟล์แนบที่กดเปิด URL ได้
# Route: "/exam_result/{submission_id}"
# ==============================================================================
import flet as ft
from controllers.form_controller import FormController
from core.auth_guard import require_auth
from core.config import APP_COLORS
from components.form_helpers import (
    create_form_row, FormDetailCard, FormDetailAppBar, form_text_value,
)


def ExamResultDetailScreen(page: ft.Page, submission_id: str):
    """สร้างหน้าจอรายละเอียดผลสอบ"""
    controller = FormController()

    user_id = require_auth(page)
    if not user_id:
        return ft.View(route=f"/exam_result/{submission_id}", controls=[ft.Text("Redirecting...")])
    user_role = page.session.get("user_role")

    # ── ตัวแปร UI ──
    student_name_val = form_text_value("Loading...")
    student_id_val = form_text_value("Loading...")
    degree_val = form_text_value()
    program_val = form_text_value()
    doc_type_val = form_text_value()        # ประเภทเอกสาร
    exam_type_val = form_text_value()       # ประเภทการสอบ
    exam_date_val = form_text_value()       # วันที่สอบ
    result_val = form_text_value()          # ผลสอบ/คะแนน
    file_list_container = ft.Column(spacing=10)  # รายการไฟล์แนบ

    # ── โหลดข้อมูลแบบ Async ──
    async def load_data(e=None):
        result = await controller.get_exam_result_detail(submission_id)

        if result["success"]:
            data = result["data"]
            student_name_val.value = data["student_name"]
            student_id_val.value = data["student_id"]
            degree_val.value = data["degree"]
            program_val.value = data["program_name"]
            doc_type_val.value = data["doc_type"]
            exam_type_val.value = data["exam_type"]
            exam_date_val.value = data["exam_date"]
            result_val.value = data["result_score"]

            # ── จัดการไฟล์แนบ ──
            file_list_container.controls.clear()
            # URL ตัวอย่าง (Mock) สำหรับเปิดไฟล์
            base_url = "https://drive.google.com/file/d/1X1PZGikJcvxwvGCbWQLAbs-s01_8XQCB/view?usp=share_link"

            if data["files"]:
                for f in data["files"]:
                    file_name = f.get("name", "Unknown File")
                    full_url = f"{base_url}{file_name}"
                    # สร้างแถวไฟล์ (กดเปิดได้)
                    file_row = ft.Container(
                        padding=10, bgcolor="#F9F9F9", border_radius=10,
                        on_click=lambda e, url=full_url: page.launch_url(url),
                        content=ft.Row([
                            ft.Icon(ft.Icons.INSERT_DRIVE_FILE, color="#5E5CE6", size=30),
                            ft.Column([
                                ft.Text(file_name, size=14, color=APP_COLORS["text_dark"],
                                    weight="bold", overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text("แตะเพื่อเปิดไฟล์ (Mock)", size=12, color="grey"),
                            ], spacing=2),
                        ], alignment=ft.MainAxisAlignment.START),
                    )
                    file_list_container.controls.append(file_row)
            else:
                file_list_container.controls.append(
                    ft.Text("ไม่มีไฟล์แนบ", size=14, color="grey")
                )
        else:
            student_name_val.value = result["message"]
            student_name_val.color = "red"
        page.update()

    # ── Layout ──
    student_card = FormDetailCard(content=ft.Column(spacing=12, controls=[
        ft.Text("ข้อมูลนักศึกษา", size=16, weight="bold", color=APP_COLORS["black"]),
        ft.Divider(height=10, color="transparent"),
        create_form_row("ชื่อ-นามสกุล:", student_name_val),
        create_form_row("รหัสนักศึกษา:", student_id_val),
        create_form_row("ระดับปริญญา:", degree_val),
        create_form_row("หลักสูตรและสาขาวิชา:", program_val),
    ]))

    exam_card = FormDetailCard(content=ft.Column(spacing=12, controls=[
        ft.Text("ข้อมูลผลสอบ", size=16, weight="bold", color=APP_COLORS["black"]),
        ft.Divider(height=10, color="transparent"),
        create_form_row("ประเภทเอกสาร:", doc_type_val),
        create_form_row("ประเภทการสอบ:", exam_type_val),
        create_form_row("วันที่สอบ:", exam_date_val),
        create_form_row("ผลสอบ/คะแนน:", result_val),
    ]))

    # การ์ดไฟล์แนบ (เฉพาะ Exam Result)
    file_card = FormDetailCard(content=ft.Column(spacing=12, controls=[
        ft.Text("หลักฐานยื่นสอบ", size=16, weight="bold", color=APP_COLORS["black"]),
        ft.Divider(height=10, color="transparent"),
        file_list_container,
    ]))

    page.run_task(load_data)

    return ft.View(
        route=f"/exam_result/{submission_id}",
        bgcolor=APP_COLORS["form_background"],
        scroll=ft.ScrollMode.AUTO,
        appbar=FormDetailAppBar(page, user_role),
        controls=[ft.Column(controls=[
            ft.Container(
                padding=ft.padding.only(left=20, right=20, bottom=10, top=20),
                content=ft.Text("รายละเอียดการยื่นผลสอบ", size=18, weight="bold",
                    color=APP_COLORS["black"], text_align="center"),
                alignment=ft.alignment.center,
            ),
            student_card, ft.Container(padding=5), exam_card,
            ft.Container(padding=5), file_card, ft.Container(padding=20),
        ])],
    )
