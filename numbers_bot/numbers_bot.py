from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import subprocess

popen_proc = ''
bot = Bot(token=<TOKKEN>)
dp = Dispatcher(bot) 

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    chat_id = message.chat.id
    global popen_proc
    popen_proc = subprocess.Popen(['python3', 'check_date.py', str(chat_id)])
    await message.answer(
        "Привет! Я бот буду присылать уведомления о заказах у которых прошел срок поставки\n"
        )

@dp.message_handler(commands=['stop'])
async def process_start_command(message: types.Message):
    chat_id = message.chat.id
    subprocess.Popen(['kill', str(popen_proc.pid)])
    await message.answer(
        "Отправка уведомлений завершена\n"
        )

async def send_notify(chat_id: int, message: str):
    await bot.send_message(chat_id, message)

if __name__ == '__main__':
    executor.start_polling(dp)
