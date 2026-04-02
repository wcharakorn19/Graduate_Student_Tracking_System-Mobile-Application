# ==============================================================================
# src/screens/forms/form1_detail.py — หน้ารายละเอียดฟอร์ม 1
# ==============================================================================
# แบบฟอร์มขอรับรองการเป็นอาจารย์ที่ปรึกษาวิทยานิพนธ์ หลัก/ร่วม
#
# การทำงาน:
#   1. ตรวจสอบ Auth Guard (ต้อง Login ก่อน)
#   2. สร้างตัวแปร UI ทั้งหมดก่อน (แสดง "Loading...")
#   3. โหลดข้อมูลจาก API แบบ Async ผ่าน FormController
#   4. เมื่อได้ข้อมูล → อัปเดตค่าในตัวแปร UI → page.update()
#
# ข้อมูลที่แสดง: ข้อมูลนักศึกษา + อาจารย์ที่ปรึกษาหลัก/ร่วม
# Route: "/form1/{submission_id}"
#
# หมายเหตุ: Form 2-6 และ Exam Result มีโครงสร้างเดียวกัน
#           แตกต่างกันเฉพาะข้อมูลที่แสดงและ layout ของแต่ละฟอร์ม
# ==============================================================================
import flet as ft
from controllers.form_controller import FormController   # Controller จัดการฟอร์ม
from core.auth_guard import require_auth                 # ตรวจสอบ Login
from core.config import APP_COLORS                      # ชุดสีกลาง
from components.form_helpers import (
    create_form_row,       # สร้างแถว label-value
    FormDetailCard,        # สร้างการ์ดมาตรฐาน
    FormDetailAppBar,      # สร้าง AppBar พร้อมปุ่มกลับ
    form_text_value,       # สร้าง Text widget สำหรับแสดงค่า
)


def FormOneDetailScreen(page: ft.Page, submission_id: str):
    """
    สร้างหน้าจอรายละเอียด Form 1
    รับ submission_id จาก URL parameter เพื่อดึงข้อมูลจาก API
    """
    controller = FormController()

    # ── Auth Guard ──
    user_id = require_auth(page)
    if not user_id:
        return ft.View(
            route=f"/form1/{submission_id}",
            controls=[ft.Text("Redirecting to login...")],
        )
    user_role = page.session.get("user_role")

    # ── ขั้นตอนที่ 1: สร้างตัวแปร UI (แสดงค่าเริ่มต้น "Loading...") ──
    # ตัวแปรเหล่านี้จะถูกอัปเดตค่าเมื่อ API ส่งข้อมูลกลับมา
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

    # ── ขั้นตอนที่ 2: ฟังก์ชันโหลดข้อมูลแบบ Async ──
    async def load_data(e=None):
        """เรียก FormController เพื่อดึงข้อมูล Form 1 แล้วอัปเดต UI"""
        result = await controller.get_form1_detail(submission_id)

        if result["success"]:
            # อัปเดตค่าในตัวแปร UI ทั้งหมด
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
            # กรณี Error → แสดงข้อความ Error แทนชื่อนักศึกษา
            student_name_val.value = result["message"]
            student_name_val.color = "red"

        page.update()

    # ── ขั้นตอนที่ 3: ประกอบร่าง Layout ──

    # การ์ดข้อมูลนักศึกษา
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

    # การ์ดอาจารย์ที่ปรึกษา
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

    # รันฟังก์ชันโหลดข้อมูลแบบ Async
    page.run_task(load_data)

    # ── คืนค่า View ──
    return ft.View(
        route=f"/form1/{submission_id}",
        bgcolor=APP_COLORS["form_background"],
        scroll=ft.ScrollMode.AUTO,
        appbar=FormDetailAppBar(page, user_role),   # AppBar พร้อมปุ่มกลับ
        controls=[
            ft.Column(
                controls=[
                    # หัวข้อฟอร์ม (กลางหน้าจอ)
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
