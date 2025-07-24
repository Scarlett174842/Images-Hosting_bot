import os
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.markdown import hlink
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram import F
from aiogram.runner import run_polling

BOT_TOKEN = "7655555394:AAGLTyM7rrXR3pb__r4IfH6zhi4hfCdNoa4"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

logging.basicConfig(level=logging.INFO)

@router.message(F.photo)
async def handle_photo(message: Message, bot: Bot):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            if resp.status != 200:
                await message.reply("❌ Не удалось загрузить фото.")
                return
            file_bytes = await resp.read()

        form = aiohttp.FormData()
        form.add_field('file', file_bytes, filename='image.jpg', content_type='image/jpeg')

        async with session.post('https://telegra.ph/upload', data=form) as response:
            result = await response.json()

        if 'error' in result:
            await message.reply("❌ Ошибка загрузки на telegra.ph.")
            return

        telegraph_url = 'https://telegra.ph' + result[0]['src']
        await message.reply(f"✅ Готово!\n{telegraph_url}")

if __name__ == "__main__":
    bot = Bot(token=BOT_TOKEN, session=AiohttpSession())
    run_polling(dp, bot=bot)
