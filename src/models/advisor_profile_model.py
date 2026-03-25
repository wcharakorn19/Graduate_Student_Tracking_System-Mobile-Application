# src/models/advisor_profile_model.py
from dataclasses import dataclass


@dataclass
class AdvisorProfileModel:
    user_id: str = "-"
    full_name: str = "-"
    role: str = "advisor"
    email: str = "-"
    phone: str = "-"
    academic_position: str = "-"
    advisor_type: str = "-"
    workplace: str = "-"
    approval_role: str = "-"
    program: str = "-"
