from aiogram import Router
from aiogram.filters.command import Command
from aiogram import types
from client.filters import *

__all__ = [
    'main_router'
]

main_router = Router(name="main_router")


@main_router.message(Command("ping"), ChatTypeFilter(chat_type='chat'))
async def cmd_test1(message: types.Message):
    await message.reply("pong")