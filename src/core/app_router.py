# ==============================================================================
# src/core/app_router.py — ระบบจัดการเส้นทาง (Router / Navigation)
# ==============================================================================
# ไฟล์นี้ทำหน้าที่เป็น "ศูนย์กลางการนำทาง" ของแอป
# เมื่อผู้ใช้กดปุ่มหรือเปลี่ยนหน้า URL จะเปลี่ยน และ Router จะตรวจสอบว่า
# URL นั้นตรงกับหน้าจอ (Screen) ไหน แล้วโหลดหน้าจอนั้นมาแสดง
#
# โครงสร้างเส้นทาง (Routes):
#   /                    → หน้า Welcome (หน้าต้อนรับ)
#   /login               → หน้า Login
#   /student_home        → หน้าหลักนักศึกษา
#   /profile             → หน้าโปรไฟล์ (ใช้ร่วมทั้ง Student และ Advisor)
#   /advisor_home        → หน้าหลักอาจารย์ที่ปรึกษา
#   /advisor_activities  → หน้ารายการกิจกรรมของอาจารย์
#   /contact_staff       → หน้าติดต่อเจ้าหน้าที่
#   /student_profile/:id → หน้าดูโปรไฟล์นักศึกษา (สำหรับอาจารย์เข้าดู)
#   /form1/:id ~ /form6/:id → หน้ารายละเอียดแบบฟอร์ม 1-6
#   /exam_result/:id     → หน้ารายละเอียดผลสอบ
# ==============================================================================
import logging
import flet as ft

# ── Import หน้าจอทั้งหมดที่ Router จะนำทางไปหา ──
from screens.auth.welcome_screen import WelcomeScreen       # หน้า Welcome
from screens.auth.login_screen import LoginScreen           # หน้า Login
from screens.student.student_home import StudentHome        # หน้าหลักนักศึกษา
from screens.advisor.advisor_home import AdvisorHome        # หน้าหลักอาจารย์
from screens.advisor.advisor_activities import AdvisorActivities  # กิจกรรมอาจารย์
from screens.advisor.contact_staff import ContactStaffScreen     # ติดต่อเจ้าหน้าที่
from screens.advisor.student_profile_view import StudentProfileViewScreen  # ดูโปรไฟล์นักศึกษา
from screens.profile_screen import ProfileScreen            # หน้าโปรไฟล์

# ── Import หน้าจอแบบฟอร์มทั้ง 7 แบบ ──
from screens.forms.form1_detail import FormOneDetailScreen      # ฟอร์ม 1: ขอรับรองอาจารย์ที่ปรึกษา
from screens.forms.form2_detail import FormTwoDetailScreen      # ฟอร์ม 2: เสนอหัวข้อวิทยานิพนธ์
from screens.forms.form3_detail import FormThreeDetailScreen    # ฟอร์ม 3: เค้าโครงวิทยานิพนธ์
from screens.forms.form4_detail import FormFourDetailScreen     # ฟอร์ม 4: ขอเชิญผู้ทรงคุณวุฒิ
from screens.forms.form5_detail import FormFiveDetailScreen     # ฟอร์ม 5: ขอเก็บรวบรวมข้อมูล
from screens.forms.form6_detail import FormSixDetailScreen      # ฟอร์ม 6: แต่งตั้งกรรมการสอบ
from screens.forms.exam_result_detail import ExamResultDetailScreen  # ผลสอบ

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Route Mapping สำหรับ Form Detail Screens
# ใช้ Dictionary จับคู่ URL prefix กับ Screen function
# เพื่อไม่ต้องเขียน if-elif ซ้ำๆ สำหรับทุกฟอร์ม
# ──────────────────────────────────────────────
FORM_ROUTES = {
    "/form1/": FormOneDetailScreen,
    "/form2/": FormTwoDetailScreen,
    "/form3/": FormThreeDetailScreen,
    "/form4/": FormFourDetailScreen,
    "/form5/": FormFiveDetailScreen,
    "/form6/": FormSixDetailScreen,
    "/exam_result/": ExamResultDetailScreen,
}


