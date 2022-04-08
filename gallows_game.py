from data import db_session
import random
from data.world import Worlds
from data.Themes import Themes

rez = []


def get_game1(update, context):
    global rez
    db_session.global_init("db/игра.db")
    db_sess = db_session.create_session()
    a = [world for world in db_sess.query(Worlds).all()]
    w = random.choice(a)
    world = w.world
    print(w.id_theme)
    theme = db_sess.query(Themes).filter(Themes.id == w.id_theme).first().theme
    level = db_sess.query(Worlds).filter(Worlds.world == world).first().complexity
    rez.append(world)
    update.message.reply_text(f"Сложноть: {level}\n"
                              f"Тема: {theme}\n"
                              f"Слово: {' '.join(list('_' * len(world)))}")


