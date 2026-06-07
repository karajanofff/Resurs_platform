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


def normalize_uzbek(text: str) -> str:
    lowered = text.lower()
    for src, dst in (("o'", "o"), ("g'", "g")):
        lowered = lowered.replace(src, dst)
    return lowered.replace("'", "")


def clean_text(text: str) -> str:
    normalized = re.sub(r"[^a-zA-Z\u0400-\u04ff\s]", " ", normalize_uzbek(text))
    return " ".join(word for word in normalized.split() if len(word) > 2 and word not in STOP_WORDS)


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


def _cosine_tfidf(text_a: str, text_b: str) -> float:
    if not text_a or not text_b:
        return 0.0
    matrix = TfidfVectorizer(ngram_range=(1, 2)).fit_transform([text_a, text_b])
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])


def calculate_similarity(resource_text: str, topic_text: str) -> float:
    resource_clean = clean_text(resource_text)
    topic_clean = clean_text(topic_text)
    if not resource_clean or not topic_clean:
        return 0.0
    full_score = _cosine_tfidf(resource_clean, topic_clean)
    keyword_text = clean_text(" ".join(extract_keywords(resource_text, top_n=25)))
    keyword_score = _cosine_tfidf(keyword_text, topic_clean) if keyword_text else 0.0
    return max(full_score, keyword_score)


def build_topic_text(topic: dict) -> str:
    return " ".join(
        part
        for part in [
            topic.get("subject_name", ""),
            topic.get("subject_description", ""),
            topic["title"],
            topic["description"],
            topic["keywords"],
        ]
        if part
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
    score = round(calculate_similarity(resource_text, topic_text) * 100, 2)
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
