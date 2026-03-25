# src/services/base_service.py
import logging
import httpx
from core.config import API_BASE_URL

logger = logging.getLogger(__name__)

# Header สำหรับ Postman Mock Server ให้จับคู่ Query Params
MOCK_QUERY_HEADERS = {"x-mock-match-request-query_params": "true"}
MOCK_BODY_HEADERS = {"x-mock-match-request-body": "true"}


class BaseService:
    def __init__(self):
        self.base_url = API_BASE_URL

    async def _get(self, url, headers=None):
        """ยิง GET Request แบบ Async — คืนค่า (data, None) หรือ (None, error)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    return response.json(), None
                return None, f"ไม่สามารถดึงข้อมูลได้ (Error: {response.status_code})"

        except Exception as e:
            logger.error(f"GET {url}: {e}")
            return None, f"เชื่อมต่อเซิร์ฟเวอร์ไม่ได้: {str(e)}"

    async def _post(self, url, json_data=None, headers=None):
        """ยิง POST Request แบบ Async — คืนค่า (data, None) หรือ (None, error)"""
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