class AppRouter:
    """
    คลาส Router หลัก — สร้างครั้งเดียวใน main.py
    ทำหน้าที่:
    1. ลงทะเบียน event handler สำหรับ route_change (URL เปลี่ยน)
    2. ลงทะเบียน event handler สำหรับ view_pop (กดปุ่มย้อนกลับ)
    """
    def __init__(self, page: ft.Page):
        self.page = page
        # ผูก event: เมื่อ URL เปลี่ยน → เรียก route_change
        self.page.on_route_change = self.route_change
        # ผูก event: เมื่อกดปุ่มย้อนกลับ → เรียก view_pop
        self.page.on_view_pop = self.view_pop

    def route_change(self, route):
        """
        ฟังก์ชันจัดการเมื่อ URL/Route เปลี่ยน
        ทำหน้าที่ตรวจสอบว่า URL ปัจจุบันตรงกับหน้าจอไหน
        แล้วสร้าง View ของหน้าจอนั้นมาแสดงผล
        """
        # ใช้ TemplateRoute เพื่อจับคู่ URL กับ pattern ที่กำหนด
        t_route = ft.TemplateRoute(self.page.route)
        logger.info(f"Router สับรางไปที่: {self.page.route}")

        # ── ตรวจสอบ Route แบบ Static (ไม่มี parameter) ──

        if t_route.match("/"):
            # หน้าแรก: Welcome Screen
            self.page.views.clear()
            self.page.views.append(WelcomeScreen(self.page))

        elif t_route.match("/login"):
            # หน้า Login
            self.page.views.clear()
            self.page.views.append(LoginScreen(self.page))

        elif t_route.match("/student_home"):
            # หน้าหลักของนักศึกษา
            self.page.views.clear()
            self.page.views.append(StudentHome(self.page))

        elif t_route.match("/profile"):
            # หน้าโปรไฟล์ (ใช้ร่วมทั้ง Student และ Advisor)
            self.page.views.clear()
            self.page.views.append(ProfileScreen(self.page))

        elif t_route.match("/advisor_home"):
            # หน้าหลักของอาจารย์ที่ปรึกษา
            self.page.views.clear()
            self.page.views.append(AdvisorHome(self.page))

        elif t_route.match("/advisor_activities"):
            # หน้ารายการกิจกรรมของอาจารย์
            self.page.views.clear()
            self.page.views.append(AdvisorActivities(self.page))

        elif t_route.match("/contact_staff"):
            # หน้าติดต่อเจ้าหน้าที่
            self.page.views.clear()
            self.page.views.append(ContactStaffScreen(self.page))

        else:
            # ── ตรวจสอบ Route แบบ Dynamic (มี parameter เป็น ID) ──

            # ตรวจสอบ student_profile route ก่อน (URL: /student_profile/{student_id})
            if self.page.route.startswith("/student_profile/"):
                # ดึง student_id จากส่วนท้ายของ URL
                student_id = self.page.route.split("/")[-1]
                self.page.views.clear()
                self.page.views.append(StudentProfileViewScreen(self.page, student_id))
            else:
                # วน loop ตรวจสอบ Form Routes ทั้งหมดจาก FORM_ROUTES dictionary
                # เช่น URL "/form1/abc123" จะ match กับ prefix "/form1/"
                matched = False
                for prefix, screen_fn in FORM_ROUTES.items():
                    if self.page.route.startswith(prefix):
                        # ดึง submission_id จากส่วนท้ายของ URL
                        submission_id = self.page.route.split("/")[-1]
                        self.page.views.clear()
                        # เรียกฟังก์ชัน Screen ที่ตรงกับ prefix พร้อมส่ง submission_id
                        self.page.views.append(screen_fn(self.page, submission_id))
                        matched = True
                        break  # เจอแล้ว ไม่ต้องเช็คต่อ

                # ถ้าไม่ match กับ route ไหนเลย → redirect กลับไปหน้า Login
                if not matched:
                    logger.warning("หา Route ไม่เจอ — redirect กลับไปหน้า Login")
                    self.page.views.clear()
                    self.page.views.append(LoginScreen(self.page))

        # อัปเดตหน้าจอหลังจากเปลี่ยน View
        self.page.update()

    def view_pop(self, view):
        """
        ฟังก์ชันจัดการเมื่อกดปุ่มย้อนกลับ (Back Button)
        ลบ View บนสุดออก แล้วกลับไปหน้าก่อนหน้า
        ถ้าไม่มี View เหลือ → กลับไปหน้าแรก (/)
        """
        self.page.views.pop()

        if len(self.page.views) > 0:
            # กลับไปยังหน้าจอก่อนหน้า (View บนสุดใน stack)
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        else:
            # ไม่มี View เหลือแล้ว → กลับหน้าแรก
            self.page.go("/")
