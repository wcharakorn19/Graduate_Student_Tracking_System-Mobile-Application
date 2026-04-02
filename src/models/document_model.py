# ==============================================================================
# src/models/document_model.py — Data Model สำหรับเอกสารและ Dashboard
# ==============================================================================
# ไฟล์นี้กำหนดโครงสร้างข้อมูลที่ใช้ในหน้า Dashboard ของทั้งนักศึกษาและอาจารย์
#
# ประกอบด้วย 5 คลาส:
#   1. ActivityModel          — กิจกรรม/เอกสารแต่ละรายการ
#   2. CurrentDocumentModel   — เอกสารปัจจุบันที่แสดงบน Status Card
#   3. StudentDashboardModel  — ข้อมูล Dashboard ของนักศึกษา
#   4. StudentSummaryModel    — ข้อมูลสรุปนักศึกษาแต่ละคน (สำหรับอาจารย์ดู)
#   5. AdvisorDashboardModel  — ข้อมูล Dashboard ของอาจารย์ที่ปรึกษา
# ==============================================================================
from dataclasses import dataclass, field
from typing import List


@dataclass
class ActivityModel:
    """
    โมเดลกิจกรรม/เอกสาร 1 รายการ
    ใช้แสดงในรายการ "Latest Activities"
    """
    title: str              # ชื่อเอกสาร (เช่น "แบบฟอร์มขอรับรองอาจารย์ที่ปรึกษา")
    status: str             # สถานะ (เช่น "รอดำเนินการ", "อนุมัติเรียบร้อย")
    name: str = ""          # ชื่อเจ้าของเอกสาร (ใช้ในฝั่ง Advisor)
    form_type: str = "form1"    # ประเภทฟอร์ม (form1-form6, exam_result) ใช้สร้าง route
    submission_id: str = ""     # รหัสเอกสาร ใช้นำทางไปหน้ารายละเอียด


@dataclass
class CurrentDocumentModel:
    """
    โมเดลเอกสารปัจจุบัน ที่แสดงบน "Status Card" หน้าหลัก
    แสดงเอกสารที่กำลัง "รอดำเนินการ" เพื่อให้นักศึกษาเห็นสถานะเด่นชัด
    """
    doc_name: str           # ชื่อเอกสาร
    status_label: str       # ข้อความ label (เช่น "สถานะ :")
    status_text: str        # ข้อความสถานะ (เช่น "รอดำเนินการ")


@dataclass
class StudentDashboardModel:
    """
    โมเดลข้อมูล Dashboard สำหรับหน้าหลักนักศึกษา
    ประกอบด้วย: ชื่อนักศึกษา, เอกสารปัจจุบัน, และรายการกิจกรรม
    """
    user_name: str                          # ชื่อนักศึกษาที่แสดงบนหน้าจอ
    current_doc: CurrentDocumentModel       # เอกสารที่กำลังดำเนินการ
    activities: List[ActivityModel] = field(default_factory=list)  # รายการกิจกรรมทั้งหมด


@dataclass
class StudentSummaryModel:
    """
    โมเดลสรุปข้อมูลนักศึกษาแต่ละคน (ใช้แสดงในหน้าหลักอาจารย์)
    แสดงชื่อนักศึกษาพร้อมสถานะเอกสาร
    """
    name: str               # ชื่อนักศึกษา
    doc_status: str          # สถานะเอกสาร
    student_id: str = ""     # รหัสนักศึกษา (ใช้นำทางไปหน้าโปรไฟล์)


@dataclass
class AdvisorDashboardModel:
    """
    โมเดลข้อมูล Dashboard สำหรับหน้าหลักอาจารย์ที่ปรึกษา
    ประกอบด้วย: จำนวนนักศึกษา, รายชื่อนักศึกษา, และรายการกิจกรรม
    """
    student_count: int      # จำนวนนักศึกษาที่ดูแลทั้งหมด
    students: List[StudentSummaryModel] = field(default_factory=list)  # รายชื่อนักศึกษา
    activities: List[ActivityModel] = field(default_factory=list)      # รายการกิจกรรม
