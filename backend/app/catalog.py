from sqlalchemy.orm import Session

from .models import Subject, Topic


def ensure_default_catalog(db: Session) -> None:
    if db.query(Subject).count():
        return

    subjects = [
        Subject(name="Sun'iy intellekt", description="AI va NLP yo'nalishlari"),
        Subject(name="Ma'lumotlar bazasi", description="Relatsion modellar"),
        Subject(name="Kompyuter tarmoqlari", description="Tarmoq arxitekturasi"),
        Subject(name="Dasturlash asoslari", description="Algoritmlar va web"),
        Subject(name="Axborot xavfsizligi", description="Himoya usullari"),
    ]
    db.add_all(subjects)
    db.flush()

    db.add_all(
        [
            Topic(subject_id=subjects[0].id, title="NLP texnologiyalari", description="tabiiy tilni qayta ishlash, tokenizatsiya, tf-idf, cosine similarity", keywords="nlp, tokenizatsiya, tf-idf"),
            Topic(subject_id=subjects[0].id, title="Mashinali o'qitish", description="klassifikatsiya, regressiya, model, dataset", keywords="model, dataset"),
            Topic(subject_id=subjects[1].id, title="Ma'lumotlar bazasini loyihalash", description="jadval, normalizatsiya, ER diagramma", keywords="normalizatsiya, jadval"),
            Topic(subject_id=subjects[2].id, title="Tarmoq xavfsizligi", description="firewall, vpn, hujumlar, shifrlash", keywords="vpn, firewall"),
            Topic(subject_id=subjects[3].id, title="Web dasturlash", description="html, css, javascript, backend", keywords="html, javascript"),
            Topic(subject_id=subjects[3].id, title="Elektron ta'lim resurslari", description="raqamli materiallar, LMS, interaktiv ta'lim", keywords="lms, raqamli"),
            Topic(subject_id=subjects[4].id, title="Raqamli kutubxona tizimlari", description="metadata, katalog, qidiruv, elektron fond", keywords="metadata, katalog"),
        ]
    )
    db.commit()
