# ==============================================================================
# tests/conftest.py — Shared Fixtures สำหรับ Test ทั้งหมด
# ==============================================================================
# รวม Mock Data ที่จำลองข้อมูลจาก API (Postman Mock Server)
# เพื่อใช้ในการทดสอบโดยไม่ต้องเชื่อมต่อ API จริง
# ==============================================================================
import pytest
from unittest.mock import MagicMock


# ══════════════════════════════════════════════
# Mock API Responses — จำลองข้อมูลที่ API ส่งกลับมา
# ══════════════════════════════════════════════

# ─── Login Response: นักศึกษา ───
STUDENT_LOGIN_RESPONSE = {
    "student": {
        "id": "S001",
        "name": "นายสมชาย ใจดี",
        "role": "student",
    }
}

# ─── Login Response: อาจารย์ที่ปรึกษา ───
ADVISOR_LOGIN_RESPONSE = {
    "advisor": {
        "id": "A001",
        "name": "ผศ.ดร.สมศรี รักเรียน",
        "role": "advisor",
    }
}

# ─── Student Dashboard Response ───
STUDENT_DASHBOARD_RESPONSE = {
    "documents": [
        {
            "name": "แบบฟอร์มขอรับรองอาจารย์ที่ปรึกษา",
            "status": "pending",
            "form_type": "form1",
            "submission_id": "sub001",
        },
        {
            "name": "แบบเสนอหัวข้อวิทยานิพนธ์",
            "status": "approved",
            "form_type": "form2",
            "submission_id": "sub002",
        },
        {
            "name": "แบบยื่นผลสอบ",
            "status": "rejected",
            "form_type": "exam_result",
            "submission_id": "sub003",
        },
    ]
}

# ─── Student Profile Response ───
STUDENT_PROFILE_RESPONSE = {
    "student": {
        "id": "S001",
        "name": "นายสมชาย ใจดี",
        "role": "student",
        "email": "somchai@kmitl.ac.th",
        "phone": "0812345678",
        "education_level": "ปริญญาโท",
        "faculty": "คณะเทคโนโลยีสารสนเทศ",
        "program": "วิทยาการคอมพิวเตอร์",
        "status": "กำลังศึกษา",
        "thesis": {
            "title_th": "ระบบติดตามนักศึกษาบัณฑิตศึกษา",
            "title_en": "Graduate Student Tracking System",
            "main_advisor": "ผศ.ดร.สมศรี รักเรียน",
            "co_advisor_1": "ดร.สมหญิง ดีงาม",
            "co_advisor_2": "-",
        },
        "progress": {
            "topic_exam_date": "2025-06-15",
            "topic_status": "ผ่าน",
            "topic_approve_date": "2025-06-20",
            "final_exam_date": "-",
            "final_status": "-",
            "final_approve_date": "-",
            "english_test_type": "TOEIC",
            "english_test_date": "2025-03-10",
            "english_test_status": "ผ่าน",
        },
    }
}

# ─── Advisor Dashboard Response ───
ADVISOR_DASHBOARD_RESPONSE = {
    "student_count": 3,
    "students": [
        {"name": "นายสมชาย ใจดี", "doc_status": "รอดำเนินการ", "student_id": "S001"},
        {"name": "นางสาวสมหญิง รักเรียน", "doc_status": "อนุมัติแล้ว", "student_id": "S002"},
        {"name": "นายสมศักดิ์ ดีงาม", "doc_status": "รอดำเนินการ", "student_id": "S003"},
    ],
    "activities": [
        {
            "doc_name": "แบบฟอร์มขอรับรองอาจารย์ที่ปรึกษา",
            "status": "รอดำเนินการ",
            "name": "นายสมชาย ใจดี",
            "form_type": "form1",
            "submission_id": "sub001",
        },
        {
            "doc_name": "แบบเสนอหัวข้อวิทยานิพนธ์",
            "status": "อนุมัติเรียบร้อย",
            "name": "นางสาวสมหญิง รักเรียน",
            "form_type": "form2",
            "submission_id": "sub002",
        },
    ],
}

# ─── Advisor Profile Response ───
ADVISOR_PROFILE_RESPONSE = {
    "advisor": {
        "id": "A001",
        "name": "ผศ.ดร.สมศรี รักเรียน",
        "role": "advisor",
        "email": "somsri@kmitl.ac.th",
        "phone": "0899876543",
        "academic_position": "ผู้ช่วยศาสตราจารย์",
        "advisor_type": "อาจารย์ประจำ",
        "workplace": "คณะเทคโนโลยีสารสนเทศ",
        "approval_role": "ประธานหลักสูตร",
        "program": "วิทยาการคอมพิวเตอร์",
    }
}

