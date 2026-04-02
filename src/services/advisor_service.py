# ==============================================================================
# src/services/advisor_service.py — Service สำหรับดึงข้อมูลอาจารย์ที่ปรึกษา
# ==============================================================================
# ไฟล์นี้ทำหน้าที่ส่ง HTTP GET Request ไปยัง API เพื่อดึงข้อมูลอาจารย์
# มี 2 method:
#   1. fetch_dashboard_data() → ดึงข้อมูล Dashboard (รายชื่อนักศึกษา + กิจกรรม)
#   2. fetch_profile_data()   → ดึงข้อมูลโปรไฟล์อาจารย์
#
# สืบทอดจาก BaseService เพื่อใช้ method _get() ร่วมกัน
# ==============================================================================
from services.base_service import BaseService, MOCK_QUERY_HEADERS


class AdvisorService(BaseService):
    """Service สำหรับดึงข้อมูลอาจารย์ที่ปรึกษาจาก API"""

    async def fetch_dashboard_data(self, advisor_id):
        """
        ดึงข้อมูลหน้าหลักของอาจารย์ที่ปรึกษา
        - Endpoint: /advisor/home?advisor_id={advisor_id}
        - คืนค่า (data, None) หรือ (None, error)
        """
        url = f"{self.base_url}/advisor/home?advisor_id={advisor_id}"
        return await self._get(url, headers=MOCK_QUERY_HEADERS)

    async def fetch_profile_data(self, advisor_id):
        """
        ดึงข้อมูลโปรไฟล์ของอาจารย์ที่ปรึกษา
        - Endpoint: /advisor/profile?advisor_id={advisor_id}
        - คืนค่า (data, None) หรือ (None, error)
        """
        url = f"{self.base_url}/advisor/profile?advisor_id={advisor_id}"
        return await self._get(url, headers=MOCK_QUERY_HEADERS)
