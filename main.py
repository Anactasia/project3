# чат бот в телеграмме
# имя: @trtranan_bot
import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
import requests
from data import db_session
from data.word import Words
from data.Themes import Themes
import random
import t
import json
import urllib.parse

API_KEY = '698b85e113937b14297f5582f941d0a7'  # ключ для API(выявление погоды)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5180202177:AAEFDmmGqMctktb_bOhrWNWjqj3ZbvWhnwg'  # Токен чат-бота
# TOKEN = '5216550043:AAFqTgbQys_J2zQliL24uqpIqMDN86i8OWY'

attempts = 0
words_used = []
word = []
spell_word = []


def start(update, context):
    print(1212)
    update.message.reply_text(
        "Привет. Я бот 'Pass the time'. А ты кто?",
    )
    return 0


# знакомство с пользователям + показ команд чат бота
def first_response(update, context):
    context.user_data['name_user'] = update.message.text
    update.message.reply_text(
        f"Очень приятно, {context.user_data['name_user'].capitalize()}.\n"
        "Хочу вам рассказать, что я умею: \n"
        "Помощь\n"
        "/weather - скажу погоду из любого города\n"
        "/market_buy - найду тебе товар на маркете\n"
        "/main_menu - главное меню\n"
        "\n"
        "Развлечения\n"
        "/gallows - игра-виселица\n"
        "/true_or_false - игра 'правда или ложь'\n"
        "\n"
        "Это пока всё, но я стараюсь развиваться(\n"
        "\n"
        "Точно, чуть не забыл, у меня есть подарок для тебя,\n"
        "Чтоб его получить отправь кодовое слово из 6 букв.\n"
        "Буквы этого слова можно найти во всех моих функциях\n"
        "—ฅ/ᐠ. ̫ .ᐟ\ฅ — P"
    )
    return 11


def checking_messages_menu(update, context):
    message = update.message.text.lower()
    if 'виселиц' in message:
        update.message.reply_text("Может быть вы хотите это:\n"
                                  "/gallows - игра-виселица")
    elif 'погод' in message:
        update.message.reply_text("Может быть вы хотите это:\n"
                                  "/weather - скажу погоду из любого города")
    elif 'правд' in message or 'лож' in message:
        update.message.reply_text("Может быть вы хотите это:\n"
                                  "/true_or_false - игра 'правда или ложь'")
    elif 'покупк' in message or 'купит' in message or 'покуп' in message:
        update.message.reply_text("Может быть вы хотите это:\n"
                                  "/market_buy - найду тебе товар на маркете")
    elif ('ты' in message and 'кто' in message) or ('как' in message and 'зовут' in message):
        update.message.reply_text("Я бот 'Pass the time'")
    elif 'я' in message and 'люблю' in message:
        update.message.reply_text("Это здорово\n"
                                  "А я люблю котиков\n"
                                  "/ᐠ ̥    ̣̮ ̥ ᐟ\ﾉ")
    elif 'расска' in message and 'себе' in message:
        update.message.reply_text("Ну... я чат-бот\n"
                                  "Ещё маленький конечно, но я стараюсь развиваться\n"
                                  "Я люблю котиков(просто без ума от них)\n")
    elif message == 'python':
        update.message.reply_text("Хе-хе-хе\n"
                                  "Лови небольшой стикерпак от моих разработчиков.\n"
                                  "https://t.me/addstickers/kitten_pass_the_time")
        context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker=r"CAACAgIAAxkBAAEEf8ViXG3M2EWheedw1HAPWlxzbAbF9gACHBsAAsq04EqC3yEVv_ngiSQE")

    elif message[0] != '/':
        update.message.reply_text("Или я это ещё не умею,\n"
                                  "Или я вас не понимаю(извините)\n"
                                  "/ᐠᵕ̩̩̥ ‸ᵕ̩̩̥ ᐟ\ﾉ")

    if '/' not in message:
        return 11
    else:
        if '/weather' == message:
            return weather(update, context)
        elif '/gallows' == message:
            return gallows(update, context)
        elif '/true_or_false' == message:
            return get_tof(update, context)
        elif '/market_buy' == message:
            return market_buy(update, context)
        elif '/main_menu' == message:
            return help(update, context)


def help(update, context):
    update.message.reply_text("Вот то, что я умею: \n"
                              "Помощь\n"
                              "/weather - скажу погоду из любого города\n"
                              "/market_buy - найду тебе товар на маркете\n"
                              "/main_menu - главное меню\n"
                              "\n"
                              "Развлечения\n"
                              "/gallows - игра-виселица\n"
                              "/true_or_false - игра 'правда или ложь'\n"
                              "\n"
                              "Это пока всё, но я стараюсь развиваться(\n"
                              "—ฅ/ᐠ. ̫ .ᐟ\ฅ — T")
    return 11


