from aiogram import Router
from aiogram.filters.command import Command
from aiogram import types
from aiogram.fsm.context import FSMContext
from client.filters import *
from .model_choiser import model_choiser

__all__ = [
    'main_router',
    'return_to_main'
]

main_router = Router(name="main_router")

main_router.include_router(model_choiser)


@main_router.message(Command("help"))
async def help_command(message: types.Message):
    commands_info = {
        'start': "в главное меню",
        'help': "помощь",
        'models': 'выбор модели'
    }
    await message.reply('\n'.join(map(str, commands_info.items())))


@main_router.message(Command('start'))
async def return_to_main(message: types.Message, state: FSMContext, edit=False):
    model_name = (await state.get_data()).get('model', "Model A")
    message_text = f"Главное меню. \nModel: {model_name}"
    if edit:
        await message.edit_text(message_text)
    else:
        await message.answer(message_text)
    await state.set_state()

