import asyncio
from aiogram import Dispatcher

from bot.bot_instance import bot
from bot.handlers.admin_handlers import admin_router


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(admin_router)


async def main() -> None:
    dp = Dispatcher()
    register_routers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
