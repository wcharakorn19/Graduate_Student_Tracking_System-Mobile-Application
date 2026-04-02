# ==============================================================================
# src/controllers/form_controller.py — Controller สำหรับจัดการข้อมูลแบบฟอร์ม
# ==============================================================================
# ไฟล์นี้ทำหน้าที่เป็น "สะพาน" ระหว่างหน้าจอ Form Detail กับ FormService
# จัดการแบบฟอร์มทั้ง 7 ประเภท:
#   - Form 1: ขอรับรองอาจารย์ที่ปรึกษาหลัก/ร่วม
#   - Form 2: เสนอหัวข้อและเค้าโครงวิทยานิพนธ์
#   - Form 3: เค้าโครงวิทยานิพนธ์ เล่ม 1
#   - Form 4: ขอหนังสือเชิญผู้ทรงคุณวุฒิ
#   - Form 5: ขอหนังสือขออนุญาตเก็บรวบรวมข้อมูล
#   - Form 6: แต่งตั้งคณะกรรมการสอบวิทยานิพนธ์ขั้นสุดท้าย
#   - Exam Result: ยื่นผลการสอบ
#
# หน้าที่หลัก:
#   1. ตรวจสอบ submission_id (Validation)
#   2. เรียก FormService เพื่อ fetch data จาก API
#   3. แปลง JSON เป็น formatted_data ที่พร้อมใช้แสดงผลบนหน้าจอ
# ==============================================================================
from services.form_service import FormService


