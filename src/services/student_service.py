# ==============================================================================
# src/services/student_service.py — Service สำหรับดึงข้อมูลนักศึกษา
# ==============================================================================
# ไฟล์นี้ทำหน้าที่ส่ง HTTP GET Request ไปยัง API เพื่อดึงข้อมูลนักศึกษา
# มี 2 method:
#   1. fetch_home_data()    → ดึงข้อมูล Dashboard หน้าหลัก (เอกสาร + กิจกรรม)
#   2. fetch_profile_data() → ดึงข้อมูลโปรไฟล์นักศึกษา (ข้อมูลส่วนตัว + วิทยานิพนธ์)
#
# สืบทอดจาก BaseService เพื่อใช้ method _get() ร่วมกัน
# ==============================================================================
from services.base_service import BaseService, MOCK_QUERY_HEADERS


class StudentService(BaseService):
    """Service สำหรับดึงข้อมูลนักศึกษาจาก API"""

    async def fetch_home_data(self, user_id):
        """
        ดึงข้อมูลหน้าหลักของนักศึกษา
        - Endpoint: /student/home?user_id={user_id}
        - ใช้ MOCK_QUERY_HEADERS เพื่อให้ Mock Server จับคู่ query parameter
        - คืนค่า (data, None) หรือ (None, error)
        """
        url = f"{self.base_url}/student/home?user_id={user_id}"
        return await self._get(url, headers=MOCK_QUERY_HEADERS)

    async def fetch_profile_data(self, user_id):
        """
        ดึงข้อมูลโปรไฟล์ของนักศึกษา
        - Endpoint: /student/profile?user_id={user_id}
        - ใช้ MOCK_QUERY_HEADERS เพื่อให้ Mock Server จับคู่ query parameter
        - คืนค่า (data, None) หรือ (None, error)
        """
        url = f"{self.base_url}/student/profile?user_id={user_id}"
        return await self._get(url, headers=MOCK_QUERY_HEADERS)
