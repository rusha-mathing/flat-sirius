from aiogram import Bot, Dispatcher

from .config_reader import config
from .handlers import main_router

__all__ = [
    'main'
]


bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


async def main():
    dp.include_router(main_router)
    print("Start polling!")
    await dp.start_polling(bot)
