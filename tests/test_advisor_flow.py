# ==============================================================================
# tests/test_advisor_flow.py — Test Cases สำหรับบทบาทอาจารย์ที่ปรึกษา
# ==============================================================================
# ทดสอบ Flow ทั้งหมดที่อาจารย์สามารถทำได้หลัง Login:
#   1. Login เข้าสู่ระบบ
#   2. ดู Dashboard หน้าหลัก (รายชื่อนักศึกษา + กิจกรรม)
#   3. ดูโปรไฟล์ส่วนตัว
#   4. ดูรายละเอียดแบบฟอร์มของนักศึกษา
# ==============================================================================
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from controllers.auth_controller import AuthController
from controllers.advisor_controller import AdvisorController
from controllers.form_controller import FormController
from core.auth_guard import require_auth
from conftest import (
    ADVISOR_LOGIN_RESPONSE,
    ADVISOR_DASHBOARD_RESPONSE,
    ADVISOR_PROFILE_RESPONSE,
    FORM1_DETAIL_RESPONSE,
    FORM2_DETAIL_RESPONSE,
    FORM3_DETAIL_RESPONSE,
    FORM4_DETAIL_RESPONSE,
    FORM5_DETAIL_RESPONSE,
    FORM6_DETAIL_RESPONSE,
    EXAM_RESULT_DETAIL_RESPONSE,
)


# ══════════════════════════════════════════════
# 1. อาจารย์ Login เข้าสู่ระบบ
# ══════════════════════════════════════════════
class TestAdvisorLogin:
    """ทดสอบการ Login ในบทบาทอาจารย์ที่ปรึกษา"""

    @pytest.fixture
    def auth_ctrl(self):
        return AuthController()

    # ── TC-A-001: Login สำเร็จ ───
    async def test_login_success(self, auth_ctrl):
        """อาจารย์ login สำเร็จ → redirect ไปหน้า advisor_home"""
        with patch.object(
            auth_ctrl.service,
            "login_api",
            new_callable=AsyncMock,
            return_value=(ADVISOR_LOGIN_RESPONSE, None),
        ):
            result = await auth_ctrl.process_login("advisor@kmitl.ac.th", "password123")

        assert result["success"] is True
        assert result["route"] == "/advisor_home"
        assert result["session_data"]["user_role"] == "advisor"
        assert result["session_data"]["user_id"] == "A001"
        assert result["session_data"]["user_full_name"] == "ผศ.ดร.สมศรี รักเรียน"

    # ── TC-A-002: ไม่กรอกอีเมล ───
    async def test_login_empty_email(self, auth_ctrl):
        """ไม่กรอกอีเมล → แสดง error กรุณากรอกอีเมล"""
        result = await auth_ctrl.process_login("", "password123")
        assert result["success"] is False
        assert "อีเมล" in result["message"]

    # ── TC-A-003: ไม่กรอกรหัสผ่าน ───
    async def test_login_empty_password(self, auth_ctrl):
        """ไม่กรอกรหัสผ่าน → แสดง error กรุณากรอกรหัสผ่าน"""
        result = await auth_ctrl.process_login("advisor@kmitl.ac.th", "")
        assert result["success"] is False
        assert "รหัสผ่าน" in result["message"]

    # ── TC-A-004: API ตอบ error ───
    async def test_login_server_error(self, auth_ctrl):
        """API ตอบ error → แสดงข้อความเซิร์ฟเวอร์มีปัญหา"""
        with patch.object(
            auth_ctrl.service,
            "login_api",
            new_callable=AsyncMock,
            return_value=(None, "เซิร์ฟเวอร์มีปัญหา"),
        ):
            result = await auth_ctrl.process_login("advisor@kmitl.ac.th", "password123")

        assert result["success"] is False

    # ── TC-A-005: อีเมลหรือรหัสผ่านผิด ───
    async def test_login_wrong_credentials(self, auth_ctrl):
        """อีเมลหรือรหัสผ่านผิด → แสดงข้อความ error"""
        with patch.object(
            auth_ctrl.service,
            "login_api",
            new_callable=AsyncMock,
            return_value=(None, "อีเมลหรือรหัสผ่านไม่ถูกต้อง"),
        ):
            result = await auth_ctrl.process_login("wrong@email.com", "wrong")

        assert result["success"] is False
        assert result["message"] == "อีเมลหรือรหัสผ่านไม่ถูกต้อง"

    # ── TC-A-006: Login ด้วย key "user" แทน "advisor" ───
    async def test_login_with_user_key(self, auth_ctrl):
        """API ส่ง response ผ่าน key 'user' แทน → ยังใช้งานได้"""
        response_with_user_key = {
            "user": {"id": "A001", "name": "ผศ.ดร.สมศรี", "role": "advisor"}
        }
        with patch.object(
            auth_ctrl.service,
            "login_api",
            new_callable=AsyncMock,
            return_value=(response_with_user_key, None),
        ):
            result = await auth_ctrl.process_login("advisor@kmitl.ac.th", "password123")

        assert result["success"] is True
        assert result["route"] == "/advisor_home"
        assert result["session_data"]["user_id"] == "A001"


