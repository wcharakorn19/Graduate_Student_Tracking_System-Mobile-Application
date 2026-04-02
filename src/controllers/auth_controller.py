# ==============================================================================
# src/controllers/auth_controller.py — Controller สำหรับจัดการ Login
# ==============================================================================
# ไฟล์นี้ทำหน้าที่เป็น "สะพาน" ระหว่างหน้าจอ Login กับ AuthService
# หน้าที่หลัก:
#   1. ตรวจสอบข้อมูลที่ผู้ใช้กรอก (Validation)
#   2. สั่ง Service ยิง API ไป Login
#   3. แปลงข้อมูลที่ได้จาก API ให้พร้อมใช้ (เช่น ดึง user_id, role)
#   4. ส่งผลลัพธ์กลับให้หน้าจอ พร้อม route ที่ต้อง redirect
#
# Pattern: MVC (Model-View-Controller)
#   - Controller รับข้อมูลจาก View (Screen) → ส่งต่อให้ Model/Service
#   - แล้วส่งผลลัพธ์กลับไปให้ View แสดงผล
# ==============================================================================
import logging
from services.auth_service import AuthService

logger = logging.getLogger(__name__)


class AuthController:
    """Controller สำหรับจัดการกระบวนการ Login ทั้งหมด"""

    def __init__(self):
        # สร้าง instance ของ AuthService เพื่อใช้เรียก API
        self.service = AuthService()

    async def process_login(self, email, password):
        """
        ฟังก์ชันหลัก: ประมวลผล Login ทั้งกระบวนการ
        รับ email + password จากหน้าจอ → ตรวจสอบ → ยิง API → คืนผลลัพธ์

        Return:
            dict — มี key ได้แก่:
            - success (bool)       : Login สำเร็จหรือไม่
            - message (str)        : ข้อความ error (กรณีล้มเหลว)
            - session_data (dict)  : ข้อมูลที่ต้องเก็บลง Session (กรณีสำเร็จ)
            - route (str)          : เส้นทางที่ต้อง redirect ไป (กรณีสำเร็จ)
        """
        # ─── ขั้นตอนที่ 1: ตรวจสอบเบื้องต้น (Validation) ───
        # ตรวจว่าผู้ใช้กรอกอีเมลมาหรือยัง
        if not email or not email.strip():
            return {"success": False, "message": "กรุณากรอกอีเมล"}
        # ตรวจว่าผู้ใช้กรอกรหัสผ่านมาหรือยัง
        if not password or not password.strip():
            return {"success": False, "message": "กรุณากรอกรหัสผ่าน"}

        # ─── ขั้นตอนที่ 2: สั่ง Service ยิง API ไปหา Postman Mock Server ───
        data, error = await self.service.login_api(email, password)

        if error:
            # API ตอบ error → ส่งข้อความ error กลับไปให้หน้าจอแสดง
            return {"success": False, "message": error}

        # ─── ขั้นตอนที่ 3: ดึงข้อมูลจาก JSON Response ───
        # รองรับ 3 รูปแบบ: {"student": {...}}, {"advisor": {...}}, {"user": {...}}
        # ใช้ or เพื่อเลือก key ที่มีข้อมูล (ตัวแรกที่ไม่ใช่ None)
        user_data = (
            data.get("student") or data.get("advisor") or data.get("user") or {}
        )

        user_id = user_data.get("id")                   # รหัสผู้ใช้
        user_name = user_data.get("name", "Unknown User")  # ชื่อผู้ใช้
        role = user_data.get("role", "student")          # บทบาท (student/advisor)

        # ตรวจสอบว่า API ส่ง user_id กลับมาจริง
        if not user_id:
            return {"success": False, "message": "ล็อกอินไม่สำเร็จ: ไม่พบรหัสผู้ใช้จากระบบ"}

        logger.debug(f"Login Success: {user_name} (ID: {user_id})")

        # ─── ขั้นตอนที่ 4: ส่งข้อมูลกลับ ───
        # เก็บเฉพาะสิ่งที่จำเป็นลง Session (user_id, ชื่อ, บทบาท, อีเมล)
        # พร้อมกำหนด route ว่าจะ redirect ไปหน้าไหน ตาม role
        return {
            "success": True,
            "session_data": {
                "user_id": str(user_id),
                "user_full_name": user_name,
                "user_role": role,
                "user_email": email,
            },
            # ถ้าเป็น advisor → ไปหน้า advisor_home, ถ้าเป็น student → ไปหน้า student_home
            "route": "/advisor_home" if role == "advisor" else "/student_home",
        }
