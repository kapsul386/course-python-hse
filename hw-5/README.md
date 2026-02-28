
# HW-6 — Comments Service

REST-сервис комментариев к постам на Django + DRF.

Реализовано
- CRUD пользователей
- CRUD постов
- CRUD комментариев
- лайки постов и комментариев
- Swagger-документация
- мок-данные через data migration (HW-6)
- агрегированные/легковесные эндпоинты (HW-6)

Проект запускается через Docker Compose (Django + PostgreSQL).

---

## Запуск

Все команды выполнять из директории:

```

hw-5/project

```

Сборка и запуск:

```

docker compose up --build

```

После запуска:

- API: http://localhost:8000/api
- Swagger: http://localhost:8000/swagger/

Миграции:
````
docker compose exec django python backend/manage.py migrate
````
---

## Тесты

```

docker compose exec django python backend/manage.py test

```
