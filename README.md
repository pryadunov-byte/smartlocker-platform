# SmartLocker Platform

Полноценный демо-стек для управления сетью постаматов с back-office, аналитикой, API и публичными экранами клиента.

## Состав

- **Backend** — FastAPI + PostgreSQL + SQLAlchemy + Alembic, Redis/Celery для фоновых задач, WebSocket для алертов.
- **Frontend** — Next.js 14 (App Router), TypeScript, TailwindCSS, Zustand, React Query, Recharts, MapLibre (react-map-gl).
- **Инфраструктура** — Docker Compose (API, БД, Redis, MinIO, Frontend, Nginx), make-скрипты.

## Быстрый старт

```bash
cp .env.example .env
make up
```

После сборки будут доступны:

- http://localhost:8080/admin — back-office панель.
- http://localhost:8080/public/DEMO123 — публичная страница заказа (замените UID на реальный).
- http://localhost:8080/device-sim — эмулятор терминала.
- http://localhost:8000/docs — Swagger UI API.

Загрузка демо-данных:

```bash
make seed
```

## Структура

- `backend/app` — FastAPI приложение, модели, сервисы, маршруты, задачи Celery.
- `backend/alembic` — миграции базы данных.
- `frontend` — Next.js приложение с экранами back-office, публичным сервисом и эмулятором устройства.
- `infra` — Dockerfile'ы и конфигурация Nginx.

## Тестовые учётные записи

- `admin@demo.local / Admin123!`
- `operator@demo.local / Operator123!`
- `technician@demo.local / Tech123!`

## Основные возможности

- Панель KPI, карта устройств, realtime-алерты через WebSocket.
- Управление заказами: создание, обновление, контроль PIN/QR кодов.
- Редактор устройств и ячеек (статусы, сервисы, флаги).
- Конструктор сценариев хранения с параметрами разблокировки и уведомлений.
- Аналитика заполненности и ROMI.
- Публичная мобильная страница получения заказа и эмулятор терминала.

## Разработка

- `make api` — локальный запуск FastAPI.
- `make frontend` — запуск Next.js в режиме разработки.

Перед пушем не забудьте прогнать форматирование и тесты.
