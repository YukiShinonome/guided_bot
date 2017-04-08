# coding: utf-8

from slackbot.bot import listen_to
import random
import ChatBotScript
import SentenceGenerator
import datetime
 
# @listen_to('あきらめたら')
# @listen_to('諦めたら')
# def anzai(message):
#     message.send('そこで試合終了ですよ。')
 
# @listen_to('いいですか')
# def reaction(message):
#     message.react('+1')

symbol = ["", "！", "？"]

#挨拶
def greeting(message, something):
    todaydetail = datetime.datetime.today()
    if 4 <= todaydetail.hour <= 10:
        message.reply(ChatBotScript.greeting[0] + symbol[random.randrange(2)])
    elif 11 <= todaydetail.hour <= 17:
        message.reply(ChatBotScript.greeting[1] + symbol[random.randrange(2)])
    else:
        message.reply(ChatBotScript.greeting[2])

#現在時刻
def time_now(message, something):
    todaydetail = datetime.datetime.today()
    message.reply("現在時刻は" + str(todaydetail.hour) + ":" + str(todaydetail.minute) + "です。")

@listen_to("(.*)")
def sentence(message, something):
    sentence = SentenceGenerator.sentence_generator(something)
    if("おはよう" in sentence or "こんにち" in sentence or "こんばん" in sentence):
        greeting(message, something)
    elif "疲れ" in sentence:
        message.reply("お疲れ様です(´ー｀)")
    elif "時間" in sentence:
        time_now(message, something)
    elif "類義語" in something:
        word = something[:-4]
        synonym = []
        synonym = SentenceGenerator.synonymwords(word)
        message.reply(synonym)