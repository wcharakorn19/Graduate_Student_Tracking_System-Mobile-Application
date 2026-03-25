# src/core/app_router.py
import logging
import flet as ft

from screens.auth.welcome_screen import WelcomeScreen
from screens.auth.login_screen import LoginScreen
from screens.student.student_home import StudentHome
from screens.advisor.advisor_home import AdvisorHome
from screens.profile_screen import ProfileScreen

from screens.forms.form1_detail import FormOneDetailScreen
from screens.forms.form2_detail import FormTwoDetailScreen
from screens.forms.form3_detail import FormThreeDetailScreen
from screens.forms.form4_detail import FormFourDetailScreen
from screens.forms.form5_detail import FormFiveDetailScreen
from screens.forms.form6_detail import FormSixDetailScreen
from screens.forms.exam_result_detail import ExamResultDetailScreen

logger = logging.getLogger(__name__)

# 🌟 Route mapping: จับคู่ URL prefix กับ Screen function
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
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

    def route_change(self, route):
        t_route = ft.TemplateRoute(self.page.route)
        logger.info(f"Router สับรางไปที่: {self.page.route}")

        if t_route.match("/"):
            self.page.views.clear()
            self.page.views.append(WelcomeScreen(self.page))

        elif t_route.match("/login"):
            self.page.views.clear()
            self.page.views.append(LoginScreen(self.page))

        elif t_route.match("/student_home"):
            self.page.views.clear()
            self.page.views.append(StudentHome(self.page))

        elif t_route.match("/profile"):
            self.page.views.clear()
            self.page.views.append(ProfileScreen(self.page))

        elif t_route.match("/advisor_home"):
            self.page.views.clear()
            self.page.views.append(AdvisorHome(self.page))

        else:
            # 🌟 วน loop เช็ค form routes ทีเดียว แทน elif ซ้ำ 7 blocks
            matched = False
            for prefix, screen_fn in FORM_ROUTES.items():
                if self.page.route.startswith(prefix):
                    submission_id = self.page.route.split("/")[-1]
                    self.page.views.clear()
                    self.page.views.append(screen_fn(self.page, submission_id))
                    matched = True
                    break

            if not matched:
                logger.warning("หา Route ไม่เจอ — redirect กลับไปหน้า Login")
                self.page.views.clear()
                self.page.views.append(LoginScreen(self.page))

        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()

        if len(self.page.views) > 0:
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        else:
            self.page.go("/")
