# ==============================================================================
# src/services/auth_service.py — Service สำหรับจัดการการยืนยันตัวตน (Authentication)
# ==============================================================================
# ไฟล์นี้ทำหน้าที่ส่ง HTTP Request ไปยัง API endpoint /login
# เพื่อตรวจสอบอีเมลและรหัสผ่านของผู้ใช้
#
# สืบทอดจาก BaseService เพื่อใช้ method _post() ที่จัดการ HTTP และ Error ให้
# ==============================================================================
from services.base_service import BaseService, MOCK_BODY_HEADERS


class AuthService(BaseService):
    """Service สำหรับจัดการ Authentication (Login/Logout)"""

    async def login_api(self, email, password):
        """
        ส่ง POST Request ไปยัง /login เพื่อยืนยันตัวตน
        - ส่ง email และ password เป็น JSON Body
        - ใช้ MOCK_BODY_HEADERS เพื่อให้ Postman Mock Server จับคู่ Body ได้
        - คืนค่า (data, None) ถ้า Login สำเร็จ
        - คืนค่า (None, error_message) ถ้าล้มเหลว
        """
        url = f"{self.base_url}/login"
        data, error = await self._post(
            url,
            json_data={"email": email, "password": password},
            headers=MOCK_BODY_HEADERS,      # บอก Mock Server ให้ match ด้วย body
        )

        if error:
            # แยกประเภท Error: ถ้าเป็นเรื่องเชื่อมต่อ → บอกว่า server มีปัญหา
            # ถ้าไม่ใช่ → น่าจะเป็นเรื่อง email/password ผิด
            return None, "เซิร์ฟเวอร์มีปัญหา" if "เชื่อมต่อ" in error else "อีเมลหรือรหัสผ่านไม่ถูกต้อง"

        return data, None