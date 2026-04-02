# ==============================================================================
# src/services/base_service.py — Service ฐาน (Base Service)
# ==============================================================================
# ไฟล์นี้คือ "แม่แบบ" ของทุก Service ในระบบ
# ทำหน้าที่จัดการการสื่อสารกับ API Server ผ่าน HTTP Request
#
# การทำงาน:
#   - ใช้ httpx library สำหรับส่ง HTTP Request แบบ Async (ไม่บล็อก UI)
#   - มี method _get() และ _post() ที่ Service ลูกๆ สามารถเรียกใช้ได้
#   - จัดการ Error อัตโนมัติ: ถ้า API ตอบ Error หรือเชื่อมต่อไม่ได้
#     จะคืนค่าเป็น tuple (None, error_message)
#   - ถ้าสำเร็จ จะคืนค่าเป็น tuple (data, None)
#
# Pattern: Template Method — ให้ Service ลูกกำหนดเฉพาะ URL + Logic
#          ส่วน Base จัดการเรื่องการเชื่อมต่อ, Error, Timeout ให้
# ==============================================================================
import logging
import httpx                            # Library HTTP Client แบบ Async
from core.config import API_BASE_URL    # URL ของ API Server จาก config กลาง

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# HTTP Headers สำหรับ Postman Mock Server
# ใช้เพื่อบอก Mock Server ว่าต้องจับคู่ Request ด้วยอะไร
# - MOCK_QUERY_HEADERS: จับคู่ด้วย Query Parameters (เช่น ?user_id=1)
# - MOCK_BODY_HEADERS:  จับคู่ด้วย Request Body (เช่น JSON ที่ส่งใน POST)
# ──────────────────────────────────────────────
MOCK_QUERY_HEADERS = {"x-mock-match-request-query_params": "true"}
MOCK_BODY_HEADERS = {"x-mock-match-request-body": "true"}


class BaseService:
    """
    คลาส Service ฐาน — ทุก Service (AuthService, StudentService, etc.)
    สืบทอดจากคลาสนี้ เพื่อใช้ method _get() และ _post() ร่วมกัน
    """
    def __init__(self):
        # เก็บ Base URL ไว้ให้ Service ลูกเอาไปต่อ endpoint
        self.base_url = API_BASE_URL

    async def _get(self, url, headers=None):
        """
        ยิง HTTP GET Request แบบ Async
        - คืนค่า (data, None)  ถ้าสำเร็จ (status 200)
        - คืนค่า (None, error) ถ้าล้มเหลว
        - timeout 10 วินาที เพื่อไม่ให้รอนานเกินไป
        """
        try:
            # สร้าง AsyncClient แบบ context manager (ปิดอัตโนมัติหลังใช้งาน)
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    # สำเร็จ: แปลง JSON Response → Python Dict แล้วคืนค่า
                    return response.json(), None
                # ไม่สำเร็จ: คืน error message พร้อม status code
                return None, f"ไม่สามารถดึงข้อมูลได้ (Error: {response.status_code})"

        except Exception as e:
            # เกิด Exception (เช่น timeout, connection refused, DNS error)
            logger.error(f"GET {url}: {e}")
            return None, f"เชื่อมต่อเซิร์ฟเวอร์ไม่ได้: {str(e)}"

    async def _post(self, url, json_data=None, headers=None):
        """
        ยิง HTTP POST Request แบบ Async
        - ใช้สำหรับส่งข้อมูลไปยัง API (เช่น Login)
        - คืนค่า (data, None)  ถ้าสำเร็จ (status 200)
        - คืนค่า (None, error) ถ้าล้มเหลว
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=json_data, headers=headers, timeout=10.0
                )
                if response.status_code == 200:
                    return response.json(), None
                return None, f"ไม่สามารถดำเนินการได้ (Error: {response.status_code})"

        except Exception as e:
            logger.error(f"POST {url}: {e}")
            return None, f"เชื่อมต่อเซิร์ฟเวอร์ไม่ได้: {str(e)}"
