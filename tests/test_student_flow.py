# ==============================================================================
# tests/test_student_flow.py — Test Cases สำหรับบทบาทนักศึกษา
# ==============================================================================
# ทดสอบ Flow ทั้งหมดที่นักศึกษาสามารถทำได้หลัง Login:
#   1. Login เข้าสู่ระบบ
#   2. ดู Dashboard หน้าหลัก (เอกสาร + กิจกรรม)
#   3. ดูโปรไฟล์ส่วนตัว
#   4. ดูรายละเอียดแบบฟอร์ม 1-6 + ผลสอบ
# ==============================================================================
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from controllers.auth_controller import AuthController
from controllers.student_controller import StudentController
from controllers.form_controller import FormController
from core.auth_guard import require_auth
from conftest import (
    STUDENT_LOGIN_RESPONSE,
    STUDENT_DASHBOARD_RESPONSE,
    STUDENT_PROFILE_RESPONSE,
    FORM1_DETAIL_RESPONSE,
    FORM2_DETAIL_RESPONSE,
    FORM3_DETAIL_RESPONSE,
    FORM4_DETAIL_RESPONSE,
    FORM5_DETAIL_RESPONSE,
    FORM6_DETAIL_RESPONSE,
    EXAM_RESULT_DETAIL_RESPONSE,
)


# ══════════════════════════════════════════════
# 1. นักศึกษา Login เข้าสู่ระบบ
# ══════════════════════════════════════════════
class TestStudentLogin:
    """ทดสอบการ Login ในบทบาทนักศึกษา"""

    @pytest.fixture
    def auth_ctrl(self):
        return AuthController()

    # ── TC-S-001: Login สำเร็จ ───
    async def test_login_success(self, auth_ctrl):
        """นักศึกษา login สำเร็จ → redirect ไปหน้า student_home"""
        with patch.object(
            auth_ctrl.service,
            "login_api",
            new_callable=AsyncMock,
            return_value=(STUDENT_LOGIN_RESPONSE, None),
        ):
            result = await auth_ctrl.process_login("student@kmitl.ac.th", "password123")

        assert result["success"] is True
        assert result["route"] == "/student_home"
        assert result["session_data"]["user_role"] == "student"
        assert result["session_data"]["user_id"] == "S001"
        assert result["session_data"]["user_full_name"] == "นายสมชาย ใจดี"

    # ── TC-S-002: ไม่กรอกอีเมล ───
    async def test_login_empty_email(self, auth_ctrl):
        """ไม่กรอกอีเมล → แสดง error กรุณากรอกอีเมล"""
        result = await auth_ctrl.process_login("", "password123")
        assert result["success"] is False
        assert "อีเมล" in result["message"]

    # ── TC-S-003: ไม่กรอกรหัสผ่าน ───
    async def test_login_empty_password(self, auth_ctrl):
        """ไม่กรอกรหัสผ่าน → แสดง error กรุณากรอกรหัสผ่าน"""
        result = await auth_ctrl.process_login("student@kmitl.ac.th", "")
        assert result["success"] is False
        assert "รหัสผ่าน" in result["message"]

    # ── TC-S-004: อีเมลและรหัสผ่านว่างทั้งคู่ ───
    async def test_login_both_empty(self, auth_ctrl):
        """ไม่กรอกทั้งอีเมลและรหัสผ่าน → แสดง error อีเมลก่อน"""
        result = await auth_ctrl.process_login("", "")
        assert result["success"] is False
        assert "อีเมล" in result["message"]

    # ── TC-S-005: API ตอบ error (เซิร์ฟเวอร์มีปัญหา) ───
    async def test_login_server_error(self, auth_ctrl):
        """API ตอบ error → แสดงข้อความเซิร์ฟเวอร์มีปัญหา"""
        with patch.object(
            auth_ctrl.service,
            "login_api",
            new_callable=AsyncMock,
            return_value=(None, "เซิร์ฟเวอร์มีปัญหา"),
        ):
            result = await auth_ctrl.process_login("student@kmitl.ac.th", "password123")

        assert result["success"] is False
        assert "เซิร์ฟเวอร์" in result["message"]

    # ── TC-S-006: อีเมลหรือรหัสผ่านไม่ถูกต้อง ───
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

    # ── TC-S-007: API ตอบกลับแต่ไม่มี user_id ───
    async def test_login_no_user_id_in_response(self, auth_ctrl):
        """API ตอบ JSON กลับมา แต่ไม่มี id → ล็อกอินไม่สำเร็จ"""
        bad_response = {"student": {"name": "Test", "role": "student"}}
        with patch.object(
            auth_ctrl.service,
            "login_api",
            new_callable=AsyncMock,
            return_value=(bad_response, None),
        ):
            result = await auth_ctrl.process_login("student@kmitl.ac.th", "password123")

        assert result["success"] is False
        assert "ไม่พบรหัสผู้ใช้" in result["message"]

    # ── TC-S-008: กรอกอีเมลเป็นช่องว่าง (whitespace) ───
    async def test_login_whitespace_email(self, auth_ctrl):
        """กรอกอีเมลเป็นช่องว่าง → ถือว่าว่าง"""
        result = await auth_ctrl.process_login("   ", "password123")
        assert result["success"] is False
        assert "อีเมล" in result["message"]


