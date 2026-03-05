# src/services/student_service.py
import requests

class StudentService:
    def __init__(self):
        # URL ของ Postman Mock Server
        self.base_url = "https://0e73cfd5-6b5f-4082-9c37-514cf7941cc1.mock.pstmn.io"

    def fetch_home_data(self, user_id):
        try:
            # 🌟 จุดสำคัญ: พ่วง ?user_id ไปที่ URL เพื่อให้ Postman เลือก Example ที่ถูกต้อง
            url = f"{self.base_url}/student/home?user_id={user_id}"
            
            # 🚀 ยิง GET Request ไปหา Server
            response = requests.get(
                url, 
                timeout=10
            )

            # ตรวจสอบ Response Status
            if response.status_code == 200:
                data = response.json()
                print(f"[SUCCESS] ดึงข้อมูลหน้า Home สำเร็จ สำหรับ ID: {user_id}")
                return data, None
            else:
                return None, f"ไม่สามารถดึงข้อมูลได้ (Error: {response.status_code})"

        except Exception as e:
            print(f"[ERROR] StudentService: {e}")
            return None, f"เชื่อมต่อเซิร์ฟเวอร์ไม่ได้: {str(e)}"