def gallows(update, context):
    global words_used, spell_word, attempts
    exit = [['Выход'], ['Да'], ['Нет']]
    s = ReplyKeyboardMarkup(exit, one_time_keyboard=True)
    attempts = 0
    words_used = []
    spell_word = []
    update.message.reply_text("Игра-виселица.\n"
                              "Я загадываю слово, а ты угадываешь.\n"
                              "1 ход = 1 буква. 8 прав на ошибку\n"
                              "Are you ready ? Напиши Да или Нет\n"
                              "Если надоест, можешь в любой момент нажать на кнопку 'Выход'",
                              reply_markup=s
                              )
    return 1


def get_game1(update, context):
    global words_used, word, spell_word, attempts
    exit = [['Выход']]
    s = ReplyKeyboardMarkup(exit, one_time_keyboard=True)
    attempts = 0
    spell_word = []
    answer = update.message.text.lower()
    print(answer)
    if 'нет' in answer:
        return help(update, context)
    elif 'выход' in answer or '/main_menu' in answer:
        return help(update, context)
    elif 'да' in answer:
        db_session.global_init("db/игра.db")
        db_sess = db_session.create_session()
        a = [i for i in db_sess.query(Words).filter(Words.word.notin_(words_used))]
        print(a)
        if len(a) == 0:
            update.message.reply_text("К сожелению, вы разгадали уже все слова(\n"
                                      "Я постараюсь в следующий раз выучить побольше слов.\n"
                                      "/main_menu - главное меню",
                                      reply_markup=s
                                      )
            return 1
        else:
            w = random.choice(a)
            wor = w.word
            print(w.id_theme)
            theme = db_sess.query(Themes).filter(Themes.id == w.id_theme).first().theme
            level = db_sess.query(Words).filter(Words.word == wor).first().complexity
            words_used.append(wor)
            spell_word = list('_' * len(wor))
            word = list(wor)
            update.message.reply_text(f"Сложноть: {level}\n"
                                      f"Тема: {theme}\n"
                                      f"Слово: {' '.join(spell_word)}",
                                      reply_markup=s
                                      )
            return 2
    elif '/' in answer:
        update.message.reply_text("Если вы пытаетесь вызвать команду\n"
                                  "То нужно сначала выйти в главное меню\n"
                                  "/main_menu или кнопка 'Выход'"

                                  )
        return 1
    else:
        update.message.reply_text("К сожелению, я вас не понимаю\n"
                                  "Ответьте, хотите ли вы играть?\n"
                                  "Да или Нет",

                                  )

        return 1


def play_game1(update, context):
    global word, spell_word, attempts, words_used
    exit = [['Выход']]
    s = ReplyKeyboardMarkup(exit, one_time_keyboard=True)
    letter = update.message.text.lower()
    if 'выход' in letter or '/main_menu' in letter:
        return help(update, context)
    letter = update.message.text.lower()
    if letter.isalpha() and len(letter) == 1:
        if letter not in word and letter.upper() in spell_word:
            update.message.reply_text("Да, такая буква есть, но вы её уже угадали.\n"
                                      f"Слово: {' '.join(spell_word)}",
                                      )
        elif letter in word:
            while word.count(letter) != 0:
                spell_word[word.index(letter)] = letter.upper()
                word[word.index(letter)] = '_'
            if word.count('_') == len(word):
                exit = [['Выход'], ['Да'], ['Нет']]
                s = ReplyKeyboardMarkup(exit, one_time_keyboard=True)

                context.bot.send_photo(chat_id=update.effective_chat.id,
                                       photo=open('img/кот_с_пальцем.jpg', 'rb'),
                                       caption="Поздравляю, слово разгадано\n"
                                               f"Слово: {' '.join(spell_word)}\n"
                                               "Хотите еще раз сыграть?\n"
                                               "Напишите Да или Нет.\n"
                                               "—ฅ/ᐠ. ̫ .ᐟ\ฅ — H",
                                       reply_markup=s)
                return 1

            update.message.reply_text("Молодец, угадал!\n"
                                      f"Слово: {' '.join(spell_word)}"
                                      )
        else:
            stroc = ''
            q = 7 - attempts
            if q != 0:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f'img/{attempts + 1}.jpg', 'rb'))
                attempts += 1
                if q in [7, 6, 5]:
                    stroc = 'попыток'
                elif q in [4, 3, 2]:
                    stroc = 'попытки'
                elif q == 1:
                    stroc = 'попытка'
                update.message.reply_text("Упс... Такой буквы нет.\n"
                                          f"Слово: {' '.join(spell_word)}\n"
                                          f"У тебя осталось {q} {stroc}"
                                          )
            else:
                exit = [['Выход'], ['Да'], ['Нет']]
                s = ReplyKeyboardMarkup(exit, one_time_keyboard=True)
                context.bot.send_photo(chat_id=update.effective_chat.id,
                                       photo=open('img/кот_немного_плачет.jpg', 'rb'),
                                       caption="Попытки кончились.\n"
                                               f"Это было слово: {words_used[-1].upper()}\n"
                                               "Хочешь ещё раз попробывать?\n"
                                               "Напиши Да или Нет.\n"
                                               "—ฅ/ᐠ. ̫ .ᐟ\ฅ — H",
                                       reply_markup=s)
                return 1
    elif '/' in letter:
        update.message.reply_text("Если вы пытаетесь вызвать команду\n"
                                  "То нужно сначала выйти в главное меню\n"
                                  "/main_menu или кнопка 'Выход'"

                                  )
    else:
        update.message.reply_text("Это точно не одна буква.\n"
                                  "Напоминаю, 1 ход = 1 буква."
                                  )
    return 2