# ══════════════════════════════════════════════
# 2. ตรวจสอบสิทธิ์เข้าถึง (Auth Guard)
# ══════════════════════════════════════════════
class TestStudentAuthGuard:
    """ทดสอบ Auth Guard สำหรับนักศึกษา"""

    # ── TC-S-009: มี Session → เข้าถึงได้ ───
    def test_auth_guard_with_session(self, mock_page):
        """ถ้า login แล้ว (มี user_id ใน session) → คืน user_id"""
        mock_page.session.get.return_value = "S001"

        user_id = require_auth(mock_page)

        assert user_id == "S001"
        mock_page.go.assert_not_called()

    # ── TC-S-010: ไม่มี Session → redirect ไป login ───
    def test_auth_guard_without_session(self, mock_page):
        """ถ้ายังไม่ได้ login (ไม่มี user_id) → redirect ไปหน้า login"""
        mock_page.session.get.return_value = None

        user_id = require_auth(mock_page)

        assert user_id is None
        mock_page.go.assert_called_once_with("/login")


# ══════════════════════════════════════════════
# 3. นักศึกษา ดู Dashboard หน้าหลัก
# ══════════════════════════════════════════════
class TestStudentDashboard:
    """ทดสอบการดู Dashboard ของนักศึกษา"""

    @pytest.fixture
    def student_ctrl(self):
        return StudentController()

    # ── TC-S-011: ดู Dashboard สำเร็จ ───
    async def test_dashboard_success(self, student_ctrl):
        """ดึงข้อมูล Dashboard สำเร็จ → มีชื่อ + เอกสารปัจจุบัน + กิจกรรม"""
        with patch.object(
            student_ctrl.service,
            "fetch_home_data",
            new_callable=AsyncMock,
            return_value=(STUDENT_DASHBOARD_RESPONSE, None),
        ):
            result = await student_ctrl.get_dashboard_data("S001", "นายสมชาย ใจดี")

        assert result["success"] is True
        model = result["data"]
        assert model.user_name == "นายสมชาย ใจดี"

    # ── TC-S-012: เอกสารปัจจุบัน (Status Card) แสดงเอกสารที่ pending ───
    async def test_dashboard_current_document(self, student_ctrl):
        """Status Card ต้องแสดงเอกสารที่สถานะ pending"""
        with patch.object(
            student_ctrl.service,
            "fetch_home_data",
            new_callable=AsyncMock,
            return_value=(STUDENT_DASHBOARD_RESPONSE, None),
        ):
            result = await student_ctrl.get_dashboard_data("S001", "นายสมชาย ใจดี")

        model = result["data"]
        assert model.current_doc.doc_name == "แบบฟอร์มขอรับรองอาจารย์ที่ปรึกษา"
        assert model.current_doc.status_text == "รอดำเนินการ"

    # ── TC-S-013: แปลสถานะจากอังกฤษเป็นไทย ───
    async def test_dashboard_status_translation(self, student_ctrl):
        """สถานะ pending/approved/rejected ต้องแปลเป็นภาษาไทย"""
        with patch.object(
            student_ctrl.service,
            "fetch_home_data",
            new_callable=AsyncMock,
            return_value=(STUDENT_DASHBOARD_RESPONSE, None),
        ):
            result = await student_ctrl.get_dashboard_data("S001", "นายสมชาย ใจดี")

        activities = result["data"].activities
        assert activities[0].status == "รอดำเนินการ"      # pending
        assert activities[1].status == "อนุมัติเรียบร้อย"   # approved
        assert activities[2].status == "ถูกปฏิเสธ แก้ไขด่วน"  # rejected

    # ── TC-S-014: รายการกิจกรรมครบทุกเอกสาร ───
    async def test_dashboard_all_activities_listed(self, student_ctrl):
        """รายการกิจกรรมต้องแสดงเอกสารทั้ง 3 รายการ"""
        with patch.object(
            student_ctrl.service,
            "fetch_home_data",
            new_callable=AsyncMock,
            return_value=(STUDENT_DASHBOARD_RESPONSE, None),
        ):
            result = await student_ctrl.get_dashboard_data("S001", "นายสมชาย ใจดี")

        activities = result["data"].activities
        assert len(activities) == 3
        assert activities[0].form_type == "form1"
        assert activities[1].form_type == "form2"
        assert activities[2].form_type == "exam_result"
        assert activities[0].submission_id == "sub001"

    # ── TC-S-015: Dashboard API error ───
    async def test_dashboard_api_error(self, student_ctrl):
        """API error → ส่ง error message กลับ"""
        with patch.object(
            student_ctrl.service,
            "fetch_home_data",
            new_callable=AsyncMock,
            return_value=(None, "เชื่อมต่อเซิร์ฟเวอร์ไม่ได้"),
        ):
            result = await student_ctrl.get_dashboard_data("S001", "นายสมชาย ใจดี")

        assert result["success"] is False
        assert "เชื่อมต่อ" in result["message"]

    # ── TC-S-016: ไม่มีเอกสาร pending → Status Card แสดงค่า default ───
    async def test_dashboard_no_pending_document(self, student_ctrl):
        """ถ้าไม่มีเอกสาร pending → Status Card แสดง '-'"""
        no_pending = {"documents": [
            {"name": "ฟอร์ม 1", "status": "approved", "form_type": "form1", "submission_id": "sub001"}
        ]}
        with patch.object(
            student_ctrl.service,
            "fetch_home_data",
            new_callable=AsyncMock,
            return_value=(no_pending, None),
        ):
            result = await student_ctrl.get_dashboard_data("S001", "นายสมชาย ใจดี")

        assert result["data"].current_doc.doc_name == "-"
        assert result["data"].current_doc.status_text == "-"


