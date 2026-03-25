# src/screens/auth/login_screen.py
import logging
import flet as ft
from components.buttons import PrimaryButton
from components.inputs import AppTextField
from controllers.auth_controller import AuthController

logger = logging.getLogger(__name__)


def LoginScreen(page: ft.Page):
    logger.info("LoginScreen loaded")

    controller = AuthController()

    siet_logo = ft.Image(
        src="siet_logo.jpeg", width=150, height=150, fit=ft.ImageFit.FIT_WIDTH
    )

    # กลุ่มข้อความยืนยันตัวตน
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

    # ฟิลด์สำหรับกรอกอีเมลและรหัสผ่าน
    email_field = AppTextField(label="E-mail Account")
    password_field = AppTextField(label="Password", is_password=True)

    # --- ฟังก์ชันตรวจสอบข้อมูลและล็อกอิน (Async) ---
    async def do_login(e):
        email = email_field.value.strip() if email_field.value else ""
        password = password_field.value.strip() if password_field.value else ""

        # 1. คลีน Error เก่าทิ้งก่อนทุกครั้งที่กดปุ่ม
        email_field.error_text = None
        password_field.error_text = None
        has_error = False

        # 2. เช็คช่องว่าง (Validation)
        if not email:
            email_field.error_text = "โปรดกรอกอีเมล"
            has_error = True
        if not password:
            password_field.error_text = "โปรดกรอกรหัสผ่าน"
            has_error = True

        if has_error:
            page.update()
            return

        # 3. โชว์วงแหวนโหลดระหว่างรอ API
        login_btn_actual.content = ft.ProgressRing(width=20, height=20, color="#FFF6FE")
        login_btn_actual.disabled = True
        page.update()

        try:
            # 🌟 เรียก Controller แบบ Async — UI จะไม่ค้างแล้ว!
            result = await controller.process_login(email, password)
        except Exception as ex:
            logger.error(f"Login exception: {ex}")
            result = {"success": False, "message": "เกิดข้อผิดพลาดที่ไม่คาดคิด"}
        finally:
            # 4. คืนค่าปุ่มกลับมาเป็นตัวหนังสือ (ทำงานเสมอแม้เกิด error)
            login_btn_actual.content = None
            login_btn_actual.disabled = False

        # 5. ประมวลผลลัพธ์จาก Controller
        if result["success"]:
            for key, value in result["session_data"].items():
                page.session.set(key, value)
            page.go(result["route"])
        else:
            # 🌟 แสดง error message จาก controller ตรงๆ แทนข้อความตายตัว
            email_field.error_text = result["message"]

        page.update()

    # --- ปุ่มล็อกอิน ---
    login_btn_actual = PrimaryButton(
        text="LOG IN",
        weight=ft.FontWeight.BOLD,
        on_click=do_login,
        padding=ft.padding.symmetric(horizontal=40, vertical=30),
    )

    login_btn_container = ft.Container(content=login_btn_actual)

    # จัดกลุ่มฟิลด์และปุ่มล็อกอิน
    field_group = ft.Container(
        content=ft.Column(
            controls=[email_field, password_field, login_btn_container],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        margin=ft.margin.only(top=50),
    )

    # กล่องล็อกอิน (กล่องเทา)
    login_box = ft.Container(
        content=ft.Column(controls=[txt_group, field_group]),
        bgcolor="#E0E0E0",
        border_radius=20,
        padding=ft.padding.only(left=30, right=30, top=30, bottom=30),
    )

    # กล่องสีแดง (กล่องนอกสุด)
    red_box = ft.Container(
        content=login_box,
        bgcolor="#EF3961",
        margin=ft.margin.only(top=50),
        padding=ft.padding.only(left=25, right=25, top=50, bottom=50),
    )

    return ft.View(
        route="/login",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.END,
        bgcolor="#FFFFFF",
        padding=0,
        appbar=ft.AppBar(
            title=ft.Text("KMITL"),
            center_title=True,
            color="#FFF6FE",
            bgcolor="#EF3961",
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color="white",
                on_click=lambda _: page.go("/"),
            ),
        ),
        controls=[siet_logo, red_box],
    )
