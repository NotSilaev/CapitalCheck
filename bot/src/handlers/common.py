import sys
sys.path.append('../') # src/

from logs import addLog
from exceptions import exceptions_catcher
from utils import makeGreetingMessage, respondEvent
from users import doesUserExist, addUser, getUserName
from portfolio import makeUserPortfolioOverview

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

    user_exists: bool = doesUserExist(user_id)
    if not user_exists:
        addUser(user_id)

    message_text = (
        f'*👋 Welcome*, {user_name}\n\n'
        f'*CapitalCheck* — asset management service for an investment portfolio.'
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='🚀 Start using', callback_data='home')
    keyboard.button(text='ℹ️ More information', callback_data='info')
    keyboard.adjust(1)

    await respondEvent(
        event,
        text=message_text, 
        parse_mode="Markdown", 
        reply_markup=keyboard.as_markup()
    )
    

@router.message(F.text & (~F.text.startswith("/")), StateFilter(None))
@router.callback_query(F.data == 'home')
@exceptions_catcher()
async def home(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    user_id = event.from_user.id
    user_name: str = getUserName(user=event.from_user)

    greeting: str = makeGreetingMessage()
    portfolio_overview: str = makeUserPortfolioOverview(user_id)

    message_text = (
        f'*{greeting}*, {user_name}\n\n'
        f'{portfolio_overview}'
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='➕ Add order', callback_data='#')
    keyboard.button(text='🗂 Orders', callback_data='#')
    keyboard.button(text='💼 Portfolio', callback_data='#')
    keyboard.adjust(1)

    await respondEvent(
        event,
        text=message_text, 
        parse_mode="Markdown", 
        reply_markup=keyboard.as_markup()
    )
