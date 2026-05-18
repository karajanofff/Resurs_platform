from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(160), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False)


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(160), nullable=False)
    description = Column(Text, default="")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    title = Column(String(180), nullable=False)
    description = Column(Text, default="")
    keywords = Column(Text, default="")
    subject = relationship("Subject", back_populates="topics")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    title = Column(String(220), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_type = Column(String(24), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    extracted_text = Column(Text, default="")
    keywords = Column(Text, default="")
    similarity_score = Column(Float, default=0)
    status = Column(String(40), default="Kutilmoqda")
    recommendation = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
