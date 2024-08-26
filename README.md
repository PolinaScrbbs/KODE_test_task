# Тестирование API с помощью cURL

## Обзор

В этом документе приведены примеры использования `curl` для взаимодействия с API, включая регистрацию пользователей, вход в систему и доступ к защищенным маршрутам. Примеры запросов включают необходимые параметры и формат запросов.

## Базовый URL

Базовый URL для запросов к API:
http://localhost:8000

## Конечные точки

### 1. Регистрация нового пользователя

**Маршрут:** `POST /auth/register`

**Описание:** Регистрирует нового пользователя с указанным email и паролем.

**Запрос:**

```sh
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "newuser@example.com",
           "password": "newpassword"
         }'
```

**Ответ:**

**Код состояния:** `201 Created`

**Тело:** JSON объект с данными пользователя

### 2. Регистрация с уже существующим email
**Маршрут:** `POST /auth/register`

**Описание:** Пытается зарегистрировать пользователя с email, который уже существует.

**Запрос:**

```sh
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "existinguser@example.com",
           "password": "somepassword"
         }'

```

**Ответ**:

**Код состояния:** `400 Bad Request`

**Тело: JSON объект с деталями ошибки**

### 3. Вход в систему
**Маршрут:** `POST /auth/login`

**Описание:** Авторизует пользователя с указанным email и паролем.

**Запрос:**

```sh
curl -X POST "http://localhost:8000/auth/jwt/login" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "user@example.com",
           "password": "userpassword"
         }'
```
**Ответ:**

**Код состояния:** `200 OK`

**Токен появится в файлах Cookie**

### 4. Создание новой заметки
**Маршрут:** `POST /api/notes`

**Описание:** Создает новую заметку с указанным заголовком и содержанием.

**Запрос:**

```sh
curl -X POST "http://localhost:8000/notes" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Моя заметка",
           "content": "Содержание заметки"
         }'
```

**Ответ:**

**Код состояния:** `201 Created`

**Тело:**

```json
{
  "id": "note123",
  "title": "Моя заметка",
  "content": "Содержание заметки",
  "created_at": "2024-08-26T12:34:56Z",
  "updated_at": "2024-08-26T12:34:56Z"
}
```

**Описание:**

**id:** Уникальный идентификатор заметки.

**content:** Содержание заметки.

**created_at:** Дата и время создания заметки.

**updated_at:** Дата и время последнего обновления заметки.

### 5. Получение заметки по ID
**Маршрут:** `GET api/notes/{id}`

**Описание:** Получает информацию о заметке по её уникальному идентификатору.

**Запрос:**

```sh
curl -X GET "http://localhost:8000/notes/{note_id}"
```

**Ответ:**

Код состояния: `200 OK`

**Тело:**

```json
{
  "id": "note123",
  "title": "Моя заметка",
  "content": "Содержание заметки",
  "created_at": "2024-08-26T12:34:56Z",
  "updated_at": "2024-08-26T12:34:56Z"
}
```

**Описание:**

**id:** Уникальный идентификатор заметки.

**title:** Заголовок заметки.

**content:** Содержание заметки.

**created_at:** Дата и время создания заметки.

**updated_at:** Дата и время последнего обновления заметки.
