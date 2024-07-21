import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, OPENWEATHER_API_KEY  # Не забудьте добавить ваш API-ключ в конфигурацию

bot = Bot(token=TOKEN)
router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, я бот! Введите команду /weather, чтобы получить прогноз погоды в Москве.")

@router.message(Command(commands=['help']))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /weather")

@router.message(Command(commands=['weather']))
async def weather(message: Message):
    weather_info = await get_weather()
    await message.answer(weather_info)

async def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={OPENWEATHER_API_KEY}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                description = data['weather'][0]['description']
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                weather_info = (f"Погода в Москве: {description}\n"
                                f"Температура: {temp}°C\n"
                                f"Ощущается как: {feels_like}°C\n"
                                f"Влажность: {humidity}%")
                return weather_info
            else:
                error_text = f"Ошибка получения данных: статус {response.status}."
                return error_text

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())