# ПОГОДА
def weather(update, context):
    exit = [['Выход']]
    s = ReplyKeyboardMarkup(exit, one_time_keyboard=True)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('img/кот_с_зонтом.jpg', 'rb'))
    update.message.reply_text("Скажи любой город, а я скажу какая там погода.\n"
                              "Если надоест, можешь в любой момент нажать на кнопку 'Выход'\n"
                              "—ฅ/ᐠ. ̫ .ᐟ\ฅ — Y",
                              reply_markup=s
                              )
    return 3


# Выявление погоды указаного города
def get_weather(update, context):
    exit = [['Выход']]
    s = ReplyKeyboardMarkup(exit, one_time_keyboard=True)
    query = update.message.text.lower()
    if 'выход' == query or '/main_menu' in query:
        return help(update, context)
    if not query:
        query = 'fetch:ip'
    response = requests.get("http://api.openweathermap.org/data/2.5/find",
                            params={'q': query, 'type': 'like', 'units': 'metric', 'APPID': API_KEY})
    data = response.json()
    if data['list'] != []:
        data = response.json()
        print(data, 43)
        conditions = t.translation(data['list'][0]['weather'][0]['description'])
        print(data, 43)
        temp = round(int(data['list'][0]['main']['temp']))
        icon = data['list'][0]['weather'][0]['icon']
        url_photo = f"http://openweathermap.org/img/wn/{icon}@2x.png"

        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=url_photo,
                               caption=f"Город: {query.capitalize()}\n"
                                       f"Погодное условие: {conditions}\n"
                                       f"Температура: {temp} °C\n")
    elif '/' in query:
        update.message.reply_text("Если вы пытаетесь вызвать команду\n"
                                  "То нужно сначала выйти в главное меню\n"
                                  "/main_menu или кнопка 'Выход'"

                                  )
        return 1
    else:
        update.message.reply_text("Или вы допустили ошибку, или я не знаю такой город.\n"
                                  "Проверьте написание или укажите другой город")
    return 3


def get_tof(update, context):
    button = [["Да", "Нет", "Выход"]]
    m = ReplyKeyboardMarkup(button, one_time_keyboard=True)
    # context.user_data['name_user'] = update.message.text
    update.message.reply_text(
        f"Рад приветствовать на игре 'Правда или Ложь', {context.user_data['name_user'].capitalize()}.\n"
        "Правила игры: \n"
        "Я рассказываю интересный факт, а ты угадываешь: правда это или ложь.\n"
        "За каждый правильный ответ начисляется один балл. "
        "В конце я подведу итоги и выведу количество правильных ответов. \n"
        "\n"
        "Все довольно просто, начинаем?\n"
        "Выберите, да или нет\n"
        "\n"
        "Если надоест, можешь в любой момент нажать на кнопку 'Выход'",
        reply_markup=m)
    return 4


def tof_check_answer(update, context):
    answer = update.message.text.lower()
    if answer == "да":
        with open("data/tof.json", 'r', encoding='utf8') as f:
            context.user_data['tof_data'] = json.load(f)
        print(json.dumps(context.user_data['tof_data'], indent=2))
        q = context.user_data['tof_data']['data'][0]
        context.user_data['tof_is_first_answer'] = True
        context.user_data['tof_quest'] = q['quest']
        context.user_data['tof_answer'] = q['answer']
        context.user_data['tof_dop'] = q['dop']
        context.user_data['tof_file'] = q['file']
        context.user_data['tof_bal'] = 0
        buttons = [['Правда', 'Ложь', 'Выход']]
        m = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=open(context.user_data['tof_file'], 'rb'),
                               caption=f"Итак, факт!\n\n{q['quest']}\n",
                               reply_markup=m)

        return 5

    elif '/' in answer:
        update.message.reply_text("Если вы пытаетесь вызвать команду\n"
                                  "То нужно сначала выйти в главное меню\n"
                                  "/main_menu или кнопка 'Выход'"
                                  )
        return 4
    elif 'выход' == answer or '/main_menu' in answer or 'нет' == answer:
        return help(update, context)

    else:
        update.message.reply_text("К сожалению, я вас не понимаю\n"
                                  "Выберите, да или нет")
        return 4