# ─── Form Detail Responses (ใช้ร่วมกันทั้ง Student และ Advisor) ───
FORM1_DETAIL_RESPONSE = {
    "documentDetail": {
        "prefix_th": "นาย",
        "first_name_th": "สมชาย",
        "last_name_th": "ใจดี",
        "student_id": "S001",
        "degree": "ปริญญาโท",
        "program_name": "วิทยาการคอมพิวเตอร์",
        "department_name": "เทคโนโลยีสารสนเทศ",
        "faculty": "คณะเทคโนโลยีสารสนเทศ",
        "plan": "แผน ก",
        "phone": "0812345678",
        "email": "somchai@kmitl.ac.th",
        "form_details": {
            "main_advisor_id": "ADV001",
            "co_advisor_id": "ADV002",
        },
    },
    "advisors": [
        {
            "advisor_id": "ADV001",
            "prefix_th": "ผศ.ดร.",
            "first_name_th": "สมศรี",
            "last_name_th": "รักเรียน",
        },
        {
            "advisor_id": "ADV002",
            "prefix_th": "ดร.",
            "first_name_th": "สมหญิง",
            "last_name_th": "ดีงาม",
        },
    ],
}

FORM2_DETAIL_RESPONSE = {
    "documentDetail": {
        "prefix_th": "นาย",
        "first_name_th": "สมชาย",
        "last_name_th": "ใจดี",
        "student_id": "S001",
        "degree": "ปริญญาโท",
        "program_name": "วิทยาการคอมพิวเตอร์",
        "department_name": "เทคโนโลยีสารสนเทศ",
        "form_details": {
            "main_advisor_id": "ADV001",
            "co_advisor_id": "ADV002",
            "committee": {
                "chair_id": "ADV003",
                "co_advisor2_id": "ADV002",
                "member5_id": "ADV004",
                "reserve_external_id": "ADV005",
                "reserve_internal_id": "ADV001",
            },
        },
    },
    "advisors": [
        {"advisor_id": "ADV001", "prefix_th": "ผศ.ดร.", "first_name_th": "สมศรี", "last_name_th": "รักเรียน"},
        {"advisor_id": "ADV002", "prefix_th": "ดร.", "first_name_th": "สมหญิง", "last_name_th": "ดีงาม"},
        {"advisor_id": "ADV003", "prefix_th": "รศ.ดร.", "first_name_th": "สุรศักดิ์", "last_name_th": "มั่นคง"},
        {"advisor_id": "ADV004", "prefix_th": "ดร.", "first_name_th": "พิชิต", "last_name_th": "เจริญ"},
        {"advisor_id": "ADV005", "prefix_th": "ศ.ดร.", "first_name_th": "ประสิทธิ์", "last_name_th": "สูงส่ง"},
    ],
}

FORM3_DETAIL_RESPONSE = {
    "documentDetail": {
        "prefix_th": "นาย",
        "first_name_th": "สมชาย",
        "last_name_th": "ใจดี",
        "student_id": "S001",
        "degree": "ปริญญาโท",
        "program_name": "วิทยาการคอมพิวเตอร์",
        "department_name": "เทคโนโลยีสารสนเทศ",
        "updated_at": "2025-07-01T10:00:00",
        "form_details": {
            "main_advisor_id": "ADV001",
            "co_advisor_id": "ADV002",
            "approved_date": "2025-07-01",
            "thesis_title_th": "ระบบติดตามนักศึกษา",
            "thesis_title_en": "Student Tracking System",
            "committee": {"chair_id": "ADV003"},
        },
    },
    "advisors": [
        {"advisor_id": "ADV001", "prefix_th": "ผศ.ดร.", "first_name_th": "สมศรี", "last_name_th": "รักเรียน"},
        {"advisor_id": "ADV002", "prefix_th": "ดร.", "first_name_th": "สมหญิง", "last_name_th": "ดีงาม"},
        {"advisor_id": "ADV003", "prefix_th": "รศ.ดร.", "first_name_th": "สุรศักดิ์", "last_name_th": "มั่นคง"},
    ],
}

