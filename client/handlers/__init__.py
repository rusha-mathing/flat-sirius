from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from client.filters import *
from .model_choiser import model_choiser
from .model_a import model_a_router, model_a_start_handling

__all__ = [
    'main_router',
    'return_to_main',
]

main_router = Router(name="main_router")
main_router.include_router(model_choiser)
main_router.include_router(model_a_router)


async def get_model(state: FSMContext) -> str:
    data = await state.get_data()
    return data.get('model', "Model A")



@main_router.message(Command("help"))
async def help_command(message: types.Message):
    commands_info = {
        'start': "в главное меню",
        'help': "помощь",
        'models': 'выбор модели',
        'handle': 'обработка моделью'
    }
    await message.reply('\n'.join(map(str, commands_info.items())))


@main_router.message(Command('start'))
async def return_to_main(message: types.Message, state: FSMContext, edit=False):
    model_name = await get_model(state)
    await state.clear()
    await state.set_data({'model': model_name})
    message_text = f"Главное меню. \nModel: {model_name}"
    if edit:
        await message.edit_text(message_text, reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(message_text, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state()


@main_router.message(Command('handle'), StateFilter(None))
async def delegate_to_concrete_models(message: types.Message, state: FSMContext):
    model = await get_model(state)
    if model == 'Model A':
        await model_a_start_handling(message, state)
    elif model == "Model B":
        pass