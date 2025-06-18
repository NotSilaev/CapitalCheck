from aiogram.types import Message, CallbackQuery

import datetime


async def respondEvent(event: Message | CallbackQuery, **kwargs):
    "Responds to various types of events: messages and callback queries."

    if isinstance(event, Message):
        await event.answer(**kwargs)
    elif isinstance(event, CallbackQuery):
        await event.message.edit_text(**kwargs)
        await event.answer()
