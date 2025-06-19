import sys
sys.path.append('../') # src/

from logs import addLog
from exceptions import exceptions_catcher
from utils import respondEvent

from database.tables.orders import OrdersTable

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


router = Router(name=__name__)


class Order(StatesGroup):
    asset = State()
    action = State()
    quantity = State()
    price = State()

    last_bot_message_id = State()


def makeOrderStructure(order_data: dict) -> str:
    structure_items = []
    for key, value in order_data.items():
        match key:
            case 'asset': structure_items.append(f'🪙 Asset: *{value}*')
            case 'action': structure_items.append(f'🔁 Action: *{value}*')
            case 'quantity': structure_items.append(f'💰 Quantity: *{value}*')
            case 'price': structure_items.append(f'💵 Price: *{value} $*')

    dash = '—'
    structure_items_string = '\n'.join(structure_items)
    order_structure = (
        f'{dash * 3} Order structure {dash * 3}\n'
        f'{structure_items_string}\n'
        f'{dash * 14}'
    )

    return order_structure


@router.callback_query(F.data == 'add_order')
async def add_order(call: CallbackQuery, state: FSMContext) -> None:
    "Form starter function."

    await specify_order_asset(call, state)



# Step 1: Specify asset
@router.callback_query(F.data == 'specify_order_asset')
@exceptions_catcher()
async def specify_order_asset(call: CallbackQuery, state: FSMContext) -> None:
    message_text = (
        '*➕ Order addition*\n\n'
        '🪙 Specify the asset name.'
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='❌ Cancel', callback_data='home')

    bot_message_id: int = (
        await respondEvent(
            call, 
            text=message_text, 
            parse_mode="Markdown", 
            reply_markup=keyboard.as_markup()
        )
    )

    await state.set_state(Order.asset)
    await state.update_data(last_bot_message_id=bot_message_id)


@router.message(Order.asset)
@exceptions_catcher()
async def set_order_asset(message: Message, state: FSMContext, bot: Bot) -> None:
    user_id = message.from_user.id
    user_message_id = message.message_id
    
    order_data = await state.get_data()
    last_bot_message_id = order_data['last_bot_message_id']

    await bot.delete_message(chat_id=user_id, message_id=user_message_id)
    await bot.delete_message(chat_id=user_id, message_id=last_bot_message_id)

    asset: str = message.text.upper()
    await state.update_data(asset=asset)

    await specify_order_action(message, state)
    


# Step 2: Specify action
@router.callback_query(F.data == 'specify_order_action')
@exceptions_catcher()
async def specify_order_action(event: Message | CallbackQuery, state: FSMContext) -> None:
    order_data: dict = await state.get_data()
    order_structure: str = makeOrderStructure(order_data)

    message_text = (
        '*➕ Order addition*\n\n'
        f'{order_structure}\n\n'
        '🔁 Select an action.'
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='🟢 Buy', callback_data='set_order_action-buy')
    keyboard.button(text='🔴 Sold', callback_data='set_order_action-sold')
    keyboard.button(text='⬅️ Go back', callback_data='specify_order_asset')
    keyboard.button(text='❌ Cancel', callback_data='home')
    keyboard.adjust(2)

    await respondEvent(
        event, 
        text=message_text, 
        parse_mode="Markdown", 
        reply_markup=keyboard.as_markup()
    )

    await state.set_state(Order.action)


@router.callback_query(F.data.startswith('set_order_action'))
@exceptions_catcher()
async def set_order_action(call: CallbackQuery, state: FSMContext) -> None:
    action: str = call.data.split('-')[1]
    await state.update_data(action=action)

    await specify_order_quantity(call, state)
    


# Step 3: Specify quantity
@router.callback_query(F.data == 'specify_order_quantity')
@exceptions_catcher()
async def specify_order_quantity(event: Message | CallbackQuery, state: FSMContext) -> None:
    order_data: dict = await state.get_data()
    order_structure: str = makeOrderStructure(order_data)

    message_text = (
        '*➕ Order addition*\n\n'
        f'{order_structure}\n\n'
        '💰 Specify the quantity of the asset.'
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='⬅️ Go back', callback_data='specify_order_action')
    keyboard.button(text='❌ Cancel', callback_data='home')
    keyboard.adjust(2)

    bot_message_id: int = (
        await respondEvent(
            event, 
            text=message_text, 
            parse_mode="Markdown", 
            reply_markup=keyboard.as_markup()
        )
    )

    await state.set_state(Order.quantity)
    await state.update_data(last_bot_message_id=bot_message_id)


