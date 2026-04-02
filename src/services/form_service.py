# ==============================================================================
# src/services/form_service.py — Service สำหรับดึงข้อมูลแบบฟอร์ม
# ==============================================================================
# ไฟล์นี้ทำหน้าที่ส่ง HTTP GET Request ไปยัง API เพื่อดึงรายละเอียดแบบฟอร์ม
# ใช้ submission_id เป็นตัวระบุว่าจะดึงเอกสารไหน
#
# มี method เดียว: fetch_submission_detail()
# ใช้ร่วมกันทุกฟอร์ม (Form 1-6 + Exam Result) เพราะ API endpoint เดียวกัน
# ==============================================================================
from services.base_service import BaseService


class FormService(BaseService):
    """Service สำหรับดึงข้อมูลรายละเอียดของแบบฟอร์มที่ยื่นแล้ว"""

    async def fetch_submission_detail(self, submission_id: str):
        """
        ดึงรายละเอียดของเอกสารที่ยื่นแล้ว
        - Endpoint: /submissions/{submission_id}
        - ใช้ submission_id เป็น path parameter
        - คืนค่า (data, None) หรือ (None, error)
        """
        url = f"{self.base_url}/submissions/{submission_id}"
        return await self._get(url)