# ══════════════════════════════════════════════
# 2. ตรวจสอบสิทธิ์เข้าถึง (Auth Guard)
# ══════════════════════════════════════════════
class TestAdvisorAuthGuard:
    """ทดสอบ Auth Guard สำหรับอาจารย์"""

    # ── TC-A-007: มี Session → เข้าถึงได้ ───
    def test_auth_guard_with_session(self, mock_page):
        """ถ้า login แล้ว (มี user_id ใน session) → คืน user_id"""
        mock_page.session.get.return_value = "A001"

        user_id = require_auth(mock_page)

        assert user_id == "A001"
        mock_page.go.assert_not_called()

    # ── TC-A-008: ไม่มี Session → redirect ไป login ───
    def test_auth_guard_without_session(self, mock_page):
        """ถ้ายังไม่ได้ login → redirect ไปหน้า login"""
        mock_page.session.get.return_value = None

        user_id = require_auth(mock_page)

        assert user_id is None
        mock_page.go.assert_called_once_with("/login")


# ══════════════════════════════════════════════
# 3. อาจารย์ ดู Dashboard หน้าหลัก
# ══════════════════════════════════════════════
class TestAdvisorDashboard:
    """ทดสอบการดู Dashboard ของอาจารย์ที่ปรึกษา"""

    @pytest.fixture
    def advisor_ctrl(self):
        return AdvisorController()

    # ── TC-A-009: ดู Dashboard สำเร็จ ───
    async def test_dashboard_success(self, advisor_ctrl):
        """ดึงข้อมูล Dashboard สำเร็จ → มีจำนวนนักศึกษา + รายชื่อ + กิจกรรม"""
        with patch.object(
            advisor_ctrl.service,
            "fetch_dashboard_data",
            new_callable=AsyncMock,
            return_value=(ADVISOR_DASHBOARD_RESPONSE, None),
        ):
            result = await advisor_ctrl.get_dashboard_data("A001")

        assert result["success"] is True
        model = result["data"]
        assert model.student_count == 3

    # ── TC-A-010: รายชื่อนักศึกษาครบ ───
    async def test_dashboard_student_list(self, advisor_ctrl):
        """Dashboard ต้องแสดงรายชื่อนักศึกษาทั้งหมดที่ดูแล"""
        with patch.object(
            advisor_ctrl.service,
            "fetch_dashboard_data",
            new_callable=AsyncMock,
            return_value=(ADVISOR_DASHBOARD_RESPONSE, None),
        ):
            result = await advisor_ctrl.get_dashboard_data("A001")

        students = result["data"].students
        assert len(students) == 3
        assert students[0].name == "นายสมชาย ใจดี"
        assert students[0].doc_status == "รอดำเนินการ"
        assert students[0].student_id == "S001"
        assert students[1].name == "นางสาวสมหญิง รักเรียน"
        assert students[2].name == "นายสมศักดิ์ ดีงาม"

    # ── TC-A-011: รายการกิจกรรมนักศึกษา ───
    async def test_dashboard_activities(self, advisor_ctrl):
        """Dashboard ต้องแสดงรายการกิจกรรม (เอกสารที่นักศึกษายื่น)"""
        with patch.object(
            advisor_ctrl.service,
            "fetch_dashboard_data",
            new_callable=AsyncMock,
            return_value=(ADVISOR_DASHBOARD_RESPONSE, None),
        ):
            result = await advisor_ctrl.get_dashboard_data("A001")

        activities = result["data"].activities
        assert len(activities) == 2
        assert activities[0].title == "แบบฟอร์มขอรับรองอาจารย์ที่ปรึกษา"
        assert activities[0].name == "นายสมชาย ใจดี"
        assert activities[0].status == "รอดำเนินการ"
        assert activities[0].form_type == "form1"
        assert activities[0].submission_id == "sub001"

    # ── TC-A-012: Dashboard API error ───
    async def test_dashboard_api_error(self, advisor_ctrl):
        """API error → ส่ง error message กลับ"""
        with patch.object(
            advisor_ctrl.service,
            "fetch_dashboard_data",
            new_callable=AsyncMock,
            return_value=(None, "เชื่อมต่อเซิร์ฟเวอร์ไม่ได้"),
        ):
            result = await advisor_ctrl.get_dashboard_data("A001")

        assert result["success"] is False
        assert "เชื่อมต่อ" in result["message"]

    # ── TC-A-013: ไม่มีนักศึกษาและกิจกรรม ───
    async def test_dashboard_empty_data(self, advisor_ctrl):
        """ถ้าไม่มีนักศึกษา → Dashboard แสดง list ว่าง"""
        empty_response = {"student_count": 0, "students": [], "activities": []}
        with patch.object(
            advisor_ctrl.service,
            "fetch_dashboard_data",
            new_callable=AsyncMock,
            return_value=(empty_response, None),
        ):
            result = await advisor_ctrl.get_dashboard_data("A001")

        assert result["success"] is True
        assert result["data"].student_count == 0
        assert len(result["data"].students) == 0
        assert len(result["data"].activities) == 0


