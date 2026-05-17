from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(160), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(160), nullable=False)
    description = Column(Text, default="")
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    teacher = relationship("User", back_populates="subjects")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="subject")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    title = Column(String(180), nullable=False)
    description = Column(Text, default="")
    keywords = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    subject = relationship("Subject", back_populates="topics")
    resources = relationship("Resource", back_populates="topic")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(220), nullable=False)
    file_url = Column(String(255), nullable=False)
    file_type = Column(String(24), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    extracted_text = Column(Text, default="")
    keywords = Column(Text, default="")
    similarity_score = Column(Float, default=0)
    status = Column(String(40), default="Kutilmoqda")
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    subject = relationship("Subject", back_populates="resources")
    topic = relationship("Topic", back_populates="resources")
    analysis = relationship("AnalysisResult", back_populates="resource", uselist=False, cascade="all, delete-orphan")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    similarity_score = Column(Float, nullable=False)
    matched_keywords = Column(Text, default="")
    recommendation = Column(Text, nullable=False)
    result_status = Column(String(40), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resource = relationship("Resource", back_populates="analysis")
