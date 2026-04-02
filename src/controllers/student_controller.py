# ==============================================================================
# src/controllers/student_controller.py — Controller สำหรับจัดการข้อมูลนักศึกษา
# ==============================================================================
# ไฟล์นี้ทำหน้าที่เป็น "สะพาน" ระหว่างหน้าจอกับ StudentService
# หน้าที่หลัก:
#   1. get_dashboard_data() → ดึงข้อมูล Dashboard และแปลงเป็น Model
#   2. get_profile_data()   → ดึงข้อมูลโปรไฟล์และแปลงเป็น Model
#
# รับ Raw JSON จาก Service → แปลงสถานะเป็นภาษาไทย → สร้าง Data Model → คืนค่า
# ==============================================================================
import logging
from services.student_service import StudentService
from models.document_model import (
    StudentDashboardModel,  # โมเดล Dashboard ของนักศึกษา
    CurrentDocumentModel,   # โมเดลเอกสารปัจจุบัน (Status Card)
    ActivityModel,          # โมเดลกิจกรรมแต่ละรายการ
)

logger = logging.getLogger(__name__)


class StudentController:
    """Controller สำหรับจัดการข้อมูลนักศึกษาทั้ง Dashboard และ Profile"""

    def __init__(self):
        # สร้าง instance ของ StudentService เพื่อใช้เรียก API
        self.service = StudentService()

    async def get_dashboard_data(self, user_id, user_name_from_session):
        """
        ดึงข้อมูล Dashboard ของนักศึกษา แล้วแปลงเป็น StudentDashboardModel

        ขั้นตอน:
        1. เรียก Service เพื่อ fetch data จาก API
        2. แปลสถานะจากอังกฤษเป็นไทย (pending → รอดำเนินการ)
        3. หาเอกสารที่กำลัง "รอดำเนินการ" มาแสดงเป็น Status Card
        4. สร้าง list ของ ActivityModel จากทุกเอกสาร
        5. ประกอบทุกอย่างเป็น StudentDashboardModel แล้วคืนค่า
        """
        # ─── ขั้นตอนที่ 1: สั่ง Service ไปดึงข้อมูล JSON จาก API ───
        data, error = await self.service.fetch_home_data(user_id)

        if error:
            return {"success": False, "message": error}

        # ─── ขั้นตอนที่ 2: พจนานุกรมแปลสถานะ (อังกฤษ → ไทย) ───
        # API ส่งสถานะเป็นภาษาอังกฤษ เช่น "pending", "approved"
        # แปลเป็นภาษาไทยเพื่อแสดงผลบน UI
        status_map = {
            "pending": "รอดำเนินการ",
            "approved": "อนุมัติเรียบร้อย",
            "rejected": "ถูกปฏิเสธ แก้ไขด่วน",
        }

        # ─── ขั้นตอนที่ 3: หาเอกสารที่สถานะ "pending" มาแสดงบน Status Card ───
        documents = data.get("documents", [])
        active_doc = CurrentDocumentModel(
            doc_name="-", status_label="สถานะ :", status_text="-"
        )

        for doc in documents:
            if doc["status"] == "pending":
                # เจอเอกสารแรกที่กำลัง "รอดำเนินการ" → ใช้เอกสารนี้แสดง
                active_doc.doc_name = doc["name"]
                active_doc.status_text = status_map.get(doc["status"], doc["status"])
                break  # ใช้เอกสารแรกที่เจอเท่านั้น

        # ─── ขั้นตอนที่ 4: สร้างรายการ Activities จากเอกสารทั้งหมด ───
        # ใช้ List Comprehension สร้าง ActivityModel จากทุกเอกสาร
        activities = [
            ActivityModel(
                title=doc["name"],                                      # ชื่อเอกสาร
                status=status_map.get(doc["status"], doc["status"]),    # สถานะ (แปลแล้ว)
                form_type=doc.get("form_type", "form1"),               # ประเภทฟอร์ม
                submission_id=doc.get("submission_id", ""),             # รหัสเอกสาร
            )
            for doc in documents
        ]

        # ─── ขั้นตอนที่ 5: ประกอบร่างเป็น Data Model แล้วส่งกลับ ───
        model = StudentDashboardModel(
            user_name=user_name_from_session,    # ชื่อจาก Session
            current_doc=active_doc,              # เอกสารที่กำลังดำเนินการ
            activities=activities,               # รายการกิจกรรมทั้งหมด
        )

        return {"success": True, "data": model}

    async def get_profile_data(self, user_id, session_name, session_role):
        """
        ดึงข้อมูลโปรไฟล์ของนักศึกษา แล้วแปลงเป็น ProfileModel

        ขั้นตอน:
        1. เรียก Service เพื่อ fetch data จาก API
        2. ตรวจสอบความปลอดภัย (ข้อมูลที่ได้ต้องตรงกับ user ปัจจุบัน)
        3. แปลง JSON → ThesisModel, ProgressModel, ProfileModel
        4. คืนค่า ProfileModel ที่พร้อมใช้แสดงผล
        """
        from models.profile_model import ProfileModel, ThesisModel, ProgressModel

        # ─── ขั้นตอนที่ 1: ดึงข้อมูลจาก API ───
        data, error = await self.service.fetch_profile_data(user_id)
        if error:
            return {"success": False, "message": error}

        student_data = data.get("student", {})

        # ─── ขั้นตอนที่ 2: ตรวจสอบความปลอดภัย ───
        # ข้อมูลที่ API ส่งกลับมาต้องเป็น ID ของ user ที่ login อยู่จริงๆ
        # ป้องกันกรณี API ส่งข้อมูลของคนอื่นมา (Security Check)
        returned_id = student_data.get("id")
        if returned_id and str(returned_id) != str(user_id):
            logger.warning(
                f"[Security] ข้อมูล API ไม่ตรงกับ User ปัจจุบัน (ขอ {user_id} แต่ได้ {returned_id})"
            )
            return {"success": False, "message": "ข้อมูลไม่ตรงกับผู้ใช้งานปัจจุบัน"}

        # ─── ขั้นตอนที่ 3: แปลง JSON เป็น Data Models ───

        # จับคู่ข้อมูลวิทยานิพนธ์ → ThesisModel
        thesis_raw = student_data.get("thesis", {})
        thesis_model = ThesisModel(
            title_th=thesis_raw.get("title_th", "-"),
            title_en=thesis_raw.get("title_en", "-"),
            main_advisor=thesis_raw.get("main_advisor", "-"),
            co_advisor_1=thesis_raw.get("co_advisor_1", "-"),
            co_advisor_2=thesis_raw.get("co_advisor_2", "-"),
        )

        # จับคู่ข้อมูลความคืบหน้า → ProgressModel
        progress_raw = student_data.get("progress", {})
        progress_model = ProgressModel(
            topic_exam_date=progress_raw.get("topic_exam_date", "-"),
            topic_status=progress_raw.get("topic_status", "-"),
            topic_approve_date=progress_raw.get("topic_approve_date", "-"),
            final_exam_date=progress_raw.get("final_exam_date", "-"),
            final_status=progress_raw.get("final_status", "-"),
            final_approve_date=progress_raw.get("final_approve_date", "-"),
            english_test_type=progress_raw.get("english_test_type", "-"),
            english_test_date=progress_raw.get("english_test_date", "-"),
            english_test_status=progress_raw.get("english_test_status", "-"),
        )

        # ─── ขั้นตอนที่ 4: ประกอบร่างเป็น ProfileModel ───
        profile_model = ProfileModel(
            user_id=str(user_id) if user_id else "-",
            full_name=student_data.get("name", session_name or "-"),
            role=student_data.get("role", session_role or "นักศึกษา"),
            email=student_data.get("email", "-"),
            phone=student_data.get("phone", "-"),
            education_level=student_data.get("education_level", "-"),
            faculty=student_data.get("faculty", "-"),
            major=student_data.get("program", "-"),
            status=student_data.get("status", "-"),
            thesis=thesis_model,
            progress=progress_model,
        )

        return {"success": True, "data": profile_model}
