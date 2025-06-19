from aiogram.types import Message, CallbackQuery

import datetime


async def respondEvent(event: Message | CallbackQuery, **kwargs) -> int:
    "Responds to various types of events: messages and callback queries."

    if isinstance(event, Message):
        bot_message = await event.answer(**kwargs)
    elif isinstance(event, CallbackQuery):
        bot_message = await event.message.edit_text(**kwargs)
        await event.answer()

    return bot_message.message_id


def makeGreetingMessage() -> str:
    "Generates a welcome message based on the current time of day."

    hour = datetime.datetime.now().hour

    if hour in range(0, 3+1) or hour in range(22, 23+1): # 22:00 - 3:00 is night
        greeting = '🌙 Good night'
    elif hour in range(4, 11+1): # 4:00 - 11:00 is morning
        greeting = '☕️ Good morning'
    elif hour in range(12, 17+1): # 12:00 - 17:00 is afternoon
        greeting = '☀️ Good afternoon'
    elif hour in range(18, 21+1): # 18:00 - 21:00 is evening
        greeting = '🌆 Good evening'
    else:
        greeting = '👋 Hello'
    
    return greeting
