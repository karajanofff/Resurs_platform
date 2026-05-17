from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class SubjectCreate(BaseModel):
    name: str
    description: str = ""
    teacher_id: Optional[int] = None


class SubjectOut(SubjectCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TopicCreate(BaseModel):
    subject_id: int
    title: str
    description: str = ""
    keywords: str = ""


class TopicOut(TopicCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ResourceOut(BaseModel):
    id: int
    title: str
    file_url: str
    file_type: str
    uploaded_by: int
    subject_id: int
    topic_id: int
    keywords: str
    similarity_score: float
    status: str
    is_approved: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SubjectScoreOut(BaseModel):
    subject_id: int
    subject_name: str
    similarity_score: float


class SectionMatchOut(BaseModel):
    section_title: str
    preview: str
    subject_name: str
    similarity_score: float


class AnalysisOut(BaseModel):
    resource_id: int
    similarity_score: float
    matched_keywords: list[str]
    recommendation: str
    result_status: str
    detected_subject: str
    subject_scores: list[SubjectScoreOut]
    section_matches: list[SectionMatchOut]


class StatisticsOut(BaseModel):
    subjects: int
    topics: int
    resources: int
    users: int
    matched: int
    partial: int
    unmatched: int
