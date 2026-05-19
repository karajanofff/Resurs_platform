# SmartResurs AI

Aqlli ta'lim resurslari tahlilchisi.

Ta'lim resurslarining fan mavzulariga tegishliligini `TF-IDF` va `cosine similarity` yordamida avtomatik baholovchi yengil web-platforma.

## Texnologiyalar

- FastAPI, Jinja2, SQLite, SQLAlchemy
- scikit-learn TF-IDF + cosine similarity
- PDF, DOCX, PPTX, TXT matn ajratish
- Tailwind CSS CDN

## Lokal ishga tushirish

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Brauzerda `http://127.0.0.1:8000` ni oching.

## Demo loginlar

- Admin: `admin@example.com / admin123`
- O'qituvchi: `teacher@example.com / teacher123`
- Talaba: `student@example.com / student123`

## Foydalanish tartibi

1. Admin fan va mavzularni boshqaradi.
2. O'qituvchi resurs yuklaydi va NLP tahlilni ishga tushiradi.
3. Tizim fayldan matn ajratadi, moslik foizini hisoblaydi, kalit so'zlarni chiqaradi.
4. Talaba katalogdan mos resurslarni ko'radi va yuklab oladi.

## Render deploy

1. Loyihani GitHub ga yuklang.
2. Render'da `New` -> `Blueprint` ni tanlang.
3. Repository ni ulang.
4. Render `render.yaml` orqali servisni yaratadi.

`RESET_DB_ON_START=true` Render free filesystemi uchun ataylab qo'yilgan: har yangi ishga tushishda baza toza yaratilib, demo foydalanuvchilar va boshlang'ich fanlar qayta seed qilinadi.