# ══════════════════════════════════════════════
# 4. นักศึกษา ดูโปรไฟล์
# ══════════════════════════════════════════════
class TestStudentProfile:
    """ทดสอบการดูโปรไฟล์ของนักศึกษา"""

    @pytest.fixture
    def student_ctrl(self):
        return StudentController()

    # ── TC-S-017: ดูโปรไฟล์สำเร็จ ───
    async def test_profile_success(self, student_ctrl):
        """ดึงข้อมูลโปรไฟล์สำเร็จ → มีข้อมูลส่วนตัวครบ"""
        with patch.object(
            student_ctrl.service,
            "fetch_profile_data",
            new_callable=AsyncMock,
            return_value=(STUDENT_PROFILE_RESPONSE, None),
        ):
            result = await student_ctrl.get_profile_data("S001", "นายสมชาย ใจดี", "student")

        assert result["success"] is True
        profile = result["data"]
        assert profile.full_name == "นายสมชาย ใจดี"
        assert profile.email == "somchai@kmitl.ac.th"
        assert profile.phone == "0812345678"
        assert profile.faculty == "คณะเทคโนโลยีสารสนเทศ"
        assert profile.major == "วิทยาการคอมพิวเตอร์"
        assert profile.status == "กำลังศึกษา"

    # ── TC-S-018: ข้อมูลวิทยานิพนธ์ ───
    async def test_profile_thesis_data(self, student_ctrl):
        """โปรไฟล์ต้องมีข้อมูลวิทยานิพนธ์"""
        with patch.object(
            student_ctrl.service,
            "fetch_profile_data",
            new_callable=AsyncMock,
            return_value=(STUDENT_PROFILE_RESPONSE, None),
        ):
            result = await student_ctrl.get_profile_data("S001", "นายสมชาย ใจดี", "student")

        thesis = result["data"].thesis
        assert thesis.title_th == "ระบบติดตามนักศึกษาบัณฑิตศึกษา"
        assert thesis.title_en == "Graduate Student Tracking System"
        assert thesis.main_advisor == "ผศ.ดร.สมศรี รักเรียน"

    # ── TC-S-019: ข้อมูลความคืบหน้า ───
    async def test_profile_progress_data(self, student_ctrl):
        """โปรไฟล์ต้องมีข้อมูลความคืบหน้าการเรียน"""
        with patch.object(
            student_ctrl.service,
            "fetch_profile_data",
            new_callable=AsyncMock,
            return_value=(STUDENT_PROFILE_RESPONSE, None),
        ):
            result = await student_ctrl.get_profile_data("S001", "นายสมชาย ใจดี", "student")

        progress = result["data"].progress
        assert progress.topic_exam_date == "2025-06-15"
        assert progress.topic_status == "ผ่าน"
        assert progress.english_test_type == "TOEIC"
        assert progress.english_test_status == "ผ่าน"

    # ── TC-S-020: Security Check — ID ไม่ตรง ───
    async def test_profile_security_id_mismatch(self, student_ctrl):
        """ถ้า API ส่งข้อมูลคนอื่นมา → reject"""
        wrong_data = {"student": {"id": "S999", "name": "คนอื่น"}}
        with patch.object(
            student_ctrl.service,
            "fetch_profile_data",
            new_callable=AsyncMock,
            return_value=(wrong_data, None),
        ):
            result = await student_ctrl.get_profile_data("S001", "นายสมชาย ใจดี", "student")

        assert result["success"] is False
        assert "ไม่ตรง" in result["message"]

    # ── TC-S-021: Profile API error ───
    async def test_profile_api_error(self, student_ctrl):
        """API error → ส่ง error message กลับ"""
        with patch.object(
            student_ctrl.service,
            "fetch_profile_data",
            new_callable=AsyncMock,
            return_value=(None, "เชื่อมต่อเซิร์ฟเวอร์ไม่ได้"),
        ):
            result = await student_ctrl.get_profile_data("S001", "นายสมชาย ใจดี", "student")

        assert result["success"] is False


