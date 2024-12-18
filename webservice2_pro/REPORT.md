# Отчет по Проекту Django + FastAPI Чат-Бот

## 1. Отчет, что, где и зачем настраивали.

### 1.1 Директории и файлы

- **webservice2_pro/django_chatbot/**: Основное Django-приложение.
  - **__pycache__/**: Скомпилированные файлы Python.
  - **.vscode/**: Настройки для редактора Visual Studio Code.
  - **chatbot/**: Приложение Django, содержащее логику чат-бота.
    - `__init__.py`
    - `admin.py`
    - `apps.py`
    - `models.py`
    - `tests.py`
    - `views.py`
    - **static/**: Статические файлы (CSS, JS, изображения).
    - **templates/**: HTML-шаблоны.
      - `base.html`
      - `chatbot.html`
      - `start.html`
      - `stats.html`
  - **django_chatbot/**: Настройки и конфигурации Django-проекта.
    - `__init__.py`
    - `asgi.py`
    - `settings.py`
    - `urls.py`  
    - `wsgi.py`
  - `db.sqlite3`: SQLite база данных. Не используем!
  - `manage.py`: Скрипт для управления Django-проектом.

- **webservice2_pro/fastapi/**: FastAPI-приложение для обработки API-запросов.
  - `__init__.py`
  - `.env`: Файл переменных окружения (например, API-ключи).
  - `chunks.py`: Логика для обработки текстов и взаимодействия с OpenAI.
  - `main.py`: Основной файл FastAPI-приложения.
  - `Simble.txt`: Файл базы знаний или документов для чат-бота.
  - `test_chunks.ipynb`, `test_main.ipynb`: Тестовые ноутбуки Jupyter для проверки функциональности.

## 2. Настройка Django Приложения

### 2.0 Установка и настройка:

1. **Установим django при помощи команды:**
	
 - `python -m pip install -r requirements.txt`


2. **Проект скопирован в учебных целях:**
 - `https://disk.yandex.ru/d/TCc7I964lipSdA`

 `django-admin startproject` **django_chatbot**


3. **Запустим проект на локальном сервере (для проверки работоспособности):**

 -`python manage.py runserver`



4. **Добавить в проект новое приложение при помощи команды:**

 -`python manage.py startapp` название_приложения `chatbot`


5. **Наполнить приложение всем необходимым функционалом (views, urls, templates, static и тд)**


6. **Запустить готовый проект:**

 -`python manage.py runserver`

### 2.1. Файл `settings.py`

- **Выполнение  настройки:**

- **Установленные приложения (`INSTALLED_APPS`):**
  - Стандартные Django-приложения.
  - `chatbot`, # Добавим приложение.
  - `corsheaders`, # Для корректной и безопасной настройки CORS-политик в Django-приложении.

- **Middleware:**
  - Включает стандартные middleware Django.
  - `corsheaders.middleware.CorsMiddleware`: Добавляет поддержку CORS.

- **CORS Настройки:**
  - `CORS_ALLOW_ALL_ORIGINS = True`: Разрешает запросы с любых источников.

- **Шаблоны (`TEMPLATES`):**
  - Определяет директории с HTML-шаблонами.
  - `DIRS`: [BASE_DIR / 'templates'], # Указывается путь к директории с шаблонами.
  - Включает контекстные процессоры для предоставления контекста в шаблонах.

- **Статические файлы:**
  - `STATIC_URL = '/static/'` # URL для доступа к статическим файлам.
  - `STATICFILES_DIRS = [ BASE_DIR / "static" ]` # Дополнительные директории со статическими файлами.
  - `STATIC_ROOT = BASE_DIR / "staticfiles"`: Директория для сбора статических файлов при развертывании.


### 2.2. Файл `urls.py`

- **Импорты:**
  - `from django.urls import path`
  - `from chatbot import views`

- **URL Patterns:**
    ```python
    urlpatterns = [
        path('', views.start, name='start'),  # Добавим Имя для Главной Страницы
        path('chatbot/', views.chatbot, name='chatbot'),  # Добавим Завершающий Слеш / в Пути
        path('stats/', views.stats, name='stats'),  # Добавим Завершающий Слеш / в Пути
    ]
    ```

- **Изменения:**
  - **Добавим имена маршрутов:**
    - `name='start'` для главной страницы.
    - `name='chatbot'` для страницы чат-бота.
    - `name='stats'` для страницы статистики.
  
  - **Добавим завершающие слеши:**
    - Маршруты `'chatbot/'` и `'stats/'` теперь заканчиваются слешем.

## 3. Настройка FastAPI Приложения

### 3.1. Файл `main.py`

- **Импорты и инициализация:**
  - Импорт необходимых модулей (FastAPI, Pydantic, CORS, логирование).
  - Настройка логирования (`app.log`).
  - Инициализация FastAPI приложения.

- **Эндпоинты:**
  - `GET /`: Возвращает приветственное сообщение.
  - `GET /about`: Возвращает описание проекта.
  - `GET /users/{id}`: Возвращает информацию о пользователе по ID.
  - `POST /test`: Тестовый эндпоинт, возвращающий сообщение.
  - `POST /users`: Принимает данные пользователя и возвращает информацию.
  - `POST /api/get_answer`: Основной эндпоинт для получения ответа от чат-бота.
  - `GET /api/request_count`: Возвращает общее количество обращений к `get_answer`.

- **Класс `Chunk` из `chunks.py`:**
  - Обрабатывает взаимодействие с OpenAI API и LangChain.
  - Загружает и разбивает документ (`Simble.txt`) на чанки.
  - Создает векторную базу данных с помощью FAISS.
  - Формирует ответы на основе запросов пользователей.

### 3.2. Файл `chunks.py`

- **Импорты и настройки:**
  - Импорт библиотек для работы с OpenAI, LangChain, FAISS и логированием.
  - Загрузка переменных окружения из `.env`.

- **Класс `Chunk`:**
  - **Метод `__init__`:** Инициализирует API-ключ OpenAI и загружает базу знаний.
  - **Метод `base_load`:** Читает документ, разбивает его на чанки и создает векторную базу.
  - **Метод `get_answer`:** Принимает запрос, ищет релевантные чанки и формирует ответ с помощью ChatOpenAI.

### 3.3. Файл `.env`

- Хранит переменные окружения, такие как `OPENAI_API_KEY`.

### 3.4. Логирование (`app.log`)

- Записывает информацию о работе приложения, ошибки и другие события для отладки и мониторинга.

## 4. Взаимодействие Django и FastAPI

- **Django** отвечает за рендеринг веб-страниц и обработку пользовательского интерфейса.
- **FastAPI**  получение ответов от чат-бота.

### 5. Файл `requirements.txt`

- Содержит список всех зависимостей проекта.
- Пример содержимого может включать:
