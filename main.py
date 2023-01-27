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

CHANNEL_ID1 = os.getenv('CHANNEL_ID1')
CHANNEL_ID2 = os.getenv('CHANNEL_ID2')

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
async def reply_echo(msg: types.Message):
    await bot.send_message(msg.from_user.id, f"всі кажуть {msg.text}, а ти візьми і відрахуйся")


@dp.channel_post_handler(lambda message: message.chat.id == CHANNEL_ID1, content_types=types.ContentType.ANY)
async def echo_message(msg: types.Message):

    if msg.text:
        await bot.send_message(CHANNEL_ID2, msg.text)
    if msg.photo:
        ph = msg.photo
        await bot.send_photo(CHANNEL_ID2, ph[len(ph) - 1].file_id, caption=msg.caption)
    elif msg.document:
        doc = msg.document
        await bot.send_document(CHANNEL_ID2, doc.file_id, caption = msg.caption)
    else:
        await bot.forward_message(CHANNEL_ID2, msg.chat.id, msg.message_id)

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