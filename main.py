# чат бот в телеграмме
# имя: @trtranan_bot


import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
import requests
from gallows_game import get_game1
import t

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
    update.message.reply_text(
        "Я бот")


def game1(update, context):
    update.message.reply_text("Игра-виселица.\n"
                              "Я загадываю слово, а ты угадываешь.\n"
                              "1 ход = 1 буква. 8 прав на ошибку\n"
                              "Are you /ready ?"
                              )


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
        "game1 - игра-виселица\n"
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
        fallbacks=[CommandHandler('stop', stop)]
    )
    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('weather', weather)],
        states={
            3: [MessageHandler(Filters.text & ~Filters.command, get_weather)]},
        fallbacks=[CommandHandler('stop1', first_response)]
    )
    # conv_handler2 = ConversationHandler(
    #     entry_points=[CommandHandler('game1', game1)],
    #     states={
    #         3: [MessageHandler(Filters.text & ~Filters.command, get_game1)]},
    #     fallbacks=[CommandHandler('stop1', first_response)]
    # )
    # dp.add_handler(conv_handler2)
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