FORM4_DETAIL_RESPONSE = {
    "documentDetail": {
        "prefix_th": "นาย",
        "first_name_th": "สมชาย",
        "last_name_th": "ใจดี",
        "student_id": "S001",
        "degree": "ปริญญาโท",
        "program_name": "วิทยาการคอมพิวเตอร์",
        "department_name": "เทคโนโลยีสารสนเทศ",
        "form_details": {
            "approved_date": "2025-08-01",
            "thesis_title_th": "ระบบติดตามนักศึกษา",
            "thesis_title_en": "Student Tracking System",
            "expert_info": {
                "title": "ศ.ดร.",
                "firstname": "ประสิทธิ์",
                "lastname": "สูงส่ง",
                "institution": "จุฬาลงกรณ์มหาวิทยาลัย",
                "phone": "0211112222",
                "email": "prasit@chula.ac.th",
            },
        },
    },
    "advisors": [],
}

FORM5_DETAIL_RESPONSE = {
    "documentDetail": {
        "prefix_th": "นาย",
        "first_name_th": "สมชาย",
        "last_name_th": "ใจดี",
        "student_id": "S001",
        "degree": "ปริญญาโท",
        "program_name": "วิทยาการคอมพิวเตอร์",
        "department_name": "เทคโนโลยีสารสนเทศ",
        "form_details": {
            "approved_date": "2025-09-01",
            "thesis_title_th": "ระบบติดตามนักศึกษา",
            "thesis_title_en": "Student Tracking System",
            "collection_methods": ["questionnaire", "test"],
            "other_detail": "",
        },
    },
    "advisors": [],
}

FORM6_DETAIL_RESPONSE = {
    "documentDetail": {
        "prefix_th": "นาย",
        "first_name_th": "สมชาย",
        "last_name_th": "ใจดี",
        "student_id": "S001",
        "degree": "ปริญญาโท",
        "program_name": "วิทยาการคอมพิวเตอร์",
        "department_name": "เทคโนโลยีสารสนเทศ",
        "phone": "0812345678",
        "form_details": {
            "entry_semester": 1,
            "entry_year": 2567,
            "current_address": "กรุงเทพมหานคร",
            "workplace": "บริษัท ABC จำกัด",
            "thesis_title_th": "ระบบติดตามนักศึกษา",
            "thesis_title_en": "Student Tracking System",
            "main_advisor_id": "ADV001",
            "co_advisor_id": "ADV002",
            "committee": {
                "chair_id": "ADV003",
                "co_advisor2_id": "ADV002",
                "member5_id": "ADV004",
                "reserve_external_id": "ADV005",
                "reserve_internal_id": "ADV001",
            },
        },
    },
    "advisors": [
        {"advisor_id": "ADV001", "prefix_th": "ผศ.ดร.", "first_name_th": "สมศรี", "last_name_th": "รักเรียน"},
        {"advisor_id": "ADV002", "prefix_th": "ดร.", "first_name_th": "สมหญิง", "last_name_th": "ดีงาม"},
        {"advisor_id": "ADV003", "prefix_th": "รศ.ดร.", "first_name_th": "สุรศักดิ์", "last_name_th": "มั่นคง"},
        {"advisor_id": "ADV004", "prefix_th": "ดร.", "first_name_th": "พิชิต", "last_name_th": "เจริญ"},
        {"advisor_id": "ADV005", "prefix_th": "ศ.ดร.", "first_name_th": "ประสิทธิ์", "last_name_th": "สูงส่ง"},
    ],
}

EXAM_RESULT_DETAIL_RESPONSE = {
    "documentDetail": {
        "prefix_th": "นาย",
        "first_name_th": "สมชาย",
        "last_name_th": "ใจดี",
        "student_id": "S001",
        "degree": "ปริญญาโท",
        "program_name": "วิทยาการคอมพิวเตอร์",
        "title": "แบบฟอร์มยื่นผลสอบ TOEIC",
        "form_details": {
            "exam_type": "TOEIC",
            "exam_date": "2025-03-10",
            "result": "750",
            "files": [
                {"file_name": "toeic_score.pdf", "file_url": "https://example.com/toeic.pdf"}
            ],
        },
    },
    "advisors": [],
}


# ══════════════════════════════════════════════
# Fixtures — ใช้ร่วมกันใน test files
# ══════════════════════════════════════════════

@pytest.fixture
def mock_page():
    """สร้าง Mock Flet Page สำหรับทดสอบ auth_guard"""
    page = MagicMock()
    page.session = MagicMock()
    return page
