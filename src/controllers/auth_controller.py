# src/controllers/auth_controller.py
import logging
from services.auth_service import AuthService

logger = logging.getLogger(__name__)


class AuthController:
    def __init__(self):
        self.service = AuthService()

    async def process_login(self, email, password):
        # 1. ตรวจสอบเบื้องต้น (Validation)
        if not email or not email.strip():
            return {"success": False, "message": "กรุณากรอกอีเมล"}
        if not password or not password.strip():
            return {"success": False, "message": "กรุณากรอกรหัสผ่าน"}

        # 2. สั่ง Service ยิง API ไปหา Postman แบบ Async
        data, error = await self.service.login_api(email, password)

        if error:
            return {"success": False, "message": error}

        # 3. ดึงข้อมูลจาก JSON ที่ได้รับมา (รองรับทั้ง student, advisor, และ user)
        user_data = (
            data.get("student") or data.get("advisor") or data.get("user") or {}
        )

        user_id = user_data.get("id")
        user_name = user_data.get("name", "Unknown User")
        role = user_data.get("role", "student")

        # ตรวจสอบว่า API ส่ง user_id กลับมาจริง
        if not user_id:
            return {"success": False, "message": "ล็อกอินไม่สำเร็จ: ไม่พบรหัสผู้ใช้จากระบบ"}

        logger.debug(f"Login Success: {user_name} (ID: {user_id})")

        # 4. ส่งข้อมูลกลับ — เก็บเฉพาะสิ่งที่จำเป็นลง Session
        return {
            "success": True,
            "session_data": {
                "user_id": str(user_id),
                "user_full_name": user_name,
                "user_role": role,
                "user_email": email,
            },
            "route": "/advisor_home" if role == "advisor" else "/student_home",
        }
