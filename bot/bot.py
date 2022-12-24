import os
from dotenv import load_dotenv

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


from messages import help_message, start_message
from data_control import *


# load environmental variables
load_dotenv(verbose=True)
BOT_TOKEN = os.getenv('TOKEN')


# initialize bot and dispatches
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# States declaration
class State:
	START =           0
	HELP =            1
	SEND_TEXT =       2
	SEND_MEDIA =      3
	ADD_CATEGORY =    4
	DELETE_CATEGORY = 5
	SHOW_PHOTOS     = 7


user_state = {
	
}

media_messages = {
	
}


def set_state(user_id: int, state: int):
	user_state[user_id] = state

def get_user_state(user_id: int):
	if not user_id in user_state:
		user_state[user_id] = State.START
	return user_state[user_id]

# a bag of shit

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
	user_id = message.from_user.id

	set_state(user_id, State.START)

	await message.reply(start_message)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
	user_id = message.from_user.id
	set_state(user_id, State.HELP)
	await message.reply(help_message)


@dp.message_handler(commands=['add', 'add_category'])
async def process_add_category_command(message: types.Message):
	user_id = message.from_user.id
	set_state(user_id, State.ADD_CATEGORY)
	await bot.send_message(user_id, "Напишите название категории, которую хотите добавить:")


@dp.message_handler(commands=['del', 'delete_category'])
async def process_delete_category_command(message: types.Message):
	user_id = message.from_user.id
	set_state(user_id, State.DELETE_CATEGORY)
	await bot.send_message(user_id, "Напишите название категории, которую хотите удалить:")


@dp.message_handler(commands=['categories'])
async def process_show_categories_command(message: types.Message):
	user_id = message.from_user.id
	set_state(user_id, State.START)

	user_categories = list_categories(user_id)

	await bot.send_message(user_id, "\n".join(user_categories))


@dp.message_handler(commands=['show_photos'])
async def process_show_photo_command(message: types.Message):
	user_id = message.from_user.id
	await bot.send_message(user_id, "Фотографии из какой категории вам показать?")
	set_state(user_id, State.SHOW_PHOTOS)


@dp.message_handler(content_types=['photo'])
async def process_photo_command(message):
	user_id = message.from_user.id
	if media_messages.get(user_id) == None:
		media_messages[user_id] = []
	media_messages[user_id].append(message)

	set_state(user_id, State.SEND_MEDIA)
	await bot.send_message(user_id, "В какую категорию вы хотите отправить фото?")




# text handlers

# add_category_text_handler
async def add_category_text_handler(message: types.Message):
	user_id = message.from_user.id
	user_text = message.text

	if not (1 <= len(user_text) <= 20):
		await bot.send_message(user_id, "Название категории должно быть от 1 до 20 символов")
	else:
		try:
			create_category(user_id, user_text)
		except:
			await bot.send_message(user_id, "Не получилось добавить категорию. Попробуйте снова.")
		else:
			await bot.send_message(user_id, f"Добавили категорию {user_text}")

	# success or fail
	set_state(user_id, State.START)


# delete_category_text_handler
async def delete_category_text_handler(message: types.Message):
	user_id = message.from_user.id
	user_text = message.text

	user_categories = list_categories(user_id)

	if not (user_text in user_categories):
		await bot.send_message(user_id, f"Категории {user_text} не существует")
	else:
		try:
			delete_category(user_id, user_text)
		except:
			await bot.send_message(user_id, "Не получилось удалить категорию. Попробуйте снова.")
		else:
			await bot.send_message(user_id, f"Категория {user_text} была удалена")

	# success or fail
	set_state(user_id, State.START)


# media text handler
async def media_text_handler(message: types.Message):
	user_id = message.from_user.id
	user_text = message.text

	user_categories = list_categories(user_id)

	# user have sent media already
	# now clarifies category to put in

	if not (user_text in user_categories):
		await bot.send_message(user_id, f"Категории {user_text} не существует")
	else:
		upload_path = f"{media_path}/{user_id}/{user_text}"
		if media_messages.get(user_id) == None:
			media_messages[user_id] = []

		for media_message in media_messages.get(user_id):
			file_id = media_message.photo[-1].file_id
			await media_message.photo[-1].download(destination_file=f"{upload_path}/{file_id}")
		await bot.send_message(user_id, f"Фотография загружена в категорию {user_text}!!!")
		
	set_state(user_id, State.START)

	if media_messages[user_id] != None:
		media_messages[user_id].clear()


async def show_photos_text_handler(message: types.Message):
	user_id = message.from_user.id
	user_text = message.text

	user_categories = list_categories(user_id)

	# show photos from user_text category

	if not (user_text in user_categories):
		await bot.send_message(user_id, f"Категории {user_text} не существует")
	else:
		path = f"{media_path}/{user_id}/{user_text}"
		for photo_name in os.listdir(path):
			photo_path = f"{path}/{photo_name}"
			photo_data = open(photo_path, "rb")

			await bot.send_photo(user_id, photo_data)

	set_state(user_id, State.START)


async def simple_text_handler(message: types.Message):
	user_id = message.from_user.id
	user_text = message.text

	await bot.send_message(user_id, f"Нет такой команды {user_text}. Чтобы получить помощь нажмите /help")




@dp.message_handler()
async def text_handler(message: types.Message):
	user_id = message.from_user.id

	if get_user_state(user_id) == State.ADD_CATEGORY:
		await add_category_text_handler(message)
	elif get_user_state(user_id) == State.DELETE_CATEGORY:
		await delete_category_text_handler(message)
	elif get_user_state(user_id) == State.SEND_MEDIA:
		await media_text_handler(message)
	elif get_user_state(user_id) == State.SHOW_PHOTOS:
		await show_photos_text_handler(message)
	else:
		await simple_text_handler(message)




if __name__ == '__main__':
	print("started!")
	executor.start_polling(dp)