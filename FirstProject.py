import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram.fsm.state import StatesGroup, State

TOKEN = "7265160375:AAEIiAlTtlQdb544r08bZIElB73-i_J3eek"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


class Reg(StatesGroup):
    name = State()
    number = State()


@dp.message(Command('reg'))
async def reg_func(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer("Ismingizni kiriting: ")


@dp.message(Reg.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Telefon raqamingizni kiriting:")
    await state.set_state(Reg.number)


@dp.message(Reg.number)
async def get_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f"Ro'yxatdan o'tish yakunlandi!\n\nIsm: {data.get('name')}\nTel: {data.get('number')}")
    await state.clear()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
