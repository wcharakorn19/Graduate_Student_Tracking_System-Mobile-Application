# src/controllers/form_controller.py
from services.form_service import FormService


class FormController:
    def __init__(self):
        self.service = FormService()

    # ฟังก์ชันกลาง: ตรวจสอบ submission_id ก่อนยิง API
    def _validate_submission_id(self, submission_id: str):
        """คืน error dict ถ้า submission_id ไม่ถูกต้อง, คืน None ถ้าผ่าน"""
        if not submission_id or not submission_id.strip():
            return {
                "success": False,
                "message": "รหัสเอกสารไม่ถูกต้อง (ว่างเปล่า)",
                "data": None,
            }

    # ฟังก์ชันกลาง: ค้นหาชื่ออาจารย์จาก ID
    def _get_advisor_name(self, adv_id, advisors_list):
        if not adv_id:
            return "-"
        for adv in advisors_list:
            if adv.get("advisor_id") == adv_id:
                return f"{adv.get('prefix_th')}{adv.get('first_name_th')} {adv.get('last_name_th')}"
        return f"รหัส {adv_id}"

    async def get_form1_detail(self, submission_id: str):
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

        req_main_id = detail.get("form_details", {}).get(
            "main_advisor_id"
        ) or detail.get("main_advisor_id")
        req_co_id = detail.get("form_details", {}).get("co_advisor_id") or detail.get(
            "co_advisor_id"
        )

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
            "main_advisor": self._get_advisor_name(req_main_id, advisors_list),
            "co_advisor": self._get_advisor_name(req_co_id, advisors_list),
        }

        return {"success": True, "data": formatted_data}

    async def get_form2_detail(self, submission_id: str):
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
            "chair": self._get_advisor_name(committee.get("chair_id"), advisors_list),
            "committee": self._get_advisor_name(
                committee.get("co_advisor2_id"), advisors_list
            ),
            "member5": self._get_advisor_name(
                committee.get("member5_id"), advisors_list
            ),
            "reserve_ext": self._get_advisor_name(
                committee.get("reserve_external_id"), advisors_list
            ),
            "reserve_int": self._get_advisor_name(
                committee.get("reserve_internal_id"), advisors_list
            ),
        }

        return {"success": True, "data": formatted_data}

    async def get_form3_detail(self, submission_id: str):
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
            "approve_date": form_details.get("approved_date")
            or str(detail.get("updated_at") or "-")[:10],
            "title_th": form_details.get("thesis_title_th", "-"),
            "title_en": form_details.get("thesis_title_en", "-"),
            "chair": self._get_advisor_name(committee.get("chair_id"), advisors_list),
            "main_advisor": self._get_advisor_name(main_id, advisors_list),
            "co_advisor": self._get_advisor_name(co_id, advisors_list),
        }

        return {"success": True, "data": formatted_data}

    async def get_form4_detail(self, submission_id: str):
        validation_error = self._validate_submission_id(submission_id)
        if validation_error:
            return validation_error

        data, error = await self.service.fetch_submission_detail(submission_id)

        if error:
            return {"success": False, "message": error, "data": None}

        detail = data.get("documentDetail", {})
        form_details = detail.get("form_details", {})
        expert_info = form_details.get("expert_info", {})

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
            "expert_title": expert_info.get("title", "-"),
            "expert_name": expert_info.get("firstname", "-"),
            "expert_surname": expert_info.get("lastname", "-"),
            "expert_org": expert_info.get("institution", "-"),
            "expert_phone": expert_info.get("phone", "-"),
            "expert_email": expert_info.get("email", "-"),
        }

        return {"success": True, "data": formatted_data}

    async def get_form5_detail(self, submission_id: str):
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

        methods = form_details.get("collection_methods", [])
        methods_str = str(methods).lower()

        is_questionnaire = "questionnaire" in methods_str or "แบบสอบถาม" in methods_str
        is_test = "test" in methods_str or "แบบทดสอบ" in methods_str
        is_teaching = (
            "teaching" in methods_str
            or "experiment" in methods_str
            or "ทดลองสอน" in methods_str
        )
        is_other = "other" in methods_str or "อื่นๆ" in methods_str

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
            "check_questionnaire": is_questionnaire,
            "check_test": is_test,
            "check_teaching": is_teaching,
            "check_other": is_other,
            "other_detail": other_text,
        }

        return {"success": True, "data": formatted_data}

    async def get_form6_detail(self, submission_id: str):
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
            "student_name": f"{prefix}{first} {last}".strip() or "ไม่ระบุ",
            "student_id": detail.get("student_id", "-"),
            "degree": detail.get("degree", "-"),
            "program_name": detail.get("program_name", "-"),
            "department_name": detail.get("department_name", "-"),
            "phone": detail.get("phone", "-"),
            "start_semester": str(form_details.get("entry_semester", "-")),
            "start_year": str(form_details.get("entry_year", "-")),
            "address": form_details.get("current_address", "-"),
            "workplace": form_details.get("workplace", "-"),
            "thesis_th": form_details.get("thesis_title_th", "-"),
            "thesis_en": form_details.get("thesis_title_en", "-"),
            "main_advisor": self._get_advisor_name(
                form_details.get("main_advisor_id"), advisors_list
            ),
            "co_advisor": self._get_advisor_name(
                form_details.get("co_advisor_id"), advisors_list
            ),
            "chair": self._get_advisor_name(committee.get("chair_id"), advisors_list),
            "committee": self._get_advisor_name(
                committee.get("co_advisor2_id"), advisors_list
            ),
            "member5": self._get_advisor_name(
                committee.get("member5_id"), advisors_list
            ),
            "reserve_ext": self._get_advisor_name(
                committee.get("reserve_external_id"), advisors_list
            ),
            "reserve_int": self._get_advisor_name(
                committee.get("reserve_internal_id"), advisors_list
            ),
        }

        return {"success": True, "data": formatted_data}

    async def get_exam_result_detail(self, submission_id: str):
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
            "doc_type": detail.get("title", "แบบฟอร์มยื่นผลการสอบ"),
            "exam_type": form_details.get("exam_type", "-"),
            "exam_date": form_details.get("exam_date", "-"),
            "result_score": str(score),
            "files": form_details.get("files", []),
        }

        return {"success": True, "data": formatted_data}
