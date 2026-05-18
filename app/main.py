import os
from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .auth import create_token, decode_token, verify_password
from .crud import dashboard_stats, seed_data
from .database import Base, SessionLocal, engine, get_db
from .file_parser import extract_text_from_file
from .models import Resource, Subject, Topic, User
from .nlp import analyze_resource


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="SmartKutubxona AI")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.on_event("startup")
def startup() -> None:
    if os.getenv("RESET_DB_ON_START", "false").lower() == "true":
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(User).count():
            seed_data(db)
    finally:
        db.close()


def get_user(request: Request, db: Session) -> User | None:
    token = request.cookies.get("access_token")
    email = decode_token(token) if token else None
    return db.query(User).filter(User.email == email).first() if email else None


def require_user(request: Request, db: Session) -> User | RedirectResponse:
    return get_user(request, db) or RedirectResponse("/login", status_code=303)


def context(request: Request, user: User | None = None, **extra):
    return {"request": request, "user": user, **extra}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", context(request))


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", context(request))


@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse("login.html", context(request, error="Email yoki parol noto'g'ri"), status_code=401)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("access_token", create_token(user.email), httponly=True, samesite="lax")
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse):
        return user
    return templates.TemplateResponse("dashboard.html", context(request, user, stats=dashboard_stats(db)))


@app.get("/subjects", response_class=HTMLResponse)
def subjects_page(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse) or user.role != "admin":
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("subjects.html", context(request, user, subjects=db.query(Subject).all()))


@app.post("/subjects")
def create_subject(request: Request, name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse) or user.role != "admin":
        return RedirectResponse("/login", status_code=303)
    db.add(Subject(name=name, description=description))
    db.commit()
    return RedirectResponse("/subjects", status_code=303)


@app.get("/topics", response_class=HTMLResponse)
def topics_page(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse) or user.role != "admin":
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(
        "topics.html",
        context(request, user, subjects=db.query(Subject).all(), topics=db.query(Topic).all()),
    )


@app.post("/topics")
def create_topic(
    request: Request,
    subject_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(""),
    keywords: str = Form(""),
    db: Session = Depends(get_db),
):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse) or user.role != "admin":
        return RedirectResponse("/login", status_code=303)
    db.add(Topic(subject_id=subject_id, title=title, description=description, keywords=keywords))
    db.commit()
    return RedirectResponse("/topics", status_code=303)


@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse) or user.role not in {"admin", "teacher"}:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(
        "upload.html",
        context(request, user, subjects=db.query(Subject).all(), topics=db.query(Topic).all()),
    )


@app.post("/upload")
def upload_resource(
    request: Request,
    title: str = Form(...),
    subject_id: int = Form(...),
    topic_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse) or user.role not in {"admin", "teacher"}:
        return RedirectResponse("/login", status_code=303)
    topic = db.get(Topic, topic_id)
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".docx", ".pptx", ".txt"} or not topic or topic.subject_id != subject_id:
        return templates.TemplateResponse(
            "upload.html",
            context(request, user, subjects=db.query(Subject).all(), topics=db.query(Topic).all(), error="Fayl turi yoki mavzu noto'g'ri"),
            status_code=400,
        )
    safe_name = f"{Path(file.filename or 'resource').stem}-{uuid4().hex[:10]}{suffix}"
    destination = UPLOAD_DIR / safe_name
    with destination.open("wb") as buffer:
        copyfileobj(file.file, buffer)
    try:
        extracted_text = extract_text_from_file(destination)
    except Exception:
        destination.unlink(missing_ok=True)
        return templates.TemplateResponse(
            "upload.html",
            context(request, user, subjects=db.query(Subject).all(), topics=db.query(Topic).all(), error="Fayldan matn ajratib bo'lmadi"),
            status_code=400,
        )
    analysis = analyze_resource(extracted_text, topic.title, topic.description, topic.keywords)
    resource = Resource(
        title=title,
        file_path=safe_name,
        file_type=suffix[1:].upper(),
        uploaded_by=user.id,
        subject_id=subject_id,
        topic_id=topic_id,
        extracted_text=extracted_text,
        keywords=", ".join(analysis["keywords"]),
        similarity_score=analysis["similarity_score"],
        status=analysis["status"],
        recommendation=analysis["recommendation"],
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return RedirectResponse(f"/result/{resource.id}", status_code=303)


@app.get("/result/{resource_id}", response_class=HTMLResponse)
def result_page(resource_id: int, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse):
        return user
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resurs topilmadi")
    return templates.TemplateResponse(
        "result.html",
        context(request, user, resource=resource, subject=db.get(Subject, resource.subject_id), topic=db.get(Topic, resource.topic_id)),
    )


@app.get("/resources", response_class=HTMLResponse)
def resources_page(
    request: Request,
    subject_id: int | None = None,
    topic_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse):
        return user
    query = db.query(Resource)
    if subject_id:
        query = query.filter(Resource.subject_id == subject_id)
    if topic_id:
        query = query.filter(Resource.topic_id == topic_id)
    if status:
        query = query.filter(Resource.status == status)
    return templates.TemplateResponse(
        "resources.html",
        context(
            request,
            user,
            resources=query.order_by(Resource.created_at.desc()).all(),
            subjects=db.query(Subject).all(),
            topics=db.query(Topic).all(),
        ),
    )


@app.get("/results", response_class=HTMLResponse)
def results_page(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse) or user.role != "admin":
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("results.html", context(request, user, resources=db.query(Resource).all()))


@app.get("/users", response_class=HTMLResponse)
def users_page(request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse) or user.role != "admin":
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("users.html", context(request, user, users=db.query(User).all()))


@app.get("/download/{resource_id}")
def download(resource_id: int, request: Request, db: Session = Depends(get_db)):
    user = require_user(request, db)
    if isinstance(user, RedirectResponse):
        return user
    resource = db.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resurs topilmadi")
    return FileResponse(UPLOAD_DIR / resource.file_path, filename=resource.file_path)
