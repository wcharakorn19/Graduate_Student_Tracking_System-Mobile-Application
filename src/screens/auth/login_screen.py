# ==============================================================================
# src/screens/auth/login_screen.py — หน้าจอเข้าสู่ระบบ (Login Screen)
# ==============================================================================
# หน้าจอสำหรับให้ผู้ใช้กรอกอีเมลและรหัสผ่านเพื่อ Login
# การทำงาน:
#   1. แสดงฟอร์ม Login (อีเมล + รหัสผ่าน + ปุ่ม LOG IN)
#   2. เมื่อกดปุ่ม → ตรวจสอบ Validation → แสดง Spinner → เรียก API
#   3. ถ้าสำเร็จ → บันทึก Session → Redirect ไปหน้าหลักตาม Role
#   4. ถ้าล้มเหลว → แสดง Error Message ใต้ช่องอีเมล
#
# Route: "/login"
# ==============================================================================
import logging
import flet as ft
from components.buttons import PrimaryButton        # ปุ่มหลัก
from components.inputs import AppTextField           # ช่องกรอกข้อมูล
from controllers.auth_controller import AuthController   # Controller ที่จัดการ Login

logger = logging.getLogger(__name__)


def LoginScreen(page: ft.Page):
    """สร้างหน้าจอ Login พร้อมระบบ Validation และ Async API Call"""

    logger.info("LoginScreen loaded")

    # สร้าง instance ของ AuthController เพื่อใช้จัดการ Login
    controller = AuthController()

    # ── ส่วนที่ 1: โลโก้ SIET ──
    siet_logo = ft.Image(
        src="siet_logo.jpeg", width=150, height=150, fit=ft.ImageFit.FIT_WIDTH
    )

    # ── ส่วนที่ 2: กลุ่มข้อความยืนยันตัวตน ──
    txt_group = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "ยืนยันตัวตนด้วยบริการของสถาบันฯ",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color="#000000",
                ),
                ft.Text("โดยใช้ E-mail Account ของสถาบันฯ", color="#000000"),
            ]
        )
    )

    # ── ส่วนที่ 3: ฟิลด์สำหรับกรอกอีเมลและรหัสผ่าน ──
    email_field = AppTextField(label="E-mail Account")
    password_field = AppTextField(label="Password", is_password=True)

    # ── ส่วนที่ 4: ฟังก์ชันตรวจสอบข้อมูลและล็อกอิน (Async) ──
    async def do_login(e):
        """
        ฟังก์ชันหลักเมื่อกดปุ่ม LOG IN
        ทำงานแบบ async เพื่อไม่ให้ UI ค้างระหว่างรอ API
        """
        # ดึงค่าจากช่องกรอกข้อมูล
        email = email_field.value.strip() if email_field.value else ""
        password = password_field.value.strip() if password_field.value else ""

        # ขั้นตอนที่ 1: ล้าง Error เก่าทิ้งก่อนทุกครั้งที่กดปุ่ม
        email_field.error_text = None
        password_field.error_text = None
        has_error = False

        # ขั้นตอนที่ 2: เช็คช่องว่าง (Validation บนหน้าจอ)
        if not email:
            email_field.error_text = "โปรดกรอกอีเมล"
            has_error = True
        if not password:
            password_field.error_text = "โปรดกรอกรหัสผ่าน"
            has_error = True

        if has_error:
            page.update()
            return      # หยุดทำงาน ไม่ยิง API

        # ขั้นตอนที่ 3: แสดงวงแหวนโหลด (Spinner) ระหว่างรอ API ตอบกลับ
        login_btn_actual.content = ft.ProgressRing(width=20, height=20, color="#FFF6FE")
        login_btn_actual.disabled = True    # ล็อคไม่ให้กดซ้ำ
        page.update()

        try:
            # เรียก Controller แบบ Async — UI จะไม่ค้างระหว่างรอ!
            result = await controller.process_login(email, password)
        except Exception as ex:
            logger.error(f"Login exception: {ex}")
            result = {"success": False, "message": "เกิดข้อผิดพลาดที่ไม่คาดคิด"}
        finally:
            # ขั้นตอนที่ 4: คืนค่าปุ่มกลับเป็นตัวหนังสือ (ทำงานเสมอแม้เกิด error)
            login_btn_actual.content = None
            login_btn_actual.disabled = False

        # ขั้นตอนที่ 5: ประมวลผลลัพธ์จาก Controller
        if result["success"]:
            # Login สำเร็จ → บันทึกข้อมูลลง Session (user_id, ชื่อ, role, email)
            for key, value in result["session_data"].items():
                page.session.set(key, value)
            # นำทางไปหน้าหลักตาม Role (student_home หรือ advisor_home)
            page.go(result["route"])
        else:
            # Login ล้มเหลว → แสดง error message จาก Controller ใต้ช่องอีเมล
            email_field.error_text = result["message"]

        page.update()

    # ── ส่วนที่ 5: สร้างปุ่ม LOG IN ──
    login_btn_actual = PrimaryButton(
        text="LOG IN",
        weight=ft.FontWeight.BOLD,
        on_click=do_login,
        padding=ft.padding.symmetric(horizontal=40, vertical=30),
    )

    login_btn_container = ft.Container(content=login_btn_actual)

    # ── ส่วนที่ 6: จัดกลุ่ม UI ──
    # จัดกลุ่มฟิลด์กรอกข้อมูล + ปุ่ม Login
    field_group = ft.Container(
        content=ft.Column(
            controls=[email_field, password_field, login_btn_container],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        margin=ft.margin.only(top=50),
    )

    # กล่องล็อกอิน (กล่องเทา — ด้านใน)
    login_box = ft.Container(
        content=ft.Column(controls=[txt_group, field_group]),
        bgcolor="#E0E0E0",
        border_radius=20,
        padding=ft.padding.only(left=30, right=30, top=30, bottom=30),
    )

    # กล่องสีแดง (กล่องนอกสุด — ล้อมรอบกล่องเทา)
    red_box = ft.Container(
        content=login_box,
        bgcolor="#EF3961",
        margin=ft.margin.only(top=50),
        padding=ft.padding.only(left=25, right=25, top=50, bottom=50),
    )

    # ── คืนค่า View ──
    return ft.View(
        route="/login",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.END,
        bgcolor="#FFFFFF",
        padding=0,
        # AppBar ด้านบน: สีชมพูแดง พร้อมชื่อ KMITL + ปุ่มย้อนกลับ
        appbar=ft.AppBar(
            title=ft.Text("KMITL"),
            center_title=True,
            color="#FFF6FE",
            bgcolor="#EF3961",
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="white",
                on_click=lambda _: page.go("/"),    # กลับไปหน้า Welcome
            ),
        ),
        controls=[siet_logo, red_box],
    )
