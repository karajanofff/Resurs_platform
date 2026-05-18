# SmartKutubxona AI

Ta'lim resurslarini fan mavzulariga mosligini TF-IDF va cosine similarity yordamida avtomatik baholovchi yengil web-platforma.

## Local ishga tushirish

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Brauzerda `http://127.0.0.1:8000` ni oching.

## Virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

## Requirements o'rnatish

```bash
pip install -r requirements.txt
```

## Uvicorn bilan ishga tushirish

```bash
uvicorn app.main:app --reload
```

## GitHub ga yuklash

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <repository-url>
git push -u origin main
```

## Render.com ga joylash

1. Repository ni GitHub ga push qiling.
2. Render'da `New` -> `Blueprint` ni tanlang.
3. Repository ni ulang.
4. Render `render.yaml` faylidan servisni yaratadi.
5. `SECRET_KEY` environment variable qo'shing.

## Demo loginlar

- Admin: `admin@example.com / admin123`
- O'qituvchi: `teacher@example.com / teacher123`
- Talaba: `student@example.com / student123`

## Platformadan foydalanish tartibi

1. Login orqali tizimga kiring.
2. Admin fan va mavzular qo'shadi.
3. O'qituvchi fan va mavzuni tanlab PDF, DOCX, PPTX yoki TXT fayl yuklaydi.
4. Tizim fayldan matn ajratadi, matnni tozalaydi, TF-IDF vektor yaratadi va cosine similarity hisoblaydi.
5. Natija foiz, status, kalit so'zlar va tavsiya ko'rinishida chiqadi.
6. Talaba katalogdan resurslarni filter qilib ko'radi va yuklab oladi.

## NLP mexanizmi

- `clean_text`
- `extract_keywords`
- `calculate_similarity`
- `analyze_resource`

Og'ir model ishlatilmaydi. Faqat `scikit-learn` asosidagi TF-IDF va cosine similarity ishlatiladi.