class FormController:
    """Controller รวมศูนย์สำหรับจัดการแบบฟอร์มทั้ง 7 ประเภท"""

    def __init__(self):
        # สร้าง instance ของ FormService เพื่อใช้เรียก API
        self.service = FormService()

    # ──────────────────────────────────────────────
    # ฟังก์ชันช่วย (Helper Functions) — ใช้ร่วมกันทุกฟอร์ม
    # ──────────────────────────────────────────────

    def _validate_submission_id(self, submission_id: str):
        """
        ตรวจสอบ submission_id ก่อนยิง API
        - ถ้าว่างเปล่า → คืน error dict
        - ถ้าถูกต้อง → คืน None (ผ่าน)
        """
        if not submission_id or not submission_id.strip():
            return {
                "success": False,
                "message": "รหัสเอกสารไม่ถูกต้อง (ว่างเปล่า)",
                "data": None,
            }

    def _get_advisor_name(self, adv_id, advisors_list):
        """
        ค้นหาชื่ออาจารย์จาก ID ในรายชื่ออาจารย์
        - วน loop หา advisor ที่มี advisor_id ตรงกัน
        - ประกอบชื่อเต็มจาก prefix_th + first_name_th + last_name_th
        - ถ้าหาไม่เจอ → คืน "รหัส {adv_id}"
        """
        if not adv_id:
            return "-"
        for adv in advisors_list:
            if adv.get("advisor_id") == adv_id:
                return f"{adv.get('prefix_th')}{adv.get('first_name_th')} {adv.get('last_name_th')}"
        return f"รหัส {adv_id}"

    # ══════════════════════════════════════════════
    # Form 1: แบบฟอร์มขอรับรองอาจารย์ที่ปรึกษาหลัก/ร่วม
    # ══════════════════════════════════════════════
    async def get_form1_detail(self, submission_id: str):
        """
        ดึงรายละเอียดฟอร์ม 1
        ข้อมูลที่ดึง: ข้อมูลนักศึกษา + อาจารย์ที่ปรึกษาหลัก/ร่วม
        """
        # ตรวจสอบ submission_id
        validation_error = self._validate_submission_id(submission_id)
        if validation_error:
            return validation_error

        # เรียก API เพื่อดึงข้อมูล
        data, error = await self.service.fetch_submission_detail(submission_id)

        if error:
            return {"success": False, "message": error, "data": None}

        # แยกข้อมูลจาก JSON Response
        detail = data.get("documentDetail", {})     # ข้อมูลเอกสาร
        advisors_list = data.get("advisors", [])    # รายชื่ออาจารย์ทั้งหมด

        # ประกอบชื่อนักศึกษาจาก prefix + first + last name
        prefix = detail.get("prefix_th") or ""
        first = detail.get("first_name_th") or ""
        last = detail.get("last_name_th") or ""

        # ดึง ID ของอาจารย์ที่ปรึกษา (ลองหาจาก form_details ก่อน ถ้าไม่มีจึงหาจาก root)
        req_main_id = detail.get("form_details", {}).get(
            "main_advisor_id"
        ) or detail.get("main_advisor_id")
        req_co_id = detail.get("form_details", {}).get("co_advisor_id") or detail.get(
            "co_advisor_id"
        )

        # จัดรูปแบบข้อมูลเพื่อส่งให้หน้าจอแสดงผล
        formatted_data = {
            "student_name": f"{prefix}{first} {last}".strip() or "ไม่ระบุ",
            "student_id": detail.get("student_id", "-"),
            "degree": detail.get("degree", "-"),
            "program_name": detail.get("program_name", "-"),
            "department_name": detail.get("department_name", "-"),
            "faculty": detail.get("faculty", "-"),
            "plan": detail.get("plan", "-"),
            "phone": detail.get("phone", "-"),
            "email": detail.get("email", "-"),
            # ค้นหาชื่ออาจารย์จาก ID
            "main_advisor": self._get_advisor_name(req_main_id, advisors_list),
            "co_advisor": self._get_advisor_name(req_co_id, advisors_list),
        }

        return {"success": True, "data": formatted_data}

    # ══════════════════════════════════════════════
    # Form 2: แบบเสนอหัวข้อและเค้าโครงวิทยานิพนธ์
    # ══════════════════════════════════════════════
    async def get_form2_detail(self, submission_id: str):
        """
        ดึงรายละเอียดฟอร์ม 2
        ข้อมูลที่ดึง: ข้อมูลนักศึกษา + อาจารย์ที่ปรึกษา + คณะกรรมการสอบ
        """
        validation_error = self._validate_submission_id(submission_id)
        if validation_error:
            return validation_error

        data, error = await self.service.fetch_submission_detail(submission_id)

        if error:
            return {"success": False, "message": error, "data": None}

        detail = data.get("documentDetail", {})
        advisors_list = data.get("advisors", [])

        prefix = detail.get("prefix_th") or ""
        first = detail.get("first_name_th") or ""
        last = detail.get("last_name_th") or ""

        form_details = detail.get("form_details", {})
        committee = form_details.get("committee", {})   # ข้อมูลคณะกรรมการสอบ

        # ดึง ID อาจารย์ที่ปรึกษา
        req_main_id = form_details.get("main_advisor_id") or detail.get(
            "main_advisor_id"
        )
        req_co_id = form_details.get("co_advisor_id") or detail.get("co_advisor1_id")

        formatted_data = {
            "student_name": f"{prefix}{first} {last}".strip() or "ไม่ระบุ",
            "student_id": detail.get("student_id", "-"),
            "degree": detail.get("degree", "-"),
            "program_name": detail.get("program_name", "-"),
            "department_name": detail.get("department_name", "-"),
            "main_advisor": self._get_advisor_name(req_main_id, advisors_list),
            "co_advisor": self._get_advisor_name(req_co_id, advisors_list),
            # คณะกรรมการสอบ: ค้นหาชื่อจาก ID ของแต่ละตำแหน่ง
            "chair": self._get_advisor_name(committee.get("chair_id"), advisors_list),
            "committee": self._get_advisor_name(
                committee.get("co_advisor2_id"), advisors_list
            ),
            "member5": self._get_advisor_name(
                committee.get("member5_id"), advisors_list
            ),
            # กรรมการสำรอง
            "reserve_ext": self._get_advisor_name(
                committee.get("reserve_external_id"), advisors_list
            ),
            "reserve_int": self._get_advisor_name(
                committee.get("reserve_internal_id"), advisors_list
            ),
        }

        return {"success": True, "data": formatted_data}

    # ══════════════════════════════════════════════
    # Form 3: แบบเสนอเค้าโครงวิทยานิพนธ์ เล่ม 1
    # ══════════════════════════════════════════════
    async def get_form3_detail(self, submission_id: str):
        """
        ดึงรายละเอียดฟอร์ม 3
        ข้อมูลที่ดึง: ข้อมูลนักศึกษา + หัวข้อวิทยานิพนธ์ที่อนุมัติ + อาจารย์ผู้รับผิดชอบ
        """
        validation_error = self._validate_submission_id(submission_id)
        if validation_error:
            return validation_error

        data, error = await self.service.fetch_submission_detail(submission_id)

        if error:
            return {"success": False, "message": error, "data": None}

        detail = data.get("documentDetail", {})
        advisors_list = data.get("advisors", [])

        prefix = detail.get("prefix_th") or ""
        first = detail.get("first_name_th") or ""
        last = detail.get("last_name_th") or ""

        form_details = detail.get("form_details", {})
        committee = form_details.get("committee", {})

        main_id = form_details.get("main_advisor_id") or detail.get("main_advisor_id")
        co_id = form_details.get("co_advisor_id") or detail.get("co_advisor1_id")

        formatted_data = {
            "student_name": f"{prefix}{first} {last}".strip() or "ไม่ระบุ",
            "student_id": detail.get("student_id", "-"),
            "degree": detail.get("degree", "-"),
            "program_name": detail.get("program_name", "-"),
            "department_name": detail.get("department_name", "-"),
            # วันที่อนุมัติ: ใช้จาก form_details ก่อน ถ้าไม่มีใช้ updated_at ตัด 10 ตัวแรก
            "approve_date": form_details.get("approved_date")
            or str(detail.get("updated_at") or "-")[:10],
            "title_th": form_details.get("thesis_title_th", "-"),   # ชื่อเรื่อง (ภาษาไทย)
            "title_en": form_details.get("thesis_title_en", "-"),   # ชื่อเรื่อง (ภาษาอังกฤษ)
            "chair": self._get_advisor_name(committee.get("chair_id"), advisors_list),
            "main_advisor": self._get_advisor_name(main_id, advisors_list),
            "co_advisor": self._get_advisor_name(co_id, advisors_list),
        }

        return {"success": True, "data": formatted_data}

    # ══════════════════════════════════════════════
    # Form 4: แบบขอหนังสือเชิญผู้ทรงคุณวุฒิ
    # ══════════════════════════════════════════════
    async def get_form4_detail(self, submission_id: str):
        """
        ดึงรายละเอียดฟอร์ม 4
        ข้อมูลที่ดึง: ข้อมูลนักศึกษา + หัวข้อวิทยานิพนธ์ + ข้อมูลผู้ทรงคุณวุฒิ
        """
        validation_error = self._validate_submission_id(submission_id)
        if validation_error:
            return validation_error

        data, error = await self.service.fetch_submission_detail(submission_id)

        if error:
            return {"success": False, "message": error, "data": None}

        detail = data.get("documentDetail", {})
        form_details = detail.get("form_details", {})
        expert_info = form_details.get("expert_info", {})   # ข้อมูลผู้ทรงคุณวุฒิ

        prefix = detail.get("prefix_th") or ""
        first = detail.get("first_name_th") or ""
        last = detail.get("last_name_th") or ""

        formatted_data = {
            "student_name": f"{prefix}{first} {last}".strip() or "ไม่ระบุ",
            "student_id": detail.get("student_id", "-"),
            "degree": detail.get("degree", "-"),
            "program_name": detail.get("program_name", "-"),
            "department_name": detail.get("department_name", "-"),
            "approve_date": form_details.get("approved_date", "-"),
            "title_th": form_details.get("thesis_title_th", "-"),
            "title_en": form_details.get("thesis_title_en", "-"),
            # ข้อมูลผู้ทรงคุณวุฒิ
            "expert_title": expert_info.get("title", "-"),          # คำนำหน้า/ยศ
            "expert_name": expert_info.get("firstname", "-"),       # ชื่อ
            "expert_surname": expert_info.get("lastname", "-"),     # นามสกุล
            "expert_org": expert_info.get("institution", "-"),      # สถาบัน/หน่วยงาน
            "expert_phone": expert_info.get("phone", "-"),          # เบอร์โทร
            "expert_email": expert_info.get("email", "-"),          # อีเมล
        }

        return {"success": True, "data": formatted_data}

    # ══════════════════════════════════════════════
    # Form 5: แบบขอหนังสือขออนุญาตเก็บรวบรวมข้อมูล
    # ══════════════════════════════════════════════
    async def get_form5_detail(self, submission_id: str):
        """
        ดึงรายละเอียดฟอร์ม 5
        ข้อมูลที่ดึง: ข้อมูลนักศึกษา + หัวข้อวิทยานิพนธ์ + วิธีการเก็บข้อมูล (Checkboxes)
        """
        validation_error = self._validate_submission_id(submission_id)
        if validation_error:
            return validation_error

        data, error = await self.service.fetch_submission_detail(submission_id)

        if error:
            return {"success": False, "message": error, "data": None}

        detail = data.get("documentDetail", {})
        form_details = detail.get("form_details", {})

        prefix = detail.get("prefix_th") or ""
        first = detail.get("first_name_th") or ""
        last = detail.get("last_name_th") or ""

        # ── จัดการ Checkbox วิธีการเก็บข้อมูล ──
        # ดึง list ของ collection_methods แล้วตรวจสอบว่ามีวิธีไหนบ้าง
        methods = form_details.get("collection_methods", [])
        methods_str = str(methods).lower()  # แปลงเป็น string ตัวเล็กเพื่อง่ายต่อการเช็ค

        # ตรวจสอบว่ามีวิธีการเก็บข้อมูลแต่ละประเภทหรือไม่
        is_questionnaire = "questionnaire" in methods_str or "แบบสอบถาม" in methods_str
        is_test = "test" in methods_str or "แบบทดสอบ" in methods_str
        is_teaching = (
            "teaching" in methods_str
            or "experiment" in methods_str
            or "ทดลองสอน" in methods_str
        )
        is_other = "other" in methods_str or "อื่นๆ" in methods_str

        # ถ้าเลือก "อื่นๆ" → ดึงรายละเอียดเพิ่มเติม
        other_text = form_details.get("other_detail", "") if is_other else ""

        formatted_data = {
            "student_name": f"{prefix}{first} {last}".strip() or "ไม่ระบุ",
            "student_id": detail.get("student_id", "-"),
            "degree": detail.get("degree", "-"),
            "program_name": detail.get("program_name", "-"),
            "department_name": detail.get("department_name", "-"),
            "approve_date": form_details.get("approved_date", "-"),
            "title_th": form_details.get("thesis_title_th", "-"),
            "title_en": form_details.get("thesis_title_en", "-"),
            # ค่า Checkbox (True/False) สำหรับแสดงเครื่องหมายถูกบนหน้าจอ
            "check_questionnaire": is_questionnaire,
            "check_test": is_test,
            "check_teaching": is_teaching,
            "check_other": is_other,
            "other_detail": other_text,
        }

        return {"success": True, "data": formatted_data}

    # ══════════════════════════════════════════════
    # Form 6: แต่งตั้งคณะกรรมการสอบวิทยานิพนธ์ขั้นสุดท้าย
    # ══════════════════════════════════════════════
    async def get_form6_detail(self, submission_id: str):
        """
        ดึงรายละเอียดฟอร์ม 6
        ข้อมูลที่ดึง: ข้อมูลผู้ยื่นคำร้อง + วิทยานิพนธ์ + คณะกรรมการสอบ + กรรมการสำรอง
        (ฟอร์มที่มีข้อมูลมากที่สุด)
        """
        validation_error = self._validate_submission_id(submission_id)
        if validation_error:
            return validation_error

        data, error = await self.service.fetch_submission_detail(submission_id)

        if error:
            return {"success": False, "message": error, "data": None}

        detail = data.get("documentDetail", {})
        advisors_list = data.get("advisors", [])
        form_details = detail.get("form_details", {})
        committee = form_details.get("committee", {})

        prefix = detail.get("prefix_th") or ""
        first = detail.get("first_name_th") or ""
        last = detail.get("last_name_th") or ""

        formatted_data = {
            # ข้อมูลผู้ยื่นคำร้อง
            "student_name": f"{prefix}{first} {last}".strip() or "ไม่ระบุ",
            "student_id": detail.get("student_id", "-"),
            "degree": detail.get("degree", "-"),
            "program_name": detail.get("program_name", "-"),
            "department_name": detail.get("department_name", "-"),
            "phone": detail.get("phone", "-"),
            "start_semester": str(form_details.get("entry_semester", "-")),  # ภาคเรียนที่เริ่ม
            "start_year": str(form_details.get("entry_year", "-")),         # ปีการศึกษา
            "address": form_details.get("current_address", "-"),            # ที่อยู่ปัจจุบัน
            "workplace": form_details.get("workplace", "-"),                # สถานที่ทำงาน
            # ข้อมูลวิทยานิพนธ์
            "thesis_th": form_details.get("thesis_title_th", "-"),
            "thesis_en": form_details.get("thesis_title_en", "-"),
            # อาจารย์ที่ปรึกษา
            "main_advisor": self._get_advisor_name(
                form_details.get("main_advisor_id"), advisors_list
            ),
            "co_advisor": self._get_advisor_name(
                form_details.get("co_advisor_id"), advisors_list
            ),
            # คณะกรรมการสอบ
            "chair": self._get_advisor_name(committee.get("chair_id"), advisors_list),
            "committee": self._get_advisor_name(
                committee.get("co_advisor2_id"), advisors_list
            ),
            "member5": self._get_advisor_name(
                committee.get("member5_id"), advisors_list
            ),
            # กรรมการสำรอง
            "reserve_ext": self._get_advisor_name(
                committee.get("reserve_external_id"), advisors_list
            ),
            "reserve_int": self._get_advisor_name(
                committee.get("reserve_internal_id"), advisors_list
            ),
        }

        return {"success": True, "data": formatted_data}

    # ══════════════════════════════════════════════
    # Exam Result: แบบฟอร์มยื่นผลการสอบ
    # ══════════════════════════════════════════════
    async def get_exam_result_detail(self, submission_id: str):
        """
        ดึงรายละเอียดผลสอบ
        ข้อมูลที่ดึง: ข้อมูลนักศึกษา + ข้อมูลผลสอบ + ไฟล์แนบ
        """
        validation_error = self._validate_submission_id(submission_id)
        if validation_error:
            return validation_error

        data, error = await self.service.fetch_submission_detail(submission_id)

        if error:
            return {"success": False, "message": error, "data": None}

        detail = data.get("documentDetail", {})
        form_details = detail.get("form_details", {})

        prefix = detail.get("prefix_th") or ""
        first = detail.get("first_name_th") or ""
        last = detail.get("last_name_th") or ""

        # ดึงผลสอบ: ลอง "result" ก่อน ถ้าไม่มีจึงใช้ "total_score"
        score = (
            form_details.get("result")
            if "result" in form_details
            else form_details.get("total_score", "-")
        )

        formatted_data = {
            "student_name": f"{prefix}{first} {last}".strip() or "ไม่ระบุ",
            "student_id": detail.get("student_id", "-"),
            "degree": detail.get("degree", "-"),
            "program_name": detail.get("program_name", "-"),
            "doc_type": detail.get("title", "แบบฟอร์มยื่นผลการสอบ"),    # ประเภทเอกสาร
            "exam_type": form_details.get("exam_type", "-"),            # ประเภทการสอบ
            "exam_date": form_details.get("exam_date", "-"),            # วันที่สอบ
            "result_score": str(score),                                 # ผลสอบ/คะแนน
            "files": form_details.get("files", []),                     # รายการไฟล์แนบ
        }

        return {"success": True, "data": formatted_data}
