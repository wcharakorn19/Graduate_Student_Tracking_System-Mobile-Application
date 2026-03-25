# src/services/form_service.py
from services.base_service import BaseService


class FormService(BaseService):
    async def fetch_submission_detail(self, submission_id: str):
        url = f"{self.base_url}/submissions/{submission_id}"
        return await self._get(url)
