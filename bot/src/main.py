from config import settings

from handlers import common, orders
from handlers.forms import add_order_form

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio


async def main() -> None:
    # Bot
    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    # Handlers routers
    dp.include_router(common.router)
    dp.include_router(orders.router)

    # Forms routers
    dp.include_router(add_order_form.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, RuntimeError):
        print('Bot has been stopped.')
