import flet as ft
import os
import sys

# --- 🌟 โซน Import หน้าจอที่สร้างเสร็จแล้ว ---
from screens.auth.welcome_screen import WelcomeScreen
from screens.auth.login_screen import LoginScreen
from screens.student.student_home import StudentHome
from screens.advisor.advisor_home import AdvisorHome

# Setup App 
def main(page: ft.Page):
    page.title = "Graduate Student Tracking System"
    page.window.width = 402
    page.window.height = 874

    # Setup Navigation and Routing
    def route_change(route):
        t_route = ft.TemplateRoute(page.route)

        if t_route.match("/"):
            page.views.clear()
            page.views.append(WelcomeScreen(page))

        elif t_route.match("/login"):
            page.views.append(LoginScreen(page))

        # 🌟 วิ่งเข้าหน้านี้เมื่อล็อกอินสำเร็จ!
        elif t_route.match("/student_home"):
            page.views.append(StudentHome(page))

        # ---------------------------------------------------------
        # ⚠️ โซนหน้าจออื่นๆ (Andy คอมเมนต์ไว้ให้ก่อนชั่วคราว)
        # ถ้านายสร้างไฟล์พวกนี้เสร็จ และ Import ข้างบนแล้ว ค่อยเอาเครื่องหมาย # ออกนะ
        # ---------------------------------------------------------
        # elif t_route.match("/contact"):
        #     page.views.append(ContactScreen(page))
        # elif t_route.match("/profile"):
        #     page.views.append(ProfileScreen(page))
        elif t_route.match("/advisor_home"):
            page.views.append(AdvisorHome(page))
        # elif t_route.match("/form1/:id"):
        #     page.views.append(FormOneDetailScreen(page, t_route.id))
        # ---------------------------------------------------------
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/")

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")