import sys
sys.path.append('../') # src/

from logs import addLog
from exceptions import exceptions_catcher
from utils import respondEvent

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext


router = Router(name=__name__)

