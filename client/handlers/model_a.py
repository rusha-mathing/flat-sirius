from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from magic_filter import F


__all__ = [
    'model_a_router',
    "model_a_start_handling"
]


model_a_router = Router(name='model_a')


class ModelForm(StatesGroup):
    a = State()
    b = State()
    confirm = State()


async def model_a_start_handling(message: types.Message, state: FSMContext):
    await message.answer("Обработчик Model A. Введите A:")
    await state.update_data(a=message.text)
    await state.set_state(ModelForm.a)


@model_a_router.message(StateFilter(ModelForm.a))
async def model_form_a(message: types.Message, state: FSMContext):
    await state.update_data(a=message.text)

    await message.answer(f'Введите B:')
    await state.set_state(ModelForm.b)


@model_a_router.message(StateFilter(ModelForm.b))
async def model_form_b(message: types.Message, state: FSMContext):
    await state.update_data(b=message.text)

    data = await state.get_data()
    data.pop('model')
    data = '\n'.join(map(str, data.items()))
    await message.answer(f'Проверьте данные:\n{data}')
    await state.set_state(ModelForm.confirm)


@model_a_router.message(StateFilter(ModelForm.confirm))
async def model_form_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data.pop('model')

    result = handle_model(data)
    await message.answer(f"Ответ модели: {result}", reply_markup=types.ReplyKeyboardRemove())

    from . import return_to_main
    await return_to_main(message, state)


def handle_model(data):
    return 42


