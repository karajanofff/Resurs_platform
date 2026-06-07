import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


STOP_WORDS = {
    "va",
    "yoki",
    "uchun",
    "bilan",
    "ham",
    "bu",
    "shu",
    "ning",
    "dan",
    "ga",
    "da",
    "bir",
}

SUBJECT_ANCHORS = {
    "suniy intellekt": [
        "suniy",
        "intellekt",
        "ai",
        "nlp",
        "kompyuter",
        "inson",
        "mashina",
        "neyron",
        "algoritm",
        "model",
        "tabiiy",
        "til",
        "token",
        "klassifikatsiya",
        "regressiya",
        "matn",
        "tahlil",
        "organish",
        "trening",
    ],
    "malumotlar bazasi": ["malumot", "bazasi", "sql", "jadval", "normalizatsiya", "join", "indeks", "relatsion"],
    "kompyuter tarmoqlari": ["tarmoq", "tcp", "protokol", "marshrutlash", "vpn", "firewall", "ip", "xavfsizlik"],
    "dasturlash asoslari": ["algoritm", "sikl", "shart", "operator", "funksiya", "python", "royxat", "lugat"],
    "web dasturlash": ["html", "css", "javascript", "frontend", "backend", "rest", "api", "http", "sahifa"],
    "axborot xavfsizligi": ["kriptografiya", "shifrlash", "hash", "autentifikatsiya", "xavfsizlik", "hujum", "himoya"],
    "operatsion tizimlar": ["process", "thread", "scheduling", "fayl", "katalog", "disk", "inode", "jarayon", "xotira"],
    "malumotlar tahlili": ["statistika", "vizualizatsiya", "tahlil", "grafik", "diagramma", "dashboard", "median", "dispersiya"],
}


def normalize_uzbek(text: str) -> str:
    lowered = text.lower()
    for src, dst in (("o'", "o"), ("g'", "g")):
        lowered = lowered.replace(src, dst)
    return lowered.replace("'", "")


def clean_text(text: str) -> str:
    normalized = re.sub(r"[^a-zA-Z\u0400-\u04ff\s]", " ", normalize_uzbek(text))
    return " ".join(word for word in normalized.split() if len(word) > 2 and word not in STOP_WORDS)


def subject_key(subject_name: str) -> str:
    return clean_text(subject_name)


def split_terms(text: str) -> list[str]:
    return clean_text(text).split()


def term_found(term: str, words: list[str]) -> bool:
    if not term:
        return False
    if term in words:
        return True
    if len(term) <= 2:
        return False
    for word in words:
        if len(word) <= 2:
            continue
        if word.startswith(term) or term.startswith(word[: min(4, len(word))]):
            return True
        if len(term) >= 4 and term in word:
            return True
    return False


def extract_keywords(text: str, top_n: int = 15) -> list[str]:
    cleaned = clean_text(text)
    if not cleaned:
        return []
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([cleaned])
    terms = vectorizer.get_feature_names_out()
    scores = matrix.toarray()[0]
    ranked = sorted(zip(terms, scores), key=lambda item: item[1], reverse=True)
    return [term for term, score in ranked[:top_n] if score > 0]


def keyword_terms(topic_keywords: str) -> list[str]:
    terms: list[str] = []
    for part in re.split(r"[,;\s]+", topic_keywords):
        cleaned = clean_text(part)
        if cleaned:
            terms.extend(cleaned.split())
    return list(dict.fromkeys(terms))


def keyword_recall(resource_text: str, topic_keywords: str) -> float:
    terms = keyword_terms(topic_keywords)
    if not terms:
        return 0.0
    words = split_terms(resource_text)
    matched = sum(1 for term in terms if term_found(term, words))
    return matched / len(terms)


