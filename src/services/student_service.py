# src/services/student_service.py
from services.base_service import BaseService, MOCK_QUERY_HEADERS


class StudentService(BaseService):
    async def fetch_home_data(self, user_id):
        url = f"{self.base_url}/student/home?user_id={user_id}"
        return await self._get(url, headers=MOCK_QUERY_HEADERS)

    async def fetch_profile_data(self, user_id):
        url = f"{self.base_url}/student/profile?user_id={user_id}"
        return await self._get(url, headers=MOCK_QUERY_HEADERS)
