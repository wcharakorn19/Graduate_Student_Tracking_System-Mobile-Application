# src/screens/auth/login_screen.py
import flet as ft
from components.buttons import PrimaryButton     # 🧱 หยิบปุ่มของนายมาใช้
from components.inputs import AppTextField       # 🧱 หยิบช่องกรอกของนายมาใช้
from controllers.auth_controller import AuthController # 🧠 หยิบสมองมาใช้

def LoginScreen(page: ft.Page):
    print("[INFO] LoginScreen")
    
    # 🌟 เรียกใช้ Controller (สมอง)
    controller = AuthController()

    siet_logo = ft.Image(src="siet_logo.jpeg", width=150, height=150, fit=ft.ImageFit.FIT_WIDTH)
    
    # กลุ่มข้อความยืนยันตัวตน
    txt_group = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("ยืนยันตัวตนด้วยบริการของสถาบันฯ", size=16, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Text("โดยใช้ E-mail Account ของสถาบันฯ", color="#000000"),
            ]
        )
    )

    # ฟิลด์สำหรับกรอกอีเมลและรหัสผ่าน
    email_field = AppTextField(label="E-mail Account")
    password_field = AppTextField(label="Password", is_password=True)
    
    # --- 2. ฟังก์ชันตรวจสอบข้อมูลและล็อกอิน (UI Logic) ---
    def do_login(e):
        email = email_field.value.strip() if email_field.value else ""
        password = password_field.value.strip() if password_field.value else ""
        
        # 1. คลีน Error เก่าทิ้งก่อนทุกครั้งที่กดปุ่ม
        email_field.error_text = None
        password_field.error_text = None
        has_error = False

        # 2. เช็คช่องว่าง (Validation) แจ้งเตือนด้วยข้อความใหม่
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

        # 🧠 โยนให้ Controller คิดและยิง API
        result = controller.process_login(email, password)

        # 4. คืนค่าปุ่มกลับมาเป็นตัวหนังสือ
        login_btn_actual.content = None
        login_btn_actual.disabled = False

        # 5. ประมวลผลลัพธ์จาก Controller
        if result["success"]:
            # สำเร็จ: เก็บ Session และเปลี่ยนหน้า
            for key, value in result["session_data"].items():
                page.session.set(key, value)
            page.go(result["route"])
        else:
            # 🌟 ล้มเหลว: แจ้งเตือนด้วย error_text ตามที่ออกแบบใหม่ (เอา SnackBar ออก)
            email_field.error_text = "อีเมลไม่ถูกต้อง"
            password_field.error_text = "รหัสผ่านไม่ถูกต้อง"

        # สั่งอัปเดตหน้าจอเพื่อโชว์ Error หรือเปลี่ยนปุ่มกลับ
        page.update()

    # --- 3. ปุ่มล็อกอินและจัด Layout (กล่องซ้อนกล่องของนาย) ---
    login_btn_actual = PrimaryButton(
        text="LOG IN",
        weight=ft.FontWeight.BOLD,
        on_click=do_login,
        padding=ft.padding.symmetric(horizontal=40, vertical=30)
    )
    
    login_btn_container = ft.Container(content=login_btn_actual)
            
    # จัดกลุ่มฟิลด์และปุ่มล็อกอิน
    field_group = ft.Container(
        content=ft.Column(
            controls=[email_field, password_field, login_btn_container],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        margin=ft.margin.only(top=50)
    )
   
    # กล่องล็อกอิน (กล่องเทา)
    login_box = ft.Container(
        content=ft.Column(
            controls=[txt_group, field_group]
        ),
        bgcolor="#E0E0E0",
        border_radius=20,
        padding=ft.padding.only(left=30, right=30, top=30, bottom=30)
    )
    
    # กล่องสีแดง (กล่องนอกสุด)
    red_box = ft.Container(
        content=login_box,
        bgcolor="#EF3961",
        margin=ft.margin.only(top=50),
        padding=ft.padding.only(left=25, right=25, top=50, bottom=50)
    )

    # ส่งออกหน้าจอ Login
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
            bgcolor="#EF3961"
        ),
        controls=[siet_logo, red_box]
    )