import googletrans
import telebot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage

from forms import WordTranslateState
from keyboards import (generate_main_menu, generate_lang_menu, generate_cancel_any_state_btn, generate_save_word_button,
                       generate_words_keyboard, generate_alphabetical_menu)
from tools import save_word, clear_all_words, get_users_words, get_word

store2 = StateMemoryStorage()
TOKEN = "5361952560:AAHVi1TXpbsx394JxlaY8LreiBgajZD4ZQA"
bot = telebot.TeleBot(TOKEN, state_storage=store2)
translator = googletrans.Translator()
import sqlite3


@bot.message_handler(commands='start')
def start(message):
    bot.reply_to(message, f"Здравствуйте, {message.from_user.first_name}", reply_markup=generate_main_menu())


@bot.message_handler(func=lambda message: "Переводчик" in message.text)
def translation_start(message):
    bot.set_state(message.from_user.id, WordTranslateState.to_lang, message.chat.id)
    bot.send_message(message.from_user.id, "Выберите язык перевода: ", reply_markup=generate_lang_menu())


@bot.message_handler(state="*", commands='cancel')
@bot.message_handler(func=lambda message: "❌ Отменить" == message.text)
def cancel_any_state(message):
    bot.send_message(chat_id=message.chat.id, text="❎ Действия отменены", reply_markup=generate_main_menu())
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: "translating_to" in call.data)
def save_translating_lang(call):
    _, to, translating_lang = call.data.split("_")
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['to_lang'] = translating_lang
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.set_state(call.from_user.id, WordTranslateState.word, call.message.chat.id)
    bot.send_message(call.from_user.id, "Напишите слово или фразу для перевода",
                     reply_markup=generate_cancel_any_state_btn())


@bot.message_handler(state=WordTranslateState.word)
def save_translating_word(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['word'] = message.text
        to_lang = data['to_lang']
        word = data['word']

    detected_lang = translator.detect(text=word.lower()).__getattribute__("lang")

    translated_word = translator.translate(src=detected_lang, dest=to_lang, text=word).text
    bot.send_message(message.from_user.id,
                     text=f"<b>Слово: </b>{word.capitalize()}\n<b>Перевод: </b>{translated_word}",
                     reply_markup=generate_save_word_button(word=f"{word.lower()} -- {translated_word.lower()}"),
                     parse_mode="HTML")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: "Словарь" == message.text)
def show_alphabet_letters(message):
    bot.send_message(message.chat.id,
                     'Выберите букву, чтобы увидеть все слова начинающиеся с этой буквы\nВыберите "Все слова", чтобы увидеть все слова',
                     reply_markup=generate_alphabetical_menu())


@bot.callback_query_handler(func=lambda call: "str_letter" in call.data)
def show_all_users_words(call):
    letter = call.data.split("_")[2]
    if letter == "0":
        words = get_users_words(call.message.chat.id)
        if len(words) == 0:
            bot.send_message(call.message.chat.id, "Список ваших слов пока пуст !", reply_markup=generate_main_menu())
            bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            msg = "--- Список ваших слов: ---\n\n"
            i = 0
            for word in sorted(get_users_words(call.message.chat.id)):
                i += 1
                msg += f"{i}) {word.capitalize()}\n"
            bot.send_message(chat_id=call.message.chat.id, text=msg,
                             reply_markup=generate_words_keyboard())
            bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        words = sorted([word for word in get_users_words(call.message.chat.id) if word[0].lower() == letter.lower()])
        if len(words) == 0:
            bot.send_message(call.message.chat.id, "Список ваших слов пока пуст !", reply_markup=generate_main_menu())
            bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            msg = "--- Список ваших слов: ---\n\n"
            i = 0
            for word in words:
                i += 1
                msg += f"{i}) {word.capitalize()}\n"
            bot.send_message(chat_id=call.message.chat.id, text=msg,
                             reply_markup=generate_words_keyboard())


@bot.message_handler(func=lambda message: "❌ Очистить список слов" == message.text)
def clear_user_words(message):
    clear_all_words(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Список слов был успешно очищен !",
                     reply_markup=generate_main_menu())


@bot.callback_query_handler(func=lambda call: "save" in call.data)
def save_user_word(call):
    chat_id = call.message.chat.id
    word = call.data.split("_")[1]
    is_word_on_db = get_word(call.message.chat.id, word)
    if is_word_on_db is None:
        save_word(call.message.chat.id, f"{call.from_user.first_name} {call.from_user.last_name}", word)
        bot.answer_callback_query(call.id, "Слово успешно добавлено в список слов !")
        bot.send_message(chat_id, "Выберите режим", reply_markup=generate_main_menu())
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.message.chat.id, "Слово уже присутствует в списке слов !")
        bot.send_message(chat_id, "Выберите режим", reply_markup=generate_main_menu())
        # bot.delete_message(call.id, call.message.message_id)


@bot.message_handler()
def return_to_main_menu(message):
    if "⬅ Главное меню" == message.text:
        bot.send_message(message.chat.id, "Главное меню", reply_markup=generate_main_menu())
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю 😑")


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.infinity_polling()
