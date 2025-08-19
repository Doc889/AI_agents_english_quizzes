import os
from dotenv import load_dotenv

from aiogram import Bot

load_dotenv()

API_TOKEN_TELEGRAM = os.getenv("API_TOKEN_TELEGRAM")

bot = Bot(token=API_TOKEN_TELEGRAM)