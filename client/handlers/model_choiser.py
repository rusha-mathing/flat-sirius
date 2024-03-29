from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from magic_filter import F


__all__ = [
    "model_choiser",
]


models_info = {
    "Model A": "A INFO",
    "Model B": "B INFO",
}


class ModelChoise(StatesGroup):
    wait_choise = State()
    confirm_choise = State()


model_choiser = Router()


class ModelsCallbackFactory(CallbackData, prefix="model_choice"):
    action: str
    model: Optional[str] = None


@model_choiser.message(Command('models'), StateFilter(None))
async def send_models_menu(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    
    for name in models_info.keys():
        builder.button(
            text=f"{name}",
            callback_data=ModelsCallbackFactory(action='choice', 
                                                model=f"{name}")
        )


    builder.button(text='Cancel', callback_data=ModelsCallbackFactory(action='cancel'))
        
    await message.answer("Вот спискок моделей!", 
                         reply_markup=builder.as_markup())
    await state.set_state(ModelChoise.wait_choise)


@model_choiser.callback_query(ModelsCallbackFactory.filter(F.action == 'choice'), 
                              StateFilter(ModelChoise.wait_choise))
async def choise_model_callback_handler(callback: types.CallbackQuery, 
                                        callback_data: ModelsCallbackFactory,
                                        state: FSMContext):
    name = callback_data.model
    description = models_info[name]
        
    builder = InlineKeyboardBuilder()

    builder.button(text='Подтвердить', callback_data=ModelsCallbackFactory(action='confirm', model=name))
    builder.button(text='В главное меню', callback_data=ModelsCallbackFactory(action='cancel'))

    await callback.message.edit_text(f"{name}\n{description}", reply_markup=builder.as_markup())
    await state.set_state(ModelChoise.confirm_choise)
    await callback.answer()


@model_choiser.callback_query(ModelsCallbackFactory.filter(F.action == 'cancel'), 
                              StateFilter(ModelChoise.wait_choise, ModelChoise.confirm_choise))
async def cancel_model_callback_handler(callback: types.CallbackQuery, 
                                        state: FSMContext):
    from . import return_to_main
    await return_to_main(callback.message, state, edit=True)
    await callback.answer()
    

@model_choiser.callback_query(ModelsCallbackFactory.filter(F.action == 'confirm'), 
                              StateFilter(ModelChoise.confirm_choise))
async def cancel_model_callback_handler(callback: types.CallbackQuery,
                                        callback_data: ModelsCallbackFactory,
                                        state: FSMContext):
    from . import return_to_main
    await state.set_data({'model': callback_data.model})
    await callback.message.edit_text(f"Вы выбрали: {callback_data.model}")
    await return_to_main(callback.message, state)
    await callback.answer()