def tof_is_right_answer(context, answer):
    a = False
    if answer == 'правда':
        a = True
    if a == context.user_data['tof_answer']:
        return True
    else:
        return False


def true_or_false(update, context):
    answer = update.message.text.lower()
    if 'выход' == answer or '/main_menu' in answer:
        return help(update, context)
    if tof_is_right_answer(context, answer):
        update.message.reply_text(f"Верно, поздравляю, вам +1 балл! \n")
        context.user_data['tof_bal'] += 1
    else:
        update.message.reply_text(f"К сожалению, вы ошиблись.\n"
                                  "\n"
                                  f"{context.user_data['tof_dop']}")

    if context.user_data['tof_is_first_answer']:
        del context.user_data['tof_data']['data'][0]
        context.user_data['tof_is_first_answer'] = False

    if len(context.user_data['tof_data']['data']) > 0:
        buttons = [['Правда'], ['Ложь'], ['Выход']]
        r = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
        q = context.user_data['tof_data']['data'].pop()
        context.user_data['tof_quest'] = q['quest']
        context.user_data['tof_answer'] = q['answer']
        context.user_data['tof_dop'] = q['dop']
        context.user_data['tof_file'] = q['file']
        print(q)
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=open(context.user_data['tof_file'], 'rb'),
                               caption=f"Итак, факт!\n\n{q['quest']}\n",
                               reply_markup=r)
    else:
        update.message.reply_text(
            f"Вы прошли игру и набрали балл: {context.user_data['tof_bal']}!\n"
            "/main_menu - главное меню\n"
            "—ฅ/ᐠ. ̫ .ᐟ\ฅ — N"
        )
        return 5


def market_buy(update, context):
    exit = [['Выход']]
    s = ReplyKeyboardMarkup(exit, one_time_keyboard=True)
    update.message.reply_text("Введи название товара, который хочешь найти\n"
                              "Если надоест, можешь в любой момент нажать на кнопку 'Выход'\n"
                              "—ฅ/ᐠ. ̫ .ᐟ\ฅ — O",
                              reply_markup=s
                              )
    return 6


def market_search(update, context):
    we = update.message.text
    tovar = urllib.parse.quote(update.message.text)
    print(tovar)
    if we.lower() == 'выход' or we.lower() == '/main_menu':
        return help(update, context)
    else:
        update.message.reply_text(
            'Вот ссылки на различные интернет-магазины! \n'
            '\n'
            'Яндекс-маркет: \n'
            f'https://market.yandex.ru/search?text={tovar}\n'
            '\n'
            'Озон: \n'
            f'https://www.ozon.ru/search?text={tovar}\n'
            '\n'
            'Алиэкспресс: \n'
            f'https://aliexpress.ru/wholesale?catId=&SearchText={tovar}\n'
        )
    return 6


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={0: [MessageHandler(Filters.text & ~Filters.command, first_response, pass_user_data=True)],
                11: [MessageHandler(Filters.text, checking_messages_menu, pass_user_data=True)],
                12: [MessageHandler(Filters.text, help, pass_user_data=True)],

                100: [MessageHandler(Filters.text & ~Filters.command, weather, pass_user_data=True)],
                3: [MessageHandler(Filters.text, get_weather)],

                101: [MessageHandler(Filters.text & ~Filters.command, gallows, pass_user_data=True)],
                1: [MessageHandler(Filters.text, get_game1)],
                2: [MessageHandler(Filters.text, play_game1)],

                102: [MessageHandler(Filters.text & ~Filters.command, get_tof, pass_user_data=True)],
                4: [MessageHandler(Filters.text, tof_check_answer, pass_user_data=True)],
                5: [MessageHandler(Filters.text, true_or_false, pass_user_data=True)],

                103: [MessageHandler(Filters.text & ~Filters.command, market_buy, pass_user_data=True)],
                6: [MessageHandler(Filters.text & ~Filters.command, market_search)]

                },
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(start_handler)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gallows", gallows))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("ready", get_game1))
    dp.add_handler(CommandHandler("main_menu", help))
    dp.add_handler(CommandHandler("true_or_false", get_tof))
    dp.add_handler(CommandHandler("market_buy", market_buy))

    updater.start_polling()
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
