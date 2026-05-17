from sqlalchemy.orm import Session

from .models import AnalysisResult, Resource, Subject, Topic, User
from .security import hash_password


def seed_demo_data(db: Session) -> None:
    if db.query(User).count():
        return

    admin = User(full_name="Platforma administratori", email="admin@example.com", password_hash=hash_password("admin123"), role="admin")
    teacher = User(full_name="Dilshod Karimov", email="teacher@example.com", password_hash=hash_password("teacher123"), role="teacher")
    db.add_all([admin, teacher])
    db.flush()

    subjects = [
        Subject(name="Sun'iy intellekt", description="AI va NLP yo'nalishlari", teacher_id=teacher.id),
        Subject(name="Ma'lumotlar bazasi", description="Relatsion modellar", teacher_id=teacher.id),
        Subject(name="Kompyuter tarmoqlari", description="Tarmoq arxitekturasi", teacher_id=teacher.id),
        Subject(name="Dasturlash asoslari", description="Algoritmlar va web", teacher_id=teacher.id),
        Subject(name="Axborot xavfsizligi", description="Himoya usullari", teacher_id=teacher.id),
    ]
    db.add_all(subjects)
    db.flush()

    topics = [
        Topic(subject_id=subjects[0].id, title="NLP texnologiyalari", description="tabiiy tilni qayta ishlash, tokenizatsiya, tf-idf, cosine similarity", keywords="nlp, tokenizatsiya, tf-idf"),
        Topic(subject_id=subjects[0].id, title="Mashinali o'qitish", description="klassifikatsiya, regressiya, model, dataset", keywords="model, dataset"),
        Topic(subject_id=subjects[1].id, title="Ma'lumotlar bazasini loyihalash", description="jadval, normalizatsiya, ER diagramma", keywords="normalizatsiya, jadval"),
        Topic(subject_id=subjects[2].id, title="Tarmoq xavfsizligi", description="firewall, vpn, hujumlar, shifrlash", keywords="vpn, firewall"),
        Topic(subject_id=subjects[3].id, title="Web dasturlash", description="html, css, javascript, backend", keywords="html, javascript"),
        Topic(subject_id=subjects[3].id, title="Elektron ta'lim resurslari", description="raqamli materiallar, LMS, interaktiv ta'lim", keywords="lms, raqamli"),
        Topic(subject_id=subjects[4].id, title="Raqamli kutubxona tizimlari", description="metadata, katalog, qidiruv, elektron fond", keywords="metadata, katalog"),
    ]
    db.add_all(topics)
    db.flush()

    samples = [
        ("NLP amaliyoti", topics[0], 88, "Mos"),
        ("Web interfeys asoslari", topics[4], 67, "Qisman mos"),
        ("Tarmoq hujumlari", topics[3], 34, "Mos emas"),
    ]
    for title, topic, score, status in samples:
        resource = Resource(
            title=title,
            file_url=f"/uploads/{title.lower().replace(' ', '-')}.pdf",
            file_type="PDF",
            uploaded_by=teacher.id,
            subject_id=topic.subject_id,
            topic_id=topic.id,
            extracted_text=topic.description,
            keywords=topic.keywords,
            similarity_score=score,
            status=status,
            is_approved=status != "Mos emas",
        )
        db.add(resource)
        db.flush()
        db.add(
            AnalysisResult(
                resource_id=resource.id,
                topic_id=topic.id,
                similarity_score=score,
                matched_keywords=topic.keywords,
                recommendation="Demo tahlil natijasi",
                result_status=status,
            )
        )
    db.commit()
