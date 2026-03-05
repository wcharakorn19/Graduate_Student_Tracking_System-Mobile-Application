# src/controllers/advisor_controller.py
from services.advisor_service import AdvisorService
import flet as ft

class AdvisorController:
    def __init__(self):
        self.service = AdvisorService()

    # 🌟 1. ฟังก์ชันดึงข้อมูลดิบ (Data Logic)
    def get_dashboard_data(self, user_id, user_name):
        data, error = self.service.fetch_dashboard_data(user_id)
        if error:
            return {"success": False, "message": error}
        
        # ตรวจสอบว่าใน JSON ของสุรชัยมีโครงสร้าง advisor -> email หรือยัง
        advisor_info = data.get("advisor", {})

        # ใน advisor_controller.py
        return {
            "success": True,
            "data": {
                "pending_text": f"{data.get('pending_count', 0)} รายการ", # ต้องได้ 2
                "student_text": f"{data.get('student_count', 0)} คน",      # ต้องได้ 5
                "email_text": data.get("advisor", {}).get("email", "-")
            }
        }

    # 🌟 2. ฟังก์ชันจัดรูปแบบหน้าจอ (UI Logic)
    def get_dashboard_view_model(self, user_id, user_name):
        # เรียกใช้ฟังก์ชันด้านบน
        result = self.get_dashboard_data(user_id, user_name)
        if not result["success"]:
            return result

        data = result["data"]
        # สร้าง ViewModel ให้ UI เอาไปวน Loop ใช้ง่ายๆ
        view_model = [
            {"title": "รายการรอคำอนุมัติ", "subtitle": data["pending_text"], "icon": ft.Icons.ACCESS_TIME, "route": "/approvals"},
            {"title": "นักศึกษาในที่ปรึกษา", "subtitle": data["student_text"], "icon": ft.Icons.PEOPLE, "route": "/advisees"},
            {"title": "โปรไฟล์อาจารย์", "subtitle": data["email_text"], "icon": ft.Icons.PERSON, "route": "/profile"}
        ]
        return {"success": True, "view_model": view_model}