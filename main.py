from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from config import BOT_TOKEN
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from keyboards import main_keyboard, select_date_keyboard

bot = Bot(BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    main_state = State()
    add_credit_state = State()


opened_credit_lines = {}


@dp.message_handler(Command("start"), state=None)
async def echo(message: Message):
    await message.answer(text="Hello, %s. This is credit bot. Available actions: " % message.from_user.username,
                         reply_markup=main_keyboard)
    await Form.main_state.set()


@dp.message_handler(state=Form.main_state)
async def handle_main_menu(message: Message, state: FSMContext):
    act = message.text
    user_id = message.from_user.id
    if user_id not in opened_credit_lines:
        opened_credit_lines[user_id] = ""
    if act != "Start credit line":
        await message.answer("Here are your credit lines: %s" % opened_credit_lines[user_id],
                             reply_markup=main_keyboard)
        await Form.main_state.set()
    else:
        await state.update_data(action_made=act)
        await message.answer("Enter credit line start date", reply_markup=select_date_keyboard)
        await Form.add_credit_state.set()


@dp.message_handler(state=Form.add_credit_state)
async def handle_new_credit_line(message: Message, state: FSMContext):
    act = message.text
    user_id = message.from_user.id
    if user_id not in opened_credit_lines:
        opened_credit_lines[user_id] = ""
    if act == "Cancel":
        await message.answer("Exit adding credit lines: %s", reply_markup=main_keyboard)
        await Form.main_state.set()
    else:
        await state.update_data(action_made=act)
        opened_credit_lines[user_id] += " " + message.text
        await message.answer("Successfully registered", reply_markup=main_keyboard)
        await Form.main_state.set()


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=on_shutdown)
