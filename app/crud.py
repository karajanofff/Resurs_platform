from sqlalchemy.orm import Session

from .auth import hash_password
from .models import Resource, Subject, Topic, User


def seed_data(db: Session) -> None:
    users = [
        ("Admin", "admin@example.com", "admin123", "admin"),
        ("O'qituvchi", "teacher@example.com", "teacher123", "teacher"),
        ("Talaba", "student@example.com", "student123", "student"),
    ]
    for full_name, email, password, role in users:
        db.add(User(full_name=full_name, email=email, password_hash=hash_password(password), role=role))

    subjects = [
        Subject(name="Sun'iy intellekt", description="AI va tabiiy tilni qayta ishlash"),
        Subject(name="Ma'lumotlar bazasi", description="Relatsion ma'lumotlar bazasi"),
        Subject(name="Kompyuter tarmoqlari", description="Tarmoq va xavfsizlik"),
    ]
    db.add_all(subjects)
    db.flush()
    db.add_all(
        [
            Topic(subject_id=subjects[0].id, title="NLP texnologiyalari", description="tokenizatsiya tf idf tabiiy tilni qayta ishlash", keywords="nlp tokenizatsiya tf idf"),
            Topic(subject_id=subjects[1].id, title="Normalizatsiya", description="jadval bog'lanish normal forma", keywords="jadval normalizatsiya"),
            Topic(subject_id=subjects[2].id, title="Tarmoq xavfsizligi", description="vpn firewall shifrlash", keywords="vpn firewall"),
        ]
    )
    db.commit()


def dashboard_stats(db: Session) -> dict[str, int]:
    return {
        "subjects": db.query(Subject).count(),
        "topics": db.query(Topic).count(),
        "resources": db.query(Resource).count(),
        "matched": db.query(Resource).filter(Resource.status == "Mos").count(),
        "partial": db.query(Resource).filter(Resource.status == "Qisman mos").count(),
        "unmatched": db.query(Resource).filter(Resource.status == "Mos emas").count(),
    }
