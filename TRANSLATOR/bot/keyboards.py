from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import string

def generate_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="Переводчик"),
        KeyboardButton(text="Словарь")
    )
    return markup


def generate_lang_menu():
    markup = InlineKeyboardMarkup()
    langs = [
        ['en', 'English'],
        ['uz', 'O`zbek'],
        ['ru', 'Руссикй'],
        ['ar', 'arabic'],
        ['be', 'belarusian'],
        ['kk', 'kazakh'],
        ['ko', 'korean'],
        ['ja', 'japanese'],
        ['it', 'italian'],
        ['ky', 'kyrgyz']
    ]
    in_row = 2
    start = 0
    end = in_row
    rows = len(langs) // 2
    if rows % 2 != 0:
        rows += 1
    for _ in range(rows):
        btns = []
        for lang_code, language in langs[start:end]:
            btns.append(
                InlineKeyboardButton(text=language.capitalize(), callback_data=f"translating_to_{lang_code}")
            )
        start = end
        end += 2
        markup.row(*btns)
    return markup


def generate_cancel_any_state_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(text="❌ Отменить")
    )
    return markup


def generate_save_word_button(word: str):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Сохранить слово", callback_data=f"save_{word}")
    )
    return markup


def generate_words_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    # in_row = 2
    # start = 0
    # end = in_row
    # rows = len(words) // 2
    # if len(words) % 2 != 0:
    #     rows += 1
    #
    # for _ in range(rows):
    #     btns = []
    #     for word in words[start:end]:
    #         btns.append(
    #             KeyboardButton(text=word.capitalize())
    #         )
    #     markup.row(*btns)
    #     start = end
    #     end += start
    markup.row(
        KeyboardButton(text="❌ Очистить список слов")
    )
    markup.row(KeyboardButton(text="⬅ Главное меню"))
    return markup


def generate_alphabetical_menu():
    letters = [letter for letter in string.ascii_lowercase]
    markup = InlineKeyboardMarkup()
    in_row = 4
    start = 0
    end = in_row
    rows = len(letters) // 2
    if len(letters) % 2 != 0:
        rows += 1

    for _ in range(rows):
        btns = []
        for letter in letters[start:end]:
            btns.append(
                InlineKeyboardButton(text=letter.upper(), callback_data=f"str_letter_{letter}")
            )
        markup.row(*btns)
        start = end
        end += in_row
        # markup.row(
        #     InlineKeyboardButton(text="Все слова", callback_data=f"str_letters_{letters}")
        # )
    return markup.add().row(InlineKeyboardButton(text="Все слова", callback_data=f"str_letter_0"))





