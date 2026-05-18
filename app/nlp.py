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
    "the",
    "and",
    "for",
    "with",
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\u0400-\u04ff\s]", " ", text)
    words = [word for word in text.split() if len(word) > 2 and word not in STOP_WORDS]
    return " ".join(words)


def extract_keywords(text: str, top_n: int = 15) -> list[str]:
    cleaned = clean_text(text)
    if not cleaned:
        return []
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([cleaned])
    scores = matrix.toarray()[0]
    names = vectorizer.get_feature_names_out()
    ranked = sorted(zip(names, scores), key=lambda item: item[1], reverse=True)
    return [name for name, score in ranked[:top_n] if score > 0]


def calculate_similarity(resource_text: str, topic_text: str) -> float:
    cleaned_resource = clean_text(resource_text)
    cleaned_topic = clean_text(topic_text)
    if not cleaned_resource or not cleaned_topic:
        return 0.0
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([cleaned_resource, cleaned_topic])
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])


def analyze_resource(resource_text: str, topic_title: str, topic_description: str, topic_keywords: str) -> dict:
    topic_text = " ".join([topic_title, topic_description, topic_keywords])
    score_percent = round(calculate_similarity(resource_text, topic_text) * 100, 2)
    keywords = extract_keywords(resource_text)
    if score_percent >= 70:
        status = "Mos"
        recommendation = "Ushbu ta'lim resursi tanlangan fan mavzusiga yuqori darajada mos keladi."
    elif score_percent >= 40:
        status = "Qisman mos"
        recommendation = "Ushbu resurs mavzuga qisman mos, lekin ayrim qismlari mavzudan chetga chiqishi mumkin."
    else:
        status = "Mos emas"
        recommendation = "Ushbu resurs tanlangan fan mavzusiga yetarli darajada mos emas."
    return {
        "similarity_score": score_percent,
        "keywords": keywords,
        "status": status,
        "recommendation": recommendation,
    }
