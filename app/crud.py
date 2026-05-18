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
        Subject(name="Dasturlash asoslari", description="Algoritm, funksiya va ma'lumot turlari"),
        Subject(name="Web dasturlash", description="HTML, CSS, JavaScript va web ilovalar"),
        Subject(name="Axborot xavfsizligi", description="Kriptografiya va himoya usullari"),
        Subject(name="Operatsion tizimlar", description="Jarayonlar, xotira va fayl tizimlari"),
        Subject(name="Ma'lumotlar tahlili", description="Statistika, vizualizatsiya va tahlil"),
    ]
    db.add_all(subjects)
    db.flush()
    db.add_all(
        [
            Topic(subject_id=subjects[0].id, title="NLP texnologiyalari", description="tokenizatsiya tf idf tabiiy tilni qayta ishlash", keywords="nlp tokenizatsiya tf idf"),
            Topic(subject_id=subjects[0].id, title="Mashinali o'rganish", description="klassifikatsiya regressiya model trening", keywords="machine learning klassifikatsiya regressiya"),
            Topic(subject_id=subjects[1].id, title="Normalizatsiya", description="jadval bog'lanish normal forma", keywords="jadval normalizatsiya"),
            Topic(subject_id=subjects[1].id, title="SQL so'rovlari", description="select join group by indeks", keywords="sql select join indeks"),
            Topic(subject_id=subjects[2].id, title="Tarmoq xavfsizligi", description="vpn firewall shifrlash", keywords="vpn firewall"),
            Topic(subject_id=subjects[2].id, title="TCP IP modeli", description="ip manzil protokol marshrutlash", keywords="tcp ip protokol marshrutlash"),
            Topic(subject_id=subjects[3].id, title="Algoritmlar", description="algoritm sikl shart operator murakkablik", keywords="algoritm sikl shart operator"),
            Topic(subject_id=subjects[3].id, title="Python asoslari", description="python funksiya ro'yxat lug'at modul", keywords="python funksiya ro'yxat lug'at"),
            Topic(subject_id=subjects[4].id, title="Frontend asoslari", description="html css javascript responsive sahifa", keywords="html css javascript frontend"),
            Topic(subject_id=subjects[4].id, title="Backend API", description="http rest api server marshrut", keywords="http rest api backend"),
            Topic(subject_id=subjects[5].id, title="Kriptografiya", description="shifrlash kalit hash autentifikatsiya", keywords="kriptografiya hash shifrlash"),
            Topic(subject_id=subjects[5].id, title="Kiberxavfsizlik", description="xavf zaiflik hujum himoya", keywords="xavfsizlik hujum himoya"),
            Topic(subject_id=subjects[6].id, title="Jarayonlar", description="process thread scheduling deadlock", keywords="process thread scheduling"),
            Topic(subject_id=subjects[6].id, title="Fayl tizimlari", description="fayl katalog disk inode", keywords="fayl katalog disk"),
            Topic(subject_id=subjects[7].id, title="Statistik tahlil", description="o'rtacha median dispersiya korrelyatsiya", keywords="statistika median dispersiya"),
            Topic(subject_id=subjects[7].id, title="Ma'lumotlarni vizualizatsiya", description="grafik diagramma dashboard tahlil", keywords="grafik diagramma dashboard"),
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