def subject_relevance(resource_text: str, subject_name: str, subject_description: str = "") -> float:
    words = split_terms(resource_text)
    anchors = SUBJECT_ANCHORS.get(subject_key(subject_name), split_terms(f"{subject_name} {subject_description}"))
    if not anchors:
        return 0.0
    matched = sum(1 for anchor in anchors if term_found(anchor, words))
    ratio = matched / len(anchors)
    if matched >= 4:
        return min(1.0, 0.72 + ratio * 0.28)
    if matched >= 3:
        return min(1.0, 0.70 + ratio * 0.22)
    if matched == 2:
        return 0.42
    if matched == 1:
        return 0.18
    return 0.0


def _cosine_tfidf(text_a: str, text_b: str) -> float:
    if not text_a or not text_b:
        return 0.0
    matrix = TfidfVectorizer(ngram_range=(1, 2)).fit_transform([text_a, text_b])
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])


def calculate_similarity(
    resource_text: str,
    topic_text: str,
    *,
    topic_keywords: str = "",
    subject_name: str = "",
    subject_description: str = "",
) -> float:
    resource_clean = clean_text(resource_text)
    topic_clean = clean_text(topic_text)
    if not resource_clean or not topic_clean:
        return 0.0

    keyword_score = keyword_recall(resource_text, topic_keywords)
    subject_score = subject_relevance(resource_text, subject_name, subject_description)
    tfidf_full = _cosine_tfidf(resource_clean, topic_clean)
    keyword_profile = clean_text(" ".join(extract_keywords(resource_text, top_n=30)))
    tfidf_profile = _cosine_tfidf(keyword_profile, topic_clean) if keyword_profile else 0.0
    tfidf_score = max(tfidf_full, tfidf_profile)

    return min(
        1.0,
        max(
            subject_score,
            0.55 * subject_score + 0.35 * keyword_score + 0.10 * tfidf_score,
            0.45 * keyword_score + 0.45 * subject_score + 0.10 * tfidf_score,
            keyword_score * 0.65 + tfidf_score * 0.35,
        ),
    )


def analyze_resource(
    resource_text: str,
    topic_title: str,
    topic_description: str,
    topic_keywords: str,
    subject_name: str = "",
    subject_description: str = "",
) -> dict:
    topic_text = " ".join(
        part
        for part in [subject_name, subject_description, topic_title, topic_description, topic_keywords]
        if part
    )
    score = round(
        calculate_similarity(
            resource_text,
            topic_text,
            topic_keywords=topic_keywords,
            subject_name=subject_name,
            subject_description=subject_description,
        )
        * 100,
        2,
    )
    if score >= 70:
        status = "Mos"
        recommendation = "Ushbu ta'lim resursi tanlangan fan mavzusiga yuqori darajada mos keladi."
    elif score >= 40:
        status = "Qisman mos"
        recommendation = "Ushbu resurs mavzuga qisman mos, lekin ayrim qismlari mavzudan chetga chiqishi mumkin."
    else:
        status = "Mos emas"
        recommendation = "Ushbu resurs tanlangan fan mavzusiga yetarli darajada mos emas."
    return {
        "similarity_score": score,
        "keywords": extract_keywords(resource_text),
        "status": status,
        "recommendation": recommendation,
    }


def classify_resource(resource_text: str, topics: list[dict]) -> list[dict]:
    predictions = []
    for topic in topics:
        analysis = analyze_resource(
            resource_text,
            topic["title"],
            topic["description"],
            topic["keywords"],
            subject_name=topic.get("subject_name", ""),
            subject_description=topic.get("subject_description", ""),
        )
        predictions.append(
            {
                "subject_id": topic["subject_id"],
                "subject_name": topic["subject_name"],
                "topic_id": topic["topic_id"],
                "topic_title": topic["title"],
                **analysis,
            }
        )

    best_by_subject = {}
    for item in predictions:
        current = best_by_subject.get(item["subject_id"])
        if current is None or item["similarity_score"] > current["similarity_score"]:
            best_by_subject[item["subject_id"]] = item
    return sorted(best_by_subject.values(), key=lambda item: item["similarity_score"], reverse=True)
