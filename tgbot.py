import telebot
from telebot import types
bot = telebot.TeleBot('5545425037:AAHX9cQ1hAGEPMPscnncuBAIRhY9e88FB-8')
import pickle
import os
from copy import copy

def mSend(text, mark = None):
    global idfrom
    if mark is not None:
        bot.send_message(idfrom, text, reply_markup = mark)
    else:
        bot.send_message(idfrom, text)


def send_rating(hero = None):
    global cur_user

    rf = open("rating.txt", 'r')

    if hero is not None:
        for line in rf:
            if f"Champion {hero}".lower() in line.lower():
                for i in range(2):
                    line += rf.readline()
                mSend(line)
                return 0
        mSend("Чемпион не найден")
        return 0
    if cur_user["start"] < 0:
        cur_user["start"] = 0
        cur_user["end"] = OFFSET_MOVE
    if cur_user["end"] > hero_count*per_hero_lines:
        cur_user["start"] = int(hero_count*per_hero_lines/OFFSET_MOVE)*OFFSET_MOVE
        cur_user["end"] = cur_user["start"] + OFFSET_MOVE
    flines = rf.readlines()[cur_user["start"]:cur_user["end"]]
    mSend("".join(flines))
    rf.close()



def createMarkUp(names = []):
    newMarkUp = types.ReplyKeyboardMarkup()
    hlpbtn = types.KeyboardButton("HELP")
    newMarkUp.row(hlpbtn)

    for name in names:
        newbtn = types.KeyboardButton(name)
        newMarkUp.row(newbtn)

    return newMarkUp


def save(data):
    with open(os.path.join("./","userbase.dict"), "wb") as f:
        pickle.dump(data, f)
        f.close()


def load():
    with open(os.path.join("./","userbase.dict"), "rb") as f:
        return pickle.load(f)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global idfrom
    global offset_start
    global offset_end
    global user_base
    global cur_user
    mtext = message.text
    idfrom = message.from_user.id

    if idfrom not in user_base:
        user_base[idfrom] = copy(USER_PARAMS)
    cur_user = user_base[idfrom]

    usermode = cur_user["mode"]

    if mtext.lower() in ["/start", "привет"]:
        cur_user["mode"] = ""
        mSend("Привет, чем я могу тебе помочь?", nav_markup)

    elif usermode == "":
        if mtext in ["/help", "HELP"]:
            mSend("RATING, NEXT, PREVIOUS, /rating [имя чемпиона]")
        elif len(mtext.split("rating ")) == 2:
            cur_hero = mtext.split("rating ")[1]
            send_rating(cur_hero)
        elif mtext in ["/rating", "RATING"]:
            cur_user["mode"] = "rating"
            mSend("Вы просматриваете рейтинг", rate_markup)
            send_rating()
        else:
            mSend("Я тебя не понимаю. Напиши /help.")
    elif usermode == "rating":
        if mtext == "NEXT":
            cur_user["start"] += OFFSET_MOVE
            cur_user["end"] += OFFSET_MOVE
            send_rating()
        elif mtext == "PREVIOUS":
            cur_user["start"] -= OFFSET_MOVE
            cur_user["end"] -= OFFSET_MOVE
            send_rating()
        elif mtext == "BACK":
            cur_user["mode"] = ""
            mSend("Вы закончили просмотр рейтинга", nav_markup)
    save(user_base)


user_base = {}

try:
    user_base = load()
except Exception as e:
    print("Не найден файл, создаю базу")
    save(user_base)

USER_PARAMS = {
    "nickname" : "",
    "mode" : "",
    "start" : 0,
    "end" : 30
}
OFFSET_MOVE = 30
cur_user = None
idfrom = None
offset_start = 0
offset_end = 30
nav_markup = createMarkUp(["RATING"])
rate_markup = createMarkUp(["NEXT", "PREVIOUS", "BACK"])
per_hero_lines = 3
hero_count = len(open("rating.txt", 'r').readlines())/per_hero_lines


bot.polling(none_stop=True, interval=0)