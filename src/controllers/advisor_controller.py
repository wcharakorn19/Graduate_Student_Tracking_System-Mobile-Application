# ==============================================================================
# src/controllers/advisor_controller.py — Controller สำหรับจัดการข้อมูลอาจารย์
# ==============================================================================
# ไฟล์นี้ทำหน้าที่เป็น "สะพาน" ระหว่างหน้าจอกับ AdvisorService
# หน้าที่หลัก:
#   1. get_dashboard_data() → ดึงข้อมูล Dashboard อาจารย์ (รายชื่อนักศึกษา + กิจกรรม)
#   2. get_profile_data()   → ดึงข้อมูลโปรไฟล์อาจารย์
#
# โครงสร้างคล้าย StudentController แต่ใช้ AdvisorService และ AdvisorProfileModel
# ==============================================================================
import logging
from services.advisor_service import AdvisorService
from models.document_model import AdvisorDashboardModel, StudentSummaryModel, ActivityModel

logger = logging.getLogger(__name__)


class AdvisorController:
    """Controller สำหรับจัดการข้อมูลอาจารย์ที่ปรึกษาทั้ง Dashboard และ Profile"""

    def __init__(self):
        # สร้าง instance ของ AdvisorService เพื่อใช้เรียก API
        self.service = AdvisorService()

    async def get_dashboard_data(self, user_id):
        """
        ดึงข้อมูล Dashboard ของอาจารย์ แล้วแปลงเป็น AdvisorDashboardModel

        ขั้นตอน:
        1. เรียก Service เพื่อ fetch data จาก API
        2. แปลงรายชื่อนักศึกษา → List[StudentSummaryModel]
        3. แปลงรายการกิจกรรม → List[ActivityModel]
        4. ประกอบเป็น AdvisorDashboardModel แล้วคืนค่า
        """
        # ─── ดึงข้อมูลจาก API ───
        data, error = await self.service.fetch_dashboard_data(user_id)

        if error:
            return {"success": False, "message": error, "data": None}

        # ─── แปลงรายชื่อนักศึกษาเป็น StudentSummaryModel ───
        # ใช้ List Comprehension สร้าง Model จากแต่ละรายการ
        students = [
            StudentSummaryModel(
                name=s.get("name", "N/A"),                      # ชื่อนักศึกษา
                doc_status=s.get("doc_status", "-"),             # สถานะเอกสาร
                student_id=str(s.get("student_id", "")),        # รหัสนักศึกษา
            )
            for s in data.get("students", [])
        ]

        # ─── แปลงรายการกิจกรรมเป็น ActivityModel ───
        activities = [
            ActivityModel(
                title=a.get("doc_name", "N/A"),                 # ชื่อเอกสาร
                status=a.get("status", "-"),                    # สถานะ
                name=a.get("name", ""),                         # ชื่อเจ้าของเอกสาร
                form_type=a.get("form_type", "form1"),          # ประเภทฟอร์ม
                submission_id=a.get("submission_id", ""),       # รหัสเอกสาร
            )
            for a in data.get("activities", [])
        ]

        # ─── ประกอบร่างเป็น AdvisorDashboardModel ───
        model = AdvisorDashboardModel(
            student_count=data.get("student_count", 0),     # จำนวนนักศึกษาทั้งหมด
            students=students,                               # รายชื่อนักศึกษา
            activities=activities,                           # รายการกิจกรรม
        )

        return {"success": True, "data": model}

    async def get_profile_data(self, user_id, session_name, session_role):
        """
        ดึงข้อมูลโปรไฟล์ของอาจารย์ แล้วแปลงเป็น AdvisorProfileModel

        ขั้นตอน:
        1. เรียก Service เพื่อ fetch data จาก API
        2. ตรวจสอบความปลอดภัย (ID ต้องตรงกัน)
        3. แปลง JSON → AdvisorProfileModel
        4. คืนค่า
        """
        from models.advisor_profile_model import AdvisorProfileModel

        # ─── ดึงข้อมูลจาก API ───
        data, error = await self.service.fetch_profile_data(user_id)
        if error:
            return {"success": False, "message": error}

        advisor_data = data.get("advisor", {})

        # ─── ตรวจสอบความปลอดภัย: ข้อมูลต้องเป็น ID ของอาจารย์คนนั้นจริงๆ ───
        returned_id = advisor_data.get("id")
        if returned_id and str(returned_id) != str(user_id):
            logger.warning(
                f"[Security] ข้อมูล API ไม่ตรงกับ User ปัจจุบัน (ขอ {user_id} แต่ได้ {returned_id})"
            )
            return {"success": False, "message": "ข้อมูลไม่ตรงกับผู้ใช้งานปัจจุบัน"}

        # ─── แปลง JSON เป็น AdvisorProfileModel ───
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
