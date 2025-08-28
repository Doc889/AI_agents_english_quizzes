import os
import sqlite3

from dotenv import load_dotenv
from langchain_gigachat import GigaChat
from langchain.prompts import ChatPromptTemplate

from .propmts import *

load_dotenv()

GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")

tasks_generator = GigaChat(
    credentials=GIGACHAT_API_KEY,
    verify_ssl_certs=False
)

db_updater = GigaChat(
    credentials=GIGACHAT_API_KEY,
    verify_ssl_certs=False
)

db_path = os.path.join(os.path.dirname(__file__), "..", "db", "english.db")
db_path = os.path.abspath(db_path)


def creating_db() -> None:  # Функция для создания таблицы в базе данных
    global db_path

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    if not os.path.exists('../db/english.db'):
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS PRONOUNS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            options TEXT,
            right_answer INTEGER
        )
        """)
        connection.commit()
        connection.close()


def insert_quiz_to_db_tool(data: str):  # Функция для записи квиза в базу данных
    global db_path

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:
        parts = data.strip("'").split(';')
        if len(parts) != 3:
            return "Неверный формат."

        question = parts[0].strip()
        options = parts[1].strip()
        right_answer = parts[2].strip()

        if len(options.split()) != 4:
            return "Должно быть 4 варианта ответа."

        cursor.execute(
            "INSERT INTO PRONOUNS (question, options, right_answer) VALUES (?, ?, ?)",
            (question, options, right_answer)
        )
        connection.commit()
        connection.close()
        return f"✅Сохранено {question} -> {options} correct: {right_answer}"

    except Exception as e:
        return f"❌ Ошибка: {e}"


def check_quiz(quiz: str):  # Функция для проверка квиза на корректность
    prompt_template_for_update = ChatPromptTemplate.from_messages(messages)
    prompt_for_update_with_quiz = prompt_template_for_update.invoke({"quiz": quiz})
    response = db_updater.invoke(prompt_for_update_with_quiz)

    return response.content


def generate_and_save_quiz():  # Функция, которая объединяет работу двух ИИ-агентов
    global db_path

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM PRONOUNS")
    count = cursor.fetchone()[0]
    if count <= 5:  # Проверка на количество квизов, записанных в базу данных
        response = tasks_generator.invoke(prompt_for_generation)
        quiz = response.content.strip().strip("'").strip('"')
        print("Сгенерировано:", quiz)

        if check_quiz(quiz) == 'ВЕРНО':  # Вызываем функцию записи квиза в базу данных
            insert_quiz_to_db_tool(quiz)
