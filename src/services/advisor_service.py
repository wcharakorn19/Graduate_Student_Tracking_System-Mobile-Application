import requests

class AdvisorService:
    def __init__(self):
        # ใช้ Base URL ตัวเดิมของนาย
        self.base_url = "https://0e73cfd5-6b5f-4082-9c37-514cf7941cc1.mock.pstmn.io"

    def fetch_dashboard_data(self, advisor_id):
        try:
            # 🌟 พ่วง ?advisor_id ไปเพื่อให้ Postman เลือก Example ถูกคน
            url = f"{self.base_url}/advisor/home?advisor_id={advisor_id}"
            print(f"DEBUG: Requesting URL -> {url}")

            headers = {
                "x-mock-match-request-query_params": "true"
            }
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                return response.json(), None
            return None, f"Error: {response.status_code}"
        except Exception as e:
            return None, str(e)