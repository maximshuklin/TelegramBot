import os
from dotenv import load_dotenv

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from messages import help_message, start_message

load_dotenv(verbose=True)
BOT_TOKEN = os.getenv('TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
	await message.reply(start_message)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
	await message.reply(help_message)

@dp.message_handler()
async def echo_message(msg: types.Message):
	text = f"text : {msg.text}, user : {msg.from_user.id}, name : {msg.from_user.full_name}"
	await bot.send_message(msg.from_user.id, text)


if __name__ == '__main__':
    executor.start_polling(dp)