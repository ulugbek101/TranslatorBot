from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup  # States
from telebot.storage import StateMemoryStorage

storage = StateMemoryStorage()


class WordTranslateState(StatesGroup):
    to_lang = State()
    word = State()
