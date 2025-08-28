import asyncio
import sqlite3
import os

from .imports import *
from bot.bot_instance import bot
from AI_agent.AI_agent import *

admin_router = Router()

current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "..", "..", "db")

@admin_router.message(Command('start'))
async def start(message: types.Message):
    await message.answer(text='Привет! Используйте /poll для создания опроса.')

@admin_router.message(Command('poll'))
async def poll(message: types.Message):
    connection = sqlite3.connect(f'{db_dir}/english.db')
    cursor = connection.cursor()

    while True:
        creating_db() # Вызов функции для создания базы данных
        generate_and_save_quiz() # Вызов функции для генерации квиза и записи его в базу данных

        cursor.execute("SELECT id, question, options, right_answer FROM PRONOUNS LIMIT 1")
        row = cursor.fetchone()
        if not row:
            await asyncio.sleep(5)
            continue

        row_id = row[0]
        print("Обрабатываю строку: ", row)

        cursor.execute("DELETE FROM PRONOUNS WHERE id = ?", (row_id,))
        connection.commit()

        question = row[1]
        options = row[2].split()
        right_answer = int(row[3]) - 1

        try:
            await bot.send_poll(
                chat_id="-1002058270200",
                question=question,
                options=options,
                type='quiz',
                correct_option_id=right_answer
            )
        except Exception as e:
            print(e)

        await asyncio.sleep(60*60*12)