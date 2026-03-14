up:
	docker compose up --build

down:
	docker compose down -v

migrate:
	docker compose exec django python backend/manage.py migrate

test:
	docker compose exec django python backend/manage.py test comments
