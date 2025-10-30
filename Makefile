.PHONY: up down seed api frontend

up:
docker compose -f infra/docker-compose.yml up -d --build

down:
docker compose -f infra/docker-compose.yml down

seed:
docker compose -f infra/docker-compose.yml exec api python -m app.seed

api:
cd backend && uvicorn app.main:app --reload

frontend:
cd frontend && npm run dev
