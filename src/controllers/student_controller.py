import logging
from services.student_service import StudentService
from models.document_model import (
    StudentDashboardModel,
    CurrentDocumentModel,
    ActivityModel,
)

logger = logging.getLogger(__name__)


class StudentController:
    def __init__(self):
        self.service = StudentService()

    async def get_dashboard_data(self, user_id, user_name_from_session):
        # 1. สั่งแมสเซนเจอร์ไปดึงข้อมูล JSON ของจริงมา
        data, error = await self.service.fetch_home_data(user_id)

        if error:
            return {"success": False, "message": error}

        # 2. เตรียมพจนานุกรมแปลสถานะ (ดึงจาก API มาแปลเป็นไทยให้ UI สวยๆ)
        status_map = {
            "pending": "รอดำเนินการ",
            "approved": "อนุมัติเรียบร้อย",
            "rejected": "ถูกปฏิเสธ แก้ไขด่วน",
        }

        # 3. หางานที่กำลัง "รอดำเนินการ" มาโชว์เป็นการ์ดหลักด้านบน (Status Card)
        documents = data.get("documents", [])
        active_doc = CurrentDocumentModel(
            doc_name="-", status_label="สถานะ :", status_text="-"
        )

        for doc in documents:
            if doc["status"] == "pending":
                active_doc.doc_name = doc["name"]
                active_doc.status_text = status_map.get(doc["status"], doc["status"])
                break

        # 4. จัดเรียงรายการ Activities ทั้งหมด
        activities = [
            ActivityModel(
                title=doc["name"],
                status=status_map.get(doc["status"], doc["status"]),
                form_type=doc.get("form_type", "form1"),
                submission_id=doc.get("submission_id", ""),
            )
            for doc in documents
        ]

        # 5. ประกอบร่างข้อมูลเป็น Data Model ส่งให้หน้าจอ
        model = StudentDashboardModel(
            user_name=user_name_from_session,
            current_doc=active_doc,
            activities=activities,
        )

        return {"success": True, "data": model}

    async def get_profile_data(self, user_id, session_name, session_role):
        from models.profile_model import ProfileModel, ThesisModel, ProgressModel

        data, error = await self.service.fetch_profile_data(user_id)
        if error:
            return {"success": False, "message": error}

        student_data = data.get("student", {})

        # 🔒 ตรวจสอบความปลอดภัย: ข้อมูลที่ได้มาต้องเป็น ID ของคนนั้นจริงๆ
        returned_id = student_data.get("id")
        if returned_id and str(returned_id) != str(user_id):
            logger.warning(
                f"[Security] ข้อมูล API ไม่ตรงกับ User ปัจจุบัน (ขอ {user_id} แต่ได้ {returned_id})"
            )
            return {"success": False, "message": "ข้อมูลไม่ตรงกับผู้ใช้งานปัจจุบัน"}

        # จับคู่ข้อมูลวิทยานิพนธ์
        thesis_raw = student_data.get("thesis", {})
        thesis_model = ThesisModel(
            title_th=thesis_raw.get("title_th", "-"),
            title_en=thesis_raw.get("title_en", "-"),
            main_advisor=thesis_raw.get("main_advisor", "-"),
            co_advisor_1=thesis_raw.get("co_advisor_1", "-"),
            co_advisor_2=thesis_raw.get("co_advisor_2", "-"),
        )

        # จับคู่ข้อมูลความคืบหน้า
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

        # ประกอบร่าง
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
