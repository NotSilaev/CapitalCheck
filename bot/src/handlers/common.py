import sys
sys.path.append('../') # src/

from logs import addLog
from exceptions import exceptions_catcher
from utils import respondEvent
from users import getUserName

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext


router = Router(name=__name__)


@router.message(CommandStart())
@router.callback_query(F.data == 'start')
@exceptions_catcher()
async def start(event: Message | CallbackQuery) -> None:
    user_id = event.from_user.id
    user_name: str = getUserName(user=event.from_user)

    message_text = (
        f'*👋 Welcome*, {user_name}\n\n'
        f'*CapitalCheck* — asset management service for an investment portfolio.'
    )

    await respondEvent(
        event,
        text=message_text, 
        parse_mode="Markdown",
    )
