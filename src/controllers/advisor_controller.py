# src/controllers/advisor_controller.py
import logging
from services.advisor_service import AdvisorService
from models.document_model import AdvisorDashboardModel, StudentSummaryModel, ActivityModel

logger = logging.getLogger(__name__)


class AdvisorController:
    def __init__(self):
        self.service = AdvisorService()

    async def get_dashboard_data(self, user_id):
        data, error = await self.service.fetch_dashboard_data(user_id)

        if error:
            return {"success": False, "message": error, "data": None}

        students = [
            StudentSummaryModel(name=s.get("name", "N/A"), doc_status=s.get("doc_status", "-"))
            for s in data.get("students", [])
        ]

        activities = [
            ActivityModel(
                title=a.get("doc_name", "N/A"),
                status=a.get("status", "-"),
                name=a.get("name", ""),
                form_type=a.get("form_type", "form1"),
                submission_id=a.get("submission_id", ""),
            )
            for a in data.get("activities", [])
        ]

        model = AdvisorDashboardModel(
            student_count=data.get("student_count", 0),
            students=students,
            activities=activities,
        )

        return {"success": True, "data": model}

    async def get_profile_data(self, user_id, session_name, session_role):
        from models.advisor_profile_model import AdvisorProfileModel

        data, error = await self.service.fetch_profile_data(user_id)
        if error:
            return {"success": False, "message": error}

        advisor_data = data.get("advisor", {})

        # 🔒 ตรวจสอบความปลอดภัย: ข้อมูลต้องเป็น ID ของคนนั้นจริงๆ
        returned_id = advisor_data.get("id")
        if returned_id and str(returned_id) != str(user_id):
            logger.warning(
                f"[Security] ข้อมูล API ไม่ตรงกับ User ปัจจุบัน (ขอ {user_id} แต่ได้ {returned_id})"
            )
            return {"success": False, "message": "ข้อมูลไม่ตรงกับผู้ใช้งานปัจจุบัน"}

        profile_model = AdvisorProfileModel(
            user_id=str(user_id) if user_id else "-",
            full_name=advisor_data.get("name", session_name or "-"),
            role=advisor_data.get("role", session_role or "อาจารย์ที่ปรึกษา"),
            email=advisor_data.get("email", "-"),
            phone=advisor_data.get("phone", "-"),
            academic_position=advisor_data.get("academic_position", "-"),
            advisor_type=advisor_data.get("advisor_type", "-"),
            workplace=advisor_data.get("workplace", "-"),
            approval_role=advisor_data.get("approval_role", "-"),
            program=advisor_data.get("program", "-"),
        )

        return {"success": True, "data": profile_model}
