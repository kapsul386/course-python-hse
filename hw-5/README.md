# HW-7 - Comments Service (Django + DRF)

REST-сервис комментариев к постам на Django и DRF.

## Что реализовано

- CRUD пользователей
- CRUD постов
- CRUD комментариев
- Лайки для постов и комментариев
- Swagger-документация API
- Мок-данные через data migration `comments.0003_seed_data`
- Кастомный эндпоинт `GET /api/posts/top/` для получения топа постов по лайкам
- Кастомный эндпоинт `GET /api/comments/by_post/?post_id=<id>` для получения легковесного списка комментариев по посту

## HW-7: авторизация, права, тесты

- Базовая авторизация DRF: `SessionAuthentication`, `BasicAuthentication`
- Чтение постов и комментариев доступно без авторизации
- Создание, редактирование и удаление доступны только авторизованным пользователям
- Изменение и удаление поста или комментария доступны только автору или администратору
- Изменение и удаление пользователя доступны только самому пользователю или администратору
- Защита от подмены автора: поле `author` для постов и комментариев назначается из `request.user`
- Защита от подмены пользователя: поле `user` для лайков назначается из `request.user`
- Тесты покрывают CRUD-ограничения, права доступа, лайки и кастомные эндпоинты
- В контейнере проходят `13` тестов

## Структура

Все команды ниже нужно выполнять из директории:

```bash
hw-5/project
```

## Запуск проекта

```bash
docker compose up --build
```

После запуска:

- API: http://localhost:8000/api/
- Swagger: http://localhost:8000/swagger/
- Admin: http://localhost:8000/admin/

## Миграции

```bash
docker compose exec django python backend/manage.py migrate
```

Проверка примененных миграций для приложения `comments`:

```bash
docker compose exec django python backend/manage.py showmigrations comments
```

## Тесты

Рекомендуемая команда для этого проекта:

```bash
docker compose exec django python backend/manage.py test comments
```

Ожидаемый результат:

- `Found 13 test(s)`
- `Ran 13 tests`
- `OK`

