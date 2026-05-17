# SmartKutubxona AI

Ta'lim resurslarini fan mavzulariga mosligini NLP yordamida avtomatik baholovchi elektron kutubxona platformasi.

## Texnologiyalar

- Frontend: Next.js, TypeScript, Tailwind CSS, Lucide React, Recharts
- Backend: FastAPI, SQLAlchemy, JWT
- Database: PostgreSQL
- NLP: TF-IDF, cosine similarity, PDF/DOCX/PPTX/TXT matn ajratish

## Lokal ishga tushirish

1. `.env.example` faylini `.env` nomi bilan nusxalang.
2. Docker bilan:

```bash
docker compose up --build
```

3. Brauzerda `http://localhost:3000` ni oching.

## Demo loginlar

- Admin: `admin@example.com / admin123`
- O'qituvchi: `teacher@example.com / teacher123`

## Ishlaydigan sahifalar

- `/` - landing page
- `/login` - role tanlash va kirish
- `/dashboard` - login qilingan foydalanuvchini roliga qarab yo'naltiradi
- `/dashboard/admin?view=...` - admin bo'limlari
- `/dashboard/teacher?view=...` - o'qituvchi bo'limlari
- `/analysis` - oxirgi NLP natijasini ko'rsatadi

## NLP oqimi

1. Fayl yuklanadi.
2. Matn ajratiladi.
3. Matn tozalanadi.
4. Kalit so'zlar aniqlanadi.
5. Resurs va mavzu matni TF-IDF vektorlarga aylantiriladi.
6. Cosine similarity hisoblanadi.
7. Natija bazaga yoziladi.

Moslik qoidalari:

- `>= 75%`: `Mos`
- `40% - 75%`: `Qisman mos`
- `< 40%`: `Mos emas`

## API endpointlar

- `POST /api/auth/login`
- `POST /api/auth/register`
- `GET /api/me`
- `GET /api/users`
- `POST /api/users`
- `GET /api/subjects`
- `POST /api/subjects`
- `PUT /api/subjects/:id`
- `DELETE /api/subjects/:id`
- `GET /api/topics`
- `POST /api/topics`
- `PUT /api/topics/:id`
- `DELETE /api/topics/:id`
- `POST /api/resources/upload`
- `GET /api/resources`
- `GET /api/resources/:id`
- `PUT /api/resources/:id/approve`
- `DELETE /api/resources/:id`
- `POST /api/analyze`
- `GET /api/statistics`

## Render.com ga deploy qilish

1. Loyihani GitHub repository ga yuklang.
2. Render dashboardda yangi PostgreSQL database yarating.
3. Repository dan ikkita Web Service yarating:
   - Backend uchun `backend/`
   - Frontend uchun `frontend/`
4. Environment variables kiriting:

```env
DATABASE_URL=
JWT_SECRET=
UPLOAD_DIR=uploads
FRONTEND_URL=
BACKEND_URL=
NODE_ENV=production
NEXT_PUBLIC_API_URL=
```

5. Backend uchun:

```bash
Build command: pip install -r requirements.txt
Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

6. Frontend uchun:

```bash
Build command: npm install && npm run build
Start command: npm run start
```

7. `render.yaml` fayli Blueprint deploy uchun tayyor.
8. Database migration bu demo versiyada `startup` vaqtida `create_all` bilan avtomatik yaratiladi. Katta production loyihada Alembic qo'shish tavsiya etiladi.
9. Deploydan keyin demo loginlar bilan kirishni tekshiring.
10. Render deployda backend persistent disk ishlatilmasa, `uploads/` fayllari redeploy vaqtida yo'qolishi mumkin. Diplom demo uchun bu yetarli, production uchun object storage tavsiya etiladi.

## Papka tuzilmasi

```text
smartkutubxona-ai/
  frontend/
  backend/
  docker-compose.yml
  render.yaml
  README.md
  .env.example
```

## Render bo'yicha eslatma

Backend va frontend domenlari yaratilgach, `FRONTEND_URL`, `BACKEND_URL` va `NEXT_PUBLIC_API_URL` qiymatlarini haqiqiy Render URL lariga moslang.
