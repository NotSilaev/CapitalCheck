from config import settings

from handlers import common

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio


async def main() -> None:
    # Bot
    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    # Routers
    dp.include_router(common.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, RuntimeError):
        print('Bot has been stopped.')