# ══════════════════════════════════════════════
# 4. อาจารย์ ดูโปรไฟล์
# ══════════════════════════════════════════════
class TestAdvisorProfile:
    """ทดสอบการดูโปรไฟล์ของอาจารย์ที่ปรึกษา"""

    @pytest.fixture
    def advisor_ctrl(self):
        return AdvisorController()

    # ── TC-A-014: ดูโปรไฟล์สำเร็จ ───
    async def test_profile_success(self, advisor_ctrl):
        """ดึงข้อมูลโปรไฟล์สำเร็จ → มีข้อมูลอาจารย์ครบ"""
        with patch.object(
            advisor_ctrl.service,
            "fetch_profile_data",
            new_callable=AsyncMock,
            return_value=(ADVISOR_PROFILE_RESPONSE, None),
        ):
            result = await advisor_ctrl.get_profile_data(
                "A001", "ผศ.ดร.สมศรี รักเรียน", "advisor"
            )

        assert result["success"] is True
        profile = result["data"]
        assert profile.full_name == "ผศ.ดร.สมศรี รักเรียน"
        assert profile.email == "somsri@kmitl.ac.th"
        assert profile.phone == "0899876543"
        assert profile.academic_position == "ผู้ช่วยศาสตราจารย์"
        assert profile.advisor_type == "อาจารย์ประจำ"
        assert profile.workplace == "คณะเทคโนโลยีสารสนเทศ"
        assert profile.approval_role == "ประธานหลักสูตร"
        assert profile.program == "วิทยาการคอมพิวเตอร์"

    # ── TC-A-015: Security Check — ID ไม่ตรง ───
    async def test_profile_security_id_mismatch(self, advisor_ctrl):
        """ถ้า API ส่งข้อมูลอาจารย์คนอื่นมา → reject"""
        wrong_data = {"advisor": {"id": "A999", "name": "คนอื่น"}}
        with patch.object(
            advisor_ctrl.service,
            "fetch_profile_data",
            new_callable=AsyncMock,
            return_value=(wrong_data, None),
        ):
            result = await advisor_ctrl.get_profile_data(
                "A001", "ผศ.ดร.สมศรี รักเรียน", "advisor"
            )

        assert result["success"] is False
        assert "ไม่ตรง" in result["message"]

    # ── TC-A-016: Profile API error ───
    async def test_profile_api_error(self, advisor_ctrl):
        """API error → ส่ง error message กลับ"""
        with patch.object(
            advisor_ctrl.service,
            "fetch_profile_data",
            new_callable=AsyncMock,
            return_value=(None, "เชื่อมต่อเซิร์ฟเวอร์ไม่ได้"),
        ):
            result = await advisor_ctrl.get_profile_data(
                "A001", "ผศ.ดร.สมศรี รักเรียน", "advisor"
            )

        assert result["success"] is False

    # ── TC-A-017: โปรไฟล์ — ข้อมูลไม่ครบ (ใช้ค่า default) ───
    async def test_profile_missing_fields(self, advisor_ctrl):
        """ถ้า API ส่งข้อมูลไม่ครบ → ใช้ค่า default '-'"""
        partial_data = {"advisor": {"id": "A001", "name": "ผศ.ดร.สมศรี รักเรียน"}}
        with patch.object(
            advisor_ctrl.service,
            "fetch_profile_data",
            new_callable=AsyncMock,
            return_value=(partial_data, None),
        ):
            result = await advisor_ctrl.get_profile_data(
                "A001", "ผศ.ดร.สมศรี รักเรียน", "advisor"
            )

        assert result["success"] is True
        profile = result["data"]
        assert profile.email == "-"
        assert profile.phone == "-"
        assert profile.academic_position == "-"


