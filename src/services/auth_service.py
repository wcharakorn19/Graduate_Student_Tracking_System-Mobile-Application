# src/services/auth_service.py
from services.base_service import BaseService, MOCK_BODY_HEADERS


class AuthService(BaseService):
    async def login_api(self, email, password):
        url = f"{self.base_url}/login"
        data, error = await self._post(
            url,
            json_data={"email": email, "password": password},
            headers=MOCK_BODY_HEADERS,
        )

        if error:
            return None, "เซิร์ฟเวอร์มีปัญหา" if "เชื่อมต่อ" in error else "อีเมลหรือรหัสผ่านไม่ถูกต้อง"

        return data, None