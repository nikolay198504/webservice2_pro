from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .chunks import Chunk
from fastapi.middleware.cors import CORSMiddleware
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования: INFO, DEBUG, ERROR и т.д.
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники. Рекомендуется ограничить в продакшене.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

# Функция, которая обрабатывает запрос по пути "/about"
@app.get('/about')
def about():
    return {'message': 'Страница с описанием проекта'}

# Функция-обработчик с параметрами пути
@app.get('/users/{id}')
def users(id: int):
    return {'Вы ввели user_id': id}

# Pydantic модель для ответа эндпоинта /test
class TestResponse(BaseModel):
    message: str

# POST-запрос на путь "/test"
@app.post('/test', response_model=TestResponse)
def post_test():
    return {'message': 'Hello Man'}

# Класс с типами данных параметров
class Item(BaseModel):
    name: str
    description: str
    old: int

# Функция-обработчик POST-запроса с параметрами
@app.post('/users')
def post_users(item: Item):
    return {'answer': f'Пользователь: {item.name} - {item.description}, возраст: {item.old} лет'}

# Класс с типами данных для метода api/get_answer
class ModelAnswer(BaseModel):
    text: str

try:
    chunk = Chunk()
    logger.info("Класс Chunk инициализирован успешно.")
except Exception as e:
    logger.error(f"Ошибка при инициализации Chunk: {e}")
    chunk = None  # Или можете завершить приложение, если инициализация критична

# Глобальная переменная для подсчёта запросов к /api/get_answer
get_answer_request_count = 0

@app.post('/api/get_answer')
async def get_answer(question: ModelAnswer):
    global get_answer_request_count
    get_answer_request_count += 1  
    logger.info(f"Получен запрос на /api/get_answer с текстом: {question.text}")
    
    if not chunk:
        logger.error("Класс Chunk не инициализирован.")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")
    
    try:
        answer = await chunk.get_answer(query=question.text)
        logger.info(f"Получен ответ: {answer}")
        return {'message': answer}
    except Exception as e:
        logger.error(f"Ошибка при обработке get_answer: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")

# GET-метод для получения количества обращений к /api/get_answer
@app.get('/api/request_count')
def get_request_count():
    return {'total_get_answer_requests': get_answer_request_count}
