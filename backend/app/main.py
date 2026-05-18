from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine, get_db
from .models import AnalysisResult, Resource, Subject, Topic, User
from .nlp import calculate_similarity, extract_keywords, extract_text_from_file, generate_recommendation, split_text_into_sections
from .schemas import (
    AnalysisOut,
    LoginRequest,
    ResourceOut,
    SectionMatchOut,
    StatisticsOut,
    SubjectCreate,
    SubjectOut,
    SubjectScoreOut,
    TokenResponse,
    TopicCreate,
    TopicOut,
    TeacherRegisterRequest,
    UserCreate,
    UserOut,
)
from .security import create_access_token, decode_access_token, hash_password, verify_password
from .bootstrap import ensure_bootstrap_admin
from .catalog import ensure_default_catalog
from .settings import settings


settings.upload_path.mkdir(parents=True, exist_ok=True)
app = FastAPI(title="SmartKutubxona AI API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[*settings.frontend_urls, "http://localhost:3000"],
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1):\d+$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
app.mount("/uploads", StaticFiles(directory=settings.upload_path), name="uploads")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/version")
def version() -> dict[str, str]:
    return {"version": "2026-05-17-public-analysis-v2"}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "SmartKutubxona AI API",
        "status": "ok",
        "docs": "/docs",
        "health": "/healthz",
    }


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    db = SessionLocal()
    try:
        ensure_bootstrap_admin(db)
        ensure_default_catalog(db)
    finally:
        db.close()


def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    email = decode_access_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Avtorizatsiya talab qilinadi")
    return user


