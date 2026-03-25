# src/services/advisor_service.py
from services.base_service import BaseService, MOCK_QUERY_HEADERS


class AdvisorService(BaseService):
    async def fetch_dashboard_data(self, advisor_id):
        url = f"{self.base_url}/advisor/home?advisor_id={advisor_id}"
        return await self._get(url, headers=MOCK_QUERY_HEADERS)

    async def fetch_profile_data(self, advisor_id):
        url = f"{self.base_url}/advisor/profile?advisor_id={advisor_id}"
        return await self._get(url, headers=MOCK_QUERY_HEADERS)