# ══════════════════════════════════════════════
# 5. อาจารย์ ดูรายละเอียดฟอร์มของนักศึกษา
# ══════════════════════════════════════════════
class TestAdvisorViewFormDetails:
    """
    ทดสอบการดูรายละเอียดแบบฟอร์มในมุมอาจารย์
    (ใช้ FormController เดียวกัน แต่ทดสอบว่าอาจารย์เข้าถึงได้)
    """

    @pytest.fixture
    def form_ctrl(self):
        return FormController()

    # ── TC-A-018: อาจารย์ดูฟอร์ม 1 ของนักศึกษา ───
    async def test_view_student_form1(self, form_ctrl):
        """อาจารย์ดูฟอร์ม 1 ที่นักศึกษายื่น → เห็นข้อมูลนักศึกษาและอาจารย์ที่ปรึกษา"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM1_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form1_detail("sub001")

        assert result["success"] is True
        data = result["data"]
        assert data["student_name"] == "นายสมชาย ใจดี"
        assert data["main_advisor"] == "ผศ.ดร.สมศรี รักเรียน"
        assert data["program_name"] == "วิทยาการคอมพิวเตอร์"

    # ── TC-A-019: อาจารย์ดูฟอร์ม 2 ของนักศึกษา ───
    async def test_view_student_form2(self, form_ctrl):
        """อาจารย์ดูฟอร์ม 2 → เห็นคณะกรรมการสอบ"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM2_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form2_detail("sub002")

        assert result["success"] is True
        data = result["data"]
        assert data["chair"] == "รศ.ดร.สุรศักดิ์ มั่นคง"
        assert data["committee"] == "ดร.สมหญิง ดีงาม"

    # ── TC-A-020: อาจารย์ดูฟอร์ม 3 ของนักศึกษา ───
    async def test_view_student_form3(self, form_ctrl):
        """อาจารย์ดูฟอร์ม 3 → เห็นหัวข้อวิทยานิพนธ์ที่อนุมัติ"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM3_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form3_detail("sub003")

        assert result["success"] is True
        assert result["data"]["title_th"] == "ระบบติดตามนักศึกษา"
        assert result["data"]["approve_date"] == "2025-07-01"

    # ── TC-A-021: อาจารย์ดูฟอร์ม 4 ของนักศึกษา ───
    async def test_view_student_form4(self, form_ctrl):
        """อาจารย์ดูฟอร์ม 4 → เห็นข้อมูลผู้ทรงคุณวุฒิ"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM4_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form4_detail("sub004")

        assert result["success"] is True
        data = result["data"]
        assert data["expert_name"] == "ประสิทธิ์"
        assert data["expert_org"] == "จุฬาลงกรณ์มหาวิทยาลัย"

    # ── TC-A-022: อาจารย์ดูฟอร์ม 5 ของนักศึกษา ───
    async def test_view_student_form5(self, form_ctrl):
        """อาจารย์ดูฟอร์ม 5 → เห็นวิธีการเก็บข้อมูล"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM5_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form5_detail("sub005")

        assert result["success"] is True
        assert result["data"]["check_questionnaire"] is True
        assert result["data"]["check_test"] is True

    # ── TC-A-023: อาจารย์ดูฟอร์ม 6 ของนักศึกษา ───
    async def test_view_student_form6(self, form_ctrl):
        """อาจารย์ดูฟอร์ม 6 → เห็นคณะกรรมการสอบและกรรมการสำรอง"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM6_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form6_detail("sub006")

        assert result["success"] is True
        data = result["data"]
        assert data["main_advisor"] == "ผศ.ดร.สมศรี รักเรียน"
        assert data["chair"] == "รศ.ดร.สุรศักดิ์ มั่นคง"
        assert data["reserve_int"] == "ผศ.ดร.สมศรี รักเรียน"

    # ── TC-A-024: อาจารย์ดูผลสอบของนักศึกษา ───
    async def test_view_student_exam_result(self, form_ctrl):
        """อาจารย์ดูผลสอบ → เห็นประเภทสอบ + คะแนน + ไฟล์แนบ"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(EXAM_RESULT_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_exam_result_detail("sub007")

        assert result["success"] is True
        data = result["data"]
        assert data["exam_type"] == "TOEIC"
        assert data["result_score"] == "750"
        assert data["doc_type"] == "แบบฟอร์มยื่นผลสอบ TOEIC"

    # ── TC-A-025: API error ตอนดึงฟอร์ม ───
    async def test_form_api_error(self, form_ctrl):
        """API error ตอนดึงข้อมูลฟอร์ม → แสดง error"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(None, "ไม่สามารถดึงข้อมูลได้"),
        ):
            result = await form_ctrl.get_form1_detail("sub001")

        assert result["success"] is False

    # ── TC-A-026: submission_id ว่าง ───
    async def test_form_empty_submission_id(self, form_ctrl):
        """ส่ง submission_id ว่าง → แสดง error"""
        result = await form_ctrl.get_form6_detail("")
        assert result["success"] is False
        assert "ว่างเปล่า" in result["message"]
