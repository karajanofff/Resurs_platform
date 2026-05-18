from sqlalchemy.orm import Session

from .auth import hash_password
from .models import Resource, Subject, Topic, User


def seed_initial_data(db: Session) -> None:
    users = [
        ("Admin", "admin@example.com", "admin123", "admin"),
        ("O'qituvchi", "teacher@example.com", "teacher123", "teacher"),
        ("Talaba", "student@example.com", "student123", "student"),
    ]
    for full_name, email, password, role in users:
        if not db.query(User).filter(User.email == email).first():
            db.add(User(full_name=full_name, email=email, password_hash=hash_password(password), role=role))
    if not db.query(Subject).count():
        subjects = [
            Subject(name="Sun'iy intellekt", description="AI va NLP yo'nalishlari"),
            Subject(name="Ma'lumotlar bazasi", description="Relatsion modellar"),
            Subject(name="Kompyuter tarmoqlari", description="Tarmoq arxitekturasi"),
        ]
        db.add_all(subjects)
        db.flush()
        db.add_all(
            [
                Topic(subject_id=subjects[0].id, title="NLP texnologiyalari", description="tabiiy tilni qayta ishlash, tokenizatsiya, tf-idf", keywords="nlp, tokenizatsiya, tf-idf"),
                Topic(subject_id=subjects[1].id, title="Normalizatsiya", description="jadval, bog'lanish, ER model", keywords="jadval, normalizatsiya"),
                Topic(subject_id=subjects[2].id, title="Tarmoq xavfsizligi", description="firewall, vpn, shifrlash", keywords="vpn, firewall"),
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
