import telebot
from telebot import types
bot = telebot.TeleBot('5545425037:AAHX9cQ1hAGEPMPscnncuBAIRhY9e88FB-8')

def mSend(text, mark = None):
    global idfrom
    if mark is not None:
        bot.send_message(idfrom, text, reply_markup = mark)
    else:
        bot.send_message(idfrom, text)


def send_rating(os, oe, hero = None):
    global offset_start
    global offset_end
    rf = open("rating.txt", 'r')
    if hero is not None:
        for line in rf:
            if f"Champion {hero}".lower() in line.lower():
                mSend(line)
                return 0
        mSend("Чемпион не найден")
        return 0
    if os < 0:
        offset_start = 0
        offset_end = 10
    if os > hero_count:
        offset_start = int(hero_count/10)*10
        offset_end = offset_start + 10
    flines = rf.readlines()[offset_start:offset_end]
    mSend("\n".join(flines))
    rf.close()

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global idfrom
    global offset_start
    global offset_end
    mtext = message.text
    idfrom = message.from_user.id
    if mtext.lower() in ["/start", "привет"]:
        mSend("Привет, чем я могу тебе помочь?", nav_markup)
    elif mtext in ["/help", "HELP"]:
        mSend("RATING, NEXT, PREVIOUS, /rating [имя чемпиона]")
    elif mtext == "NEXT":
        offset_start += 10
        offset_end += 10
        send_rating(offset_start, offset_end)
    elif mtext == "PREVIOUS":
        offset_start -= 10
        offset_end -= 10
        send_rating(offset_start, offset_end)
    elif len(mtext.split("rating ")) == 2:
        cur_hero = mtext.split("rating ")[1]
        send_rating(offset_start, offset_end, cur_hero)
    elif mtext in ["/rating", "RATING"]:
        send_rating(offset_start, offset_end)
    else:
        mSend("Я тебя не понимаю. Напиши /help.")

def createMarkUp(names = []):
    newMarkUp = types.ReplyKeyboardMarkup()
    hlpbtn = types.KeyboardButton("HELP")
    newMarkUp.row(hlpbtn)

    for name in names:
        newbtn = types.KeyboardButton(name)
        newMarkUp.row(newbtn)

    return newMarkUp


idfrom = None
offset_start = 0
offset_end = 10
nav_markup = createMarkUp(["NEXT", "PREVIOUS", "RATING"])
hero_count = len(open("rating.txt", 'r').readlines())


bot.polling(none_stop=True, interval=0)