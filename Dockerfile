FROM node:20-bookworm-slim AS frontend-deps

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install

FROM node:20-bookworm-slim AS frontend-builder

WORKDIR /frontend
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=frontend-deps /frontend/node_modules ./node_modules
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim

WORKDIR /app
ENV BACKEND_INTERNAL_URL=http://127.0.0.1:8000
ENV NODE_ENV=production

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl nodejs npm \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ ./backend/
COPY --from=frontend-builder /frontend/.next/standalone ./frontend/
COPY --from=frontend-builder /frontend/.next/static ./frontend/.next/static
COPY --from=frontend-builder /frontend/public ./frontend/public

CMD ["sh", "-c", "cd /app/backend && uvicorn app.main:app --host 127.0.0.1 --port 8000 & cd /app/frontend && PORT=${PORT:-10000} HOSTNAME=0.0.0.0 node server.js"]