@router.message(Order.quantity)
@exceptions_catcher()
async def set_order_quantity(message: Message, state: FSMContext, bot: Bot) -> None:
    user_id = message.from_user.id
    user_message_id = message.message_id

    order_data = await state.get_data()
    last_bot_message_id = order_data['last_bot_message_id']

    await bot.delete_message(chat_id=user_id, message_id=user_message_id)
    await bot.delete_message(chat_id=user_id, message_id=last_bot_message_id)

    raw_quantity: str = message.text.replace(',', '.')
    try:
        quantity = float(raw_quantity)
        await state.update_data(quantity=quantity)
        await specify_order_price(message, state)
    except ValueError:
        await specify_order_quantity(message, state)
    


# Step 4: Specify price
@router.callback_query(F.data == 'specify_order_price')
@exceptions_catcher()
async def specify_order_price(event: Message | CallbackQuery, state: FSMContext) -> None:
    order_data: dict = await state.get_data()
    order_structure: str = makeOrderStructure(order_data)

    message_text = (
        '*➕ Order addition*\n\n'
        f'{order_structure}\n\n'
        '💵 Specify the price of one asset unit.'
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='⬅️ Go back', callback_data='specify_order_quantity')
    keyboard.button(text='❌ Cancel', callback_data='home')
    keyboard.adjust(2)

    bot_message_id: int = (
        await respondEvent(
            event, 
            text=message_text, 
            parse_mode="Markdown", 
            reply_markup=keyboard.as_markup()
        )
    )

    await state.set_state(Order.price)
    await state.update_data(last_bot_message_id=bot_message_id)


@router.message(Order.price)
@exceptions_catcher()
async def set_order_quantity(message: Message, state: FSMContext, bot: Bot) -> None:
    user_id = message.from_user.id
    user_message_id = message.message_id
    
    order_data = await state.get_data()
    last_bot_message_id = order_data['last_bot_message_id']

    await bot.delete_message(chat_id=user_id, message_id=user_message_id)
    await bot.delete_message(chat_id=user_id, message_id=last_bot_message_id)

    raw_price: str = message.text.replace(',', '.')
    try:
        price = float(raw_price)
        await state.update_data(price=price)
        await create_order(message, state, is_confirmed=False)
    except ValueError:
        await specify_order_price(message, state)



# Order confirmation and creation
@exceptions_catcher()
async def create_order(event: Message | CallbackQuery, state: FSMContext, is_confirmed: bool = False) -> None:
    user_id = event.from_user.id

    order_data: dict = await state.get_data()
    order_structure: str = makeOrderStructure(order_data)

    if is_confirmed:
        OrdersTable.addOrder(
            user_id,
            asset=order_data['asset'],
            action=order_data['action'],
            quantity=order_data['quantity'],
            price=order_data['price'],
        )

        message_text = (
            '*✅ Order added*\n\n'
            f'{order_structure}'
        )

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='🏠 Go home page', callback_data='home')

    else:
        message_text = (
            '*➕ Order addition*\n\n'
            f'{order_structure}\n\n'
            '👀 Check the order structure and confirm its creation.'
        )

        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='☑️ Create order', callback_data='confirm_order_creation')
        keyboard.button(text='⬅️ Go back', callback_data='specify_order_price')
        keyboard.button(text='❌ Cancel', callback_data='home')
        keyboard.adjust(1, 2)

    await respondEvent(
        event, 
        text=message_text, 
        parse_mode="Markdown", 
        reply_markup=keyboard.as_markup()
    )


@router.callback_query(F.data == 'confirm_order_creation')
async def confirm_order_creation(call: CallbackQuery, state: FSMContext) -> None:
    await create_order(call, state, is_confirmed=True)