# ══════════════════════════════════════════════
# 5. นักศึกษา ดูรายละเอียดแบบฟอร์ม (Form 1-6 + Exam Result)
# ══════════════════════════════════════════════
class TestStudentViewFormDetails:
    """ทดสอบการดูรายละเอียดแบบฟอร์มของนักศึกษา"""

    @pytest.fixture
    def form_ctrl(self):
        return FormController()

    # ── TC-S-022: ดูฟอร์ม 1 (ขอรับรองอาจารย์ที่ปรึกษา) ───
    async def test_view_form1_detail(self, form_ctrl):
        """ดูรายละเอียดฟอร์ม 1 → มีชื่อนักศึกษา + อาจารย์ที่ปรึกษา"""
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
        assert data["student_id"] == "S001"
        assert data["degree"] == "ปริญญาโท"
        assert data["main_advisor"] == "ผศ.ดร.สมศรี รักเรียน"
        assert data["co_advisor"] == "ดร.สมหญิง ดีงาม"
        assert data["faculty"] == "คณะเทคโนโลยีสารสนเทศ"

    # ── TC-S-023: ดูฟอร์ม 2 (เสนอหัวข้อวิทยานิพนธ์) ───
    async def test_view_form2_detail(self, form_ctrl):
        """ดูรายละเอียดฟอร์ม 2 → มีคณะกรรมการสอบ"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM2_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form2_detail("sub002")

        assert result["success"] is True
        data = result["data"]
        assert data["student_name"] == "นายสมชาย ใจดี"
        assert data["chair"] == "รศ.ดร.สุรศักดิ์ มั่นคง"
        assert data["main_advisor"] == "ผศ.ดร.สมศรี รักเรียน"
        assert data["reserve_ext"] == "ศ.ดร.ประสิทธิ์ สูงส่ง"

    # ── TC-S-024: ดูฟอร์ม 3 (เค้าโครงวิทยานิพนธ์) ───
    async def test_view_form3_detail(self, form_ctrl):
        """ดูรายละเอียดฟอร์ม 3 → มีหัวข้อที่อนุมัติ"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM3_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form3_detail("sub003")

        assert result["success"] is True
        data = result["data"]
        assert data["title_th"] == "ระบบติดตามนักศึกษา"
        assert data["title_en"] == "Student Tracking System"
        assert data["approve_date"] == "2025-07-01"

    # ── TC-S-025: ดูฟอร์ม 4 (ขอเชิญผู้ทรงคุณวุฒิ) ───
    async def test_view_form4_detail(self, form_ctrl):
        """ดูรายละเอียดฟอร์ม 4 → มีข้อมูลผู้ทรงคุณวุฒิ"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM4_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form4_detail("sub004")

        assert result["success"] is True
        data = result["data"]
        assert data["expert_title"] == "ศ.ดร."
        assert data["expert_name"] == "ประสิทธิ์"
        assert data["expert_surname"] == "สูงส่ง"
        assert data["expert_org"] == "จุฬาลงกรณ์มหาวิทยาลัย"
        assert data["expert_email"] == "prasit@chula.ac.th"

    # ── TC-S-026: ดูฟอร์ม 5 (ขอเก็บรวบรวมข้อมูล) ───
    async def test_view_form5_detail(self, form_ctrl):
        """ดูรายละเอียดฟอร์ม 5 → มี checkbox วิธีเก็บข้อมูล"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM5_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form5_detail("sub005")

        assert result["success"] is True
        data = result["data"]
        assert data["check_questionnaire"] is True   # เลือกแบบสอบถาม
        assert data["check_test"] is True             # เลือกแบบทดสอบ
        assert data["check_teaching"] is False        # ไม่เลือกทดลองสอน
        assert data["check_other"] is False           # ไม่เลือกอื่นๆ

    # ── TC-S-027: ดูฟอร์ม 5 — เลือก "อื่นๆ" พร้อมรายละเอียด ───
    async def test_view_form5_with_other_method(self, form_ctrl):
        """ฟอร์ม 5 เลือก 'อื่นๆ' → ต้องมีรายละเอียดเพิ่มเติม"""
        data_with_other = {
            "documentDetail": {
                "prefix_th": "นาย", "first_name_th": "สมชาย", "last_name_th": "ใจดี",
                "student_id": "S001", "degree": "ปริญญาโท",
                "program_name": "วิทยาการคอมพิวเตอร์", "department_name": "เทคโนโลยีสารสนเทศ",
                "form_details": {
                    "approved_date": "2025-09-01",
                    "thesis_title_th": "ระบบติดตามนักศึกษา",
                    "thesis_title_en": "Student Tracking System",
                    "collection_methods": ["questionnaire", "other"],
                    "other_detail": "สัมภาษณ์เชิงลึก",
                },
            },
            "advisors": [],
        }
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(data_with_other, None),
        ):
            result = await form_ctrl.get_form5_detail("sub005")

        data = result["data"]
        assert data["check_other"] is True
        assert data["other_detail"] == "สัมภาษณ์เชิงลึก"

    # ── TC-S-028: ดูฟอร์ม 6 (แต่งตั้งกรรมการสอบ) ───
    async def test_view_form6_detail(self, form_ctrl):
        """ดูรายละเอียดฟอร์ม 6 → มีคณะกรรมการ + กรรมการสำรอง"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(FORM6_DETAIL_RESPONSE, None),
        ):
            result = await form_ctrl.get_form6_detail("sub006")

        assert result["success"] is True
        data = result["data"]
        assert data["student_name"] == "นายสมชาย ใจดี"
        assert data["start_semester"] == "1"
        assert data["start_year"] == "2567"
        assert data["workplace"] == "บริษัท ABC จำกัด"
        assert data["chair"] == "รศ.ดร.สุรศักดิ์ มั่นคง"
        assert data["main_advisor"] == "ผศ.ดร.สมศรี รักเรียน"
        assert data["reserve_ext"] == "ศ.ดร.ประสิทธิ์ สูงส่ง"

    # ── TC-S-029: ดูผลสอบ (Exam Result) ───
    async def test_view_exam_result_detail(self, form_ctrl):
        """ดูรายละเอียดผลสอบ → มีประเภทสอบ + วันที่ + คะแนน + ไฟล์"""
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
        assert data["exam_date"] == "2025-03-10"
        assert data["result_score"] == "750"
        assert len(data["files"]) == 1
        assert data["files"][0]["file_name"] == "toeic_score.pdf"

    # ── TC-S-030: submission_id ว่าง → error ───
    async def test_form_empty_submission_id(self, form_ctrl):
        """ส่ง submission_id ว่าง → แสดง error"""
        result = await form_ctrl.get_form1_detail("")
        assert result["success"] is False
        assert "ว่างเปล่า" in result["message"]

    # ── TC-S-031: submission_id เป็น whitespace ───
    async def test_form_whitespace_submission_id(self, form_ctrl):
        """ส่ง submission_id เป็นช่องว่าง → ถือว่าว่าง"""
        result = await form_ctrl.get_form2_detail("   ")
        assert result["success"] is False
        assert "ว่างเปล่า" in result["message"]

    # ── TC-S-032: API error ตอนดึงข้อมูลฟอร์ม ───
    async def test_form_api_error(self, form_ctrl):
        """API error ตอนดึงข้อมูลฟอร์ม → แสดง error"""
        with patch.object(
            form_ctrl.service,
            "fetch_submission_detail",
            new_callable=AsyncMock,
            return_value=(None, "ไม่สามารถดึงข้อมูลได้ (Error: 500)"),
        ):
            result = await form_ctrl.get_form3_detail("sub003")

        assert result["success"] is False
        assert "Error" in result["message"]

    # ── TC-S-033: ค้นหาชื่ออาจารย์จาก ID ที่ไม่มีในระบบ ───
    async def test_advisor_name_not_found(self, form_ctrl):
        """ถ้า advisor_id ไม่ตรงกับใคร → แสดง 'รหัส XXX'"""
        result = form_ctrl._get_advisor_name("UNKNOWN_ID", [
            {"advisor_id": "ADV001", "prefix_th": "ดร.", "first_name_th": "ทดสอบ", "last_name_th": "ระบบ"}
        ])
        assert "รหัส" in result
        assert "UNKNOWN_ID" in result

    # ── TC-S-034: ค้นหาชื่ออาจารย์ที่ไม่มี ID ───
    async def test_advisor_name_empty_id(self, form_ctrl):
        """ถ้า advisor_id เป็น None → คืน '-'"""
        result = form_ctrl._get_advisor_name(None, [])
        assert result == "-"
