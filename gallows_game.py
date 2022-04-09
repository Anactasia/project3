from data import db_session
import random
from data.world import Worlds
from data.Themes import Themes
from main import help

rez = []
world = []
qw = []


def get_game(update, context):
    global rez, world, qw
    answer = update.message.text.lower().split(' ')
    if 'нет' in answer:
        return help
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
                return get_game

            update.message.reply_text("Молодец, угадал!\n"
                                      f"Слово: {' '.join(qw)}")
        else:
            update.message.reply_text("Такой буквы нет."
                                      f"Слово: {' '.join(qw)}")
    else:
        update.message.reply_text("Это точно не одна буква.\n"
                                  "Напоминаю, 1 ход = 1 буква.")
    return 2