@app.post("/api/auth/register", response_model=UserOut)
def register(payload: TeacherRegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Bu email allaqachon mavjud")
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role="teacher",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/api/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Email yoki parol noto'g'ri")
    if payload.role and payload.role != user.role:
        raise HTTPException(403, "Tanlangan rol ushbu hisobga mos emas")
    return TokenResponse(access_token=create_access_token(user.email), user=user)


@app.get("/api/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user


@app.get("/api/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(current_user)):
    return db.query(User).all()


@app.post("/api/users", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _: User = Depends(current_user)):
    if payload.role not in {"admin", "teacher"}:
        raise HTTPException(400, "Rol noto'g'ri")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Bu email allaqachon mavjud")
    user = User(**payload.model_dump(exclude={"password"}), password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/api/subjects", response_model=list[SubjectOut])
def list_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()


@app.post("/api/subjects", response_model=SubjectOut)
def create_subject(payload: SubjectCreate, db: Session = Depends(get_db), _: User = Depends(current_user)):
    subject = Subject(**payload.model_dump())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@app.put("/api/subjects/{subject_id}", response_model=SubjectOut)
def update_subject(subject_id: int, payload: SubjectCreate, db: Session = Depends(get_db), _: User = Depends(current_user)):
    subject = db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(404, "Fan topilmadi")
    for key, value in payload.model_dump().items():
        setattr(subject, key, value)
    db.commit()
    db.refresh(subject)
    return subject


@app.delete("/api/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    subject = db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(404, "Fan topilmadi")
    db.delete(subject)
    db.commit()
    return {"ok": True}


@app.get("/api/topics", response_model=list[TopicOut])
def list_topics(db: Session = Depends(get_db)):
    return db.query(Topic).all()


@app.post("/api/topics", response_model=TopicOut)
def create_topic(payload: TopicCreate, db: Session = Depends(get_db), _: User = Depends(current_user)):
    topic = Topic(**payload.model_dump())
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


@app.put("/api/topics/{topic_id}", response_model=TopicOut)
def update_topic(topic_id: int, payload: TopicCreate, db: Session = Depends(get_db), _: User = Depends(current_user)):
    topic = db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(404, "Mavzu topilmadi")
    for key, value in payload.model_dump().items():
        setattr(topic, key, value)
    db.commit()
    db.refresh(topic)
    return topic


@app.delete("/api/topics/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    topic = db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(404, "Mavzu topilmadi")
    db.delete(topic)
    db.commit()
    return {"ok": True}


@app.post("/api/resources/upload", response_model=ResourceOut)
async def upload_resource(
    title: str = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".docx", ".pptx", ".txt"}:
        raise HTTPException(400, "Faqat PDF, DOCX, PPTX yoki TXT fayl yuklang")
    destination = settings.upload_path / f"{Path(file.filename or 'resource').stem}-{user.id}{suffix}"
    destination.write_bytes(await file.read())
    try:
        text = extract_text_from_file(destination)
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(400, f"{suffix.upper().replace('.', '')} fayl matnini o'qib bo'lmadi") from exc
    if not text.strip():
        destination.unlink(missing_ok=True)
        raise HTTPException(400, "Fayldan matn topilmadi")
    keywords = extract_keywords(text)
    subjects = db.query(Subject).all()
    if not subjects:
        raise HTTPException(400, "Tahlil uchun kamida bitta fan mavjud bo'lishi kerak")
    topics = db.query(Topic).all()
    subject_profiles = {
        subject.id: " ".join(
            [subject.name, subject.description]
            + [f"{topic.title} {topic.description} {topic.keywords}" for topic in topics if topic.subject_id == subject.id]
        )
        for subject in subjects
    }
    best_subject = max(subjects, key=lambda subject: calculate_similarity(text, subject_profiles[subject.id]))
    related_topics = [topic for topic in topics if topic.subject_id == best_subject.id]
    best_topic = max(related_topics, key=lambda topic: calculate_similarity(text, f"{topic.title} {topic.description} {topic.keywords}")) if related_topics else None
    score = calculate_similarity(text, subject_profiles[best_subject.id])
    result_status, _ = generate_recommendation(score, keywords)
    resource = Resource(
        title=title,
        file_url=f"/uploads/{destination.name}",
        file_type=suffix.replace(".", "").upper(),
        uploaded_by=user.id,
        subject_id=best_subject.id,
        topic_id=best_topic.id if best_topic else topics[0].id,
        extracted_text=text,
        keywords=", ".join(keywords),
        similarity_score=score,
        status=result_status,
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


@app.get("/api/resources", response_model=list[ResourceOut])
def list_resources(db: Session = Depends(get_db)):
    return db.query(Resource).order_by(Resource.created_at.desc()).all()


@app.get("/api/resources/{resource_id}", response_model=ResourceOut)
def resource_detail(resource_id: int, db: Session = Depends(get_db)):
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(404, "Resurs topilmadi")
    return resource


@app.put("/api/resources/{resource_id}/approve", response_model=ResourceOut)
def approve_resource(resource_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(404, "Resurs topilmadi")
    resource.is_approved = True
    db.commit()
    db.refresh(resource)
    return resource


@app.delete("/api/resources/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(404, "Resurs topilmadi")
    if resource.analysis:
        db.delete(resource.analysis)
    db.delete(resource)
    db.commit()
    return {"ok": True}


@app.post("/api/analyze", response_model=AnalysisOut)
def analyze(resource_id: int = Form(...), db: Session = Depends(get_db), _: User = Depends(current_user)):
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(404, "Resurs topilmadi")
    subjects = db.query(Subject).all()
    topics = db.query(Topic).all()
    if not subjects or not topics:
        raise HTTPException(400, "Tahlil uchun fan va mavzular mavjud bo'lishi kerak")
    subject_profiles = {
        subject.id: " ".join(
            [subject.name, subject.description]
            + [f"{topic.title} {topic.description} {topic.keywords}" for topic in topics if topic.subject_id == subject.id]
        )
        for subject in subjects
    }
    subject_scores = sorted(
        [
            SubjectScoreOut(
                subject_id=subject.id,
                subject_name=subject.name,
                similarity_score=calculate_similarity(resource.extracted_text, subject_profiles[subject.id]),
            )
            for subject in subjects
        ],
        key=lambda item: item.similarity_score,
        reverse=True,
    )
    detected_subject = subject_scores[0]
    score = detected_subject.similarity_score
    keywords = extract_keywords(resource.extracted_text)
    result_status, recommendation = generate_recommendation(score, keywords)
    resource.similarity_score = score
    resource.keywords = ", ".join(keywords)
    resource.status = result_status
    related_topics = [topic for topic in topics if topic.subject_id == detected_subject.subject_id]
    best_topic = max(related_topics, key=lambda topic: calculate_similarity(resource.extracted_text, f"{topic.title} {topic.description} {topic.keywords}")) if related_topics else db.get(Topic, resource.topic_id)
    resource.subject_id = detected_subject.subject_id
    if best_topic:
        resource.topic_id = best_topic.id
    analysis = resource.analysis or AnalysisResult(resource_id=resource.id, topic_id=resource.topic_id)
    analysis.similarity_score = score
    analysis.matched_keywords = ", ".join(keywords)
    analysis.recommendation = recommendation
    analysis.result_status = result_status
    db.add(analysis)
    db.commit()
    section_matches = []
    for index, section in enumerate(split_text_into_sections(resource.extracted_text), start=1):
        section_subject = max(
            subject_scores,
            key=lambda item: calculate_similarity(section, subject_profiles[item.subject_id]),
        )
        section_matches.append(
            SectionMatchOut(
                section_title=f"{index}-bo'lim",
                preview=section[:180],
                subject_name=section_subject.subject_name,
                similarity_score=calculate_similarity(section, subject_profiles[section_subject.subject_id]),
            )
        )
    return AnalysisOut(
        resource_id=resource.id,
        similarity_score=score,
        matched_keywords=keywords,
        recommendation=recommendation,
        result_status=result_status,
        detected_subject=detected_subject.subject_name,
        subject_scores=subject_scores,
        section_matches=section_matches,
    )


@app.get("/api/statistics", response_model=StatisticsOut)
def statistics(db: Session = Depends(get_db)):
    return StatisticsOut(
        subjects=db.query(Subject).count(),
        topics=db.query(Topic).count(),
        resources=db.query(Resource).count(),
        users=db.query(User).count(),
        matched=db.query(Resource).filter(Resource.status == "Mos").count(),
        partial=db.query(Resource).filter(Resource.status == "Qisman mos").count(),
        unmatched=db.query(Resource).filter(Resource.status == "Mos emas").count(),
    )
    SectionMatchOut,
    SubjectScoreOut,
