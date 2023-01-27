from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

CHANNEL_ID = -1001845349384
SUPER_USERS = (598564736, 731860478)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("шо ти хочеш")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("не можу")


# @dp.message_handler(chat_type=[types.ChatType.CHANNEL, types.ChatType.GROUP])
# async def group_handler(msg: types.Message):
#     logging.info("here is a group")
#     logging.info(msg)
#     await bot.send_message(-1001845349384, "hui")


@dp.message_handler(content_types=types.ContentType.all())
async def echo_message(msg: types.Message):
    logging.info("BP1")
    #check if vika
    if msg.from_user.id in SUPER_USERS:
        await bot.forward_message(CHANNEL_ID, msg.from_user.id, msg.message_id)
    else:
        await bot.send_message(msg.from_user.id, f"всі кажуть {msg.text}, а ти візьми і відрахуйся")


if __name__ == '__main__':
    executor.start_polling(dp)