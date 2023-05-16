from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from constants import test_link
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    """Handler to introduce bot himself."""

    await message.answer("Greetings! I'm test version of CyberTolya bot!")

@dp.message_handler()
async def echo_handler(message: types.Message):
    """Test handler which duplicate every message like echo."""

    await message.answer(test_link[0])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
