from dotenv import load_dotenv
import os
import openai
import asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Загрузка переменных окружения
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Chunk:
    def __init__(self):
        # Установка API-ключа
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("Ключ API OpenAI не найден. Проверьте переменные окружения.")
        self.base_load()

    def base_load(self):
        # Путь к базе знаний
        rules_path = os.path.join(os.path.dirname(__file__), 'Simble.txt')
        if not os.path.exists(rules_path):
            raise FileNotFoundError(f"Файл {rules_path} не найден.")
        
        # Чтение содержимого
        with open(rules_path, 'r', encoding='utf-8') as file:
            document = file.read()

        # Разбиение текста на чанки
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        source_chunks = splitter.split_text(document)
        docs = [Document(page_content=chunk) for chunk in source_chunks]

        # Создание векторной базы
        embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
        self.db = FAISS.from_documents(docs, embeddings)

        # Формирование системного сообщения
        self.system = '''
            Ты-консультант в компании Simble.
            Ответь на вопрос клиента на основе документа с информацией.
            Не придумывай ничего от себя, отвечай максимально по документу.
            Не упоминай документ с информацией для ответа клиенту.
            Клиент ничего не должен знать про документ с информацией для ответа клиенту.
        '''

    async def get_answer(self, query: str):
        # Поиск в базе
        docs = self.db.similarity_search(query, k=4)
        message_content = '\n'.join([doc.page_content for doc in docs])

        # Формирование пользовательского сообщения
        user_message = f'''
            Ответь на вопрос клиента. Не упоминай документ с информацией для ответа в ответе.
            Контекст для ответа:
            {message_content}

            Вопрос клиента:
            {query}
        '''

        # Формирование сообщений для чат-модели
        messages = [
            SystemMessage(content=self.system),
            HumanMessage(content=user_message)
        ]

        # Инициализация ChatOpenAI
        chat = ChatOpenAI(model_name='gpt-4', temperature=0, openai_api_key=openai.api_key)

        # Получение ответа (асинхронно)
        response = await chat.agenerate([messages])

        # Возвращаем текст ответа
        return response.generations[0][0].text.strip()

# Запуск программы для проверки
if __name__ == "__main__":
    chunk = Chunk()
    query = 'Какие исключения предусмотрены в страховом договоре?'
    try:
        # Запускаем асинхронную функцию
        result = asyncio.run(chunk.get_answer(query))
        print(result)
    except Exception as e:
        print(f"Ошибка: {e}")
