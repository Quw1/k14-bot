import logging
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types


TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

CHANNEL_ID = os.getenv('CHANNEL_ID')
SUPER_USERS = (598564736, 731860478, 223238862)

WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(dispatcher):
    await bot.delete_webhook()


#----------------------------------------------------------------

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("шо ти хочеш")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("не можу")



@dp.message_handler(content_types=types.ContentType.all())
async def echo_message(msg: types.Message):
    logging.info("BP1")
    #check if vika
    if msg.from_user.id in SUPER_USERS:
        await bot.forward_message(CHANNEL_ID, msg.from_user.id, msg.message_id)
    else:
        await bot.send_message(msg.from_user.id, f"всі кажуть {msg.text}, а ти візьми і відрахуйся")

#----------------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )