from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiohttp import ClientSession
import json

from configs import token


bot = Bot(token=token)
dp = Dispatcher(bot)

btn_btc_usdt, btn_eth_usdt = KeyboardButton('btc_usdt'), KeyboardButton('eth_usdt')
btn_start, btn_help = KeyboardButton('/start'), KeyboardButton('/help')
bot_keyboard = ReplyKeyboardMarkup()
bot_keyboard.add(btn_btc_usdt, btn_eth_usdt, btn_start, btn_help)


async def get_price(symbol1: str = 'BTC', symbol2: str = 'USDT'):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol1}{symbol2}'
    async with ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
    return json.loads(data)


def prepare_answer(data: dict):
    return '\n'.join(f'{key}: {value}' for key, value in data.items())


@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    if 'start' in message.text:
        await message.reply(text='Hello\nWelcome to the CryptoBot',
                            reply_markup=bot_keyboard)
    elif 'help' in message.text:
        await message.reply(text='what can i help you?',
                            reply_markup=bot_keyboard)


@dp.message_handler()
async def response_messages(message: types.Message):
    try:
        currency1, currency2 = message.text.upper().split('_')
        data = await get_price(currency1, currency2)

        await bot.send_message(message.from_user.id, prepare_answer(data))
    except ValueError:
        await message.reply(text='bad command! ',
                            reply_markup=bot_keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
