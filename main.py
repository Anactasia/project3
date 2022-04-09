# чат бот в телеграмме
# имя: @trtranan_bot


import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
import requests
from data import db_session
from data.world import Worlds
from data.Themes import Themes
import random
import t

rez = []
world = []
qw = []

API_KEY = '698b85e113937b14297f5582f941d0a7'  # ключ для API(выявление погоды)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5180202177:AAEFDmmGqMctktb_bOhrWNWjqj3ZbvWhnwg'  # Токен чат-бота

reply_keyboard = [['/weather']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update, context):
    print(1212)
    update.message.reply_text(
        "Привет. Я бот 'Pass the time'. А ты кто?",
    )
    return 1


def help(update, context):
    update.message.reply_text("Вот то, что я умею.\n"
                              "/weather - Скажу погоду из любого города\n"
                              "/game1 - игра-виселица\n"
                              "Это пока всё(")
    return ConversationHandler.END


def game1(update, context):
    update.message.reply_text("Игра-виселица.\n"
                              "Я загадываю слово, а ты угадываешь.\n"
                              "1 ход = 1 буква. 8 прав на ошибку\n"
                              "Are you ready ? Напиши Да или Нет"
                              )
    return 1


def get_game1(update, context):
    global rez, world, qw
    answer = update.message.text.lower().split(' ')
    print(answer, 34)
    if 'нет' in answer:
        return help(update, context)
    else:
        db_session.global_init("db/игра.db")
        db_sess = db_session.create_session()
        a = [world for world in db_sess.query(Worlds).all()]
        w = random.choice(a)
        worl = w.world
        print(w.id_theme)
        theme = db_sess.query(Themes).filter(Themes.id == w.id_theme).first().theme
        level = db_sess.query(Worlds).filter(Worlds.world == worl).first().complexity
        rez.append(worl)
        qw = list('_' * len(worl))
        world = list(worl)
        update.message.reply_text(f"Сложноть: {level}\n"
                                  f"Тема: {theme}\n"
                                  f"Слово: {' '.join(qw)}")
    return 2


def play_game1(update, context):
    global world, qw
    letter = update.message.text.lower()
    print(letter, world, qw)
    if letter.isalpha() and len(letter) == 1:
        if letter in world:
            while world.count(letter) != 0:
                qw[world.index(letter)] = letter.upper()
                world[world.index(letter)] = '_'
            if world.count('_') == len(world):
                update.message.reply_text("Поздравляю, слово разгадано\n"
                                          f"Слово: {' '.join(qw)}\n"
                                          "Хотите еще раз сыграть?\n"
                                          "Напишите Да или Нет.")
                return 1

            update.message.reply_text("Молодец, угадал!\n"
                                      f"Слово: {' '.join(qw)}")
        else:
            update.message.reply_text("Такой буквы нет.\n"
                                      f"Слово: {' '.join(qw)}")
    else:
        update.message.reply_text("Это точно не одна буква.\n"
                                  "Напоминаю, 1 ход = 1 буква.")
    return 2


# ПОГОДА
def weather(update, context):
    update.message.reply_text("Скажи любой город, а я скажу какая там погода.")
    return 3


# Выявление погоды указаного города
def get_weather(update, context):
    query = update.message.text
    print(query)
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
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url_photo, )
        update.message.reply_text(f"Город: {query.capitalize()}\n"
                                  f"Погодное условие: {conditions}\n"
                                  f"Температура: {temp} °C\n")
    else:
        update.message.reply_text("Или вы допустили ошибку, или я не знаю такой город.\n"
                                  "Проверте написание или укажите другой город")
    return 3


# знакомство с пользователям + показ команд чат бота
def first_response(update, context):
    context.user_data['name_user'] = update.message.text
    update.message.reply_text(
        f"Очень приятно, {context.user_data['name_user'].capitalize()}.\n"
        "Хочу вам рассказать, что я умею.\n"
        "/weather - Скажу погоду из любого города\n"
        "/game1 - игра-виселица\n"
        "Это пока всё(")
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, first_response)]},
        fallbacks=[CommandHandler('stop', help)]
    )
    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('weather', weather)],
        states={
            3: [MessageHandler(Filters.text & ~Filters.command, get_weather)]},
        fallbacks=[CommandHandler('stop', help)]
    )
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('game1', game1)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, get_game1)],
            2: [MessageHandler(Filters.text & ~Filters.command, play_game1)]},
        fallbacks=[CommandHandler('stop', help)]
    )
    dp.add_handler(conv_handler2)
    dp.add_handler(conv_handler)
    dp.add_handler(conv_handler1)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("ready", get_game1))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("close", close_keyboard))

    updater.start_polling()
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
