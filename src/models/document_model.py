# src/models/document_model.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class ActivityModel:
    title: str
    status: str
    name: str = ""
    form_type: str = "form1"
    submission_id: str = ""

@dataclass
class CurrentDocumentModel:
    doc_name: str
    status_label: str
    status_text: str

@dataclass
class StudentDashboardModel:
    user_name: str
    current_doc: CurrentDocumentModel
    activities: List[ActivityModel] = field(default_factory=list)

@dataclass
class StudentSummaryModel:
    name: str
    doc_status: str
    student_id: str = ""

@dataclass
class AdvisorDashboardModel:
    student_count: int
    students: List[StudentSummaryModel] = field(default_factory=list)
    activities: List[ActivityModel] = field(default_factory=list)
