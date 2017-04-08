# coding: utf-8

from slackbot.bot import respond_to
from slacker import Slacker
import slackbot_settings

# @respond_to("疲れた")
# @respond_to("つかれた")
# def cheer(message):
#     message.reply("ファイト！")

import MeCab
import random
import ChatBotScript
import SentenceGenerator
import datetime
import webbrowser
import time
import sys
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json
import requests
from requests.exceptions import Timeout
import os

def count(f_count):
    f_count += 1
    # count_talk = 0

def weather(message, something, number):
    try: citycode = sys.argv[1]
    except: citycode = '130010' #東京
    resp = urllib2.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read().decode('utf-8')

    # 読み込んだJSONデータをディクショナリ型に変換
    resp = json.loads(resp)
    # 明日の天気
    if number == 1:
        message.reply("私の住んでいるところ" + resp['title'][7:] + "は" + resp['forecasts'][1]['telop'] + "になると思います。")
    # 今日の天気
    else:
        message.reply("私の住んでいるところ" + resp['title'][7:] + "は" + resp['forecasts'][0]['telop'] + "です。")


#現在時刻
def time_now(message, something):
    todaydetail = datetime.datetime.today()
    message.reply("現在時刻は" + str(todaydetail.hour) + ":" + str(todaydetail.minute) + "です。")

#挨拶
# def greeting():
#     todaydetail = datetime.datetime.today()

#     if 4 <= todaydetail.hour <= 10:
#         message.reply(ChatBotScript.greeting[0] + symbol[random.randrange(2)])
#     elif 11 <= todaydetail.hour <= 17:
#         message.reply(ChatBotScript.greeting[1] + symbol[random.randrange(2)])
#     else:
#         message.reply(ChatBotScript.greeting[2])


# 天気の会話
def weather_talk():
    count_weather = 0
    count = 0
    # 入力
    @respond_to("(.*)")
    def sentence(message, something):
        global count_talk
        sentence = SentenceGenerator.sentence_generator(something)
        # \\\\\\\\\\
        # message.reply("----------変換後: " + sentence + "--weather--")
        # パターンマッチング
        if ("天気" in sentence or "晴れ" in sentence or "曇り" in sentence or "雨" in sentence) and ("?" in sentence or "？" in sentence or "何" in sentence) and ("明日" not in sentence):
            weather_talk.count_weather = 1
            weather(message, something, 0)
        elif ("天気" in sentence or "晴れ" in sentence or "曇り" in sentence or "雨" in sentence) and ("?" in sentence or "？" in sentence or "何" in sentence) and ("明日" in sentence):
            weather_talk.count_weather = 1                
            weather(message, something, 1)
        elif ("どこに" in sentence and "住んで" in sentence) or ("どこ住み" in sentence):
            message.reply("どこかです。")
        elif "リセット" in sentence:
            count_talk = 0
            main_talk()
        elif "晴れ" in sentence and "?" not in sentence and "？" not in sentence:
            message.reply(random.choice(ChatBotScript.sunny))
        elif "曇" in sentence and "?" not in sentence and "？" not in sentence:
            message.reply(random.choice(ChatBotScript.cloudy))
        elif "雨" in sentence and "?" not in sentence and "？" not in sentence:
            message.reply(random.choice(ChatBotScript.rainy))
        elif ("風" in sentence and "強い" in sentence) or ("強風" in sentence):
            message.reply("吹き飛ばされないように気をつけてくださいね")
        elif "台風" in sentence:
            message.reply(random.choice(ChatBotScript.typhoon))
        elif "元気" in sentence:
            message.reply(random.choice(ChatBotScript.physical_condition))
        elif "本当" in sentence and ("?" in sentence or "？" in sentence):
            message.reply(random.choice(ChatBotScript.response2))
        elif "今何時" in sentence:
            time_now(message, something)
        elif "元気" in sentence or ("本当" in sentence and ("?" in sentence or "？" in sentence)) or "朝食" in sentence or "昼食" in sentence or "晩飯" in sentence  or "夜食" in sentence or "食事" in sentence or "ご飯" in sentence or "ランチ" in sentence or "ディナー" in sentence or "かっこいい" in sentence or "かっこ良い" in sentence or "かわいい" in sentence or "高い" in sentence or "安い" in sentence or "難しい" in sentence or "簡単" in sentence or "面白" in sentence or "おもしろ" in sentence or "おいし" in sentence or "美味し" in sentence or (("体重" in sentence or "身長" in sentence or "スリーサイズ" in sentence) and ("?" in sentence or "？" in sentence)):
            weather_talk.count = 1
            main_talk()
        else:
            if weather_talk.count_weather == 1:
                weather_talk.count_weather += 1
                message.reply("今週の天気は安定しそうですか？")
            elif weather_talk.count_weather == 3:
                if "はい" in sentence or "よろ" in sentence or "お願い" in sentence or "調べて" in sentence:
                    message.reply("http://weather.yahoo.co.jp/weather/")
                    weather_talk.count = 1
                    main_talk()
                else:
                    message.reply("わかりました。何か別の話をしませんか？")
                    weather_talk.count = 1
                    talk.count_talk = 2
                    main_talk()
            else:
                weather_talk.count_weather = 3
                message.reply("天気を調べられるページのリンク載せましょうか？")


def food_talk():
    global f_count
    # 入力
    @respond_to("(.*)")
    def sentence(message, something):
        global f_count
        global count_talk
        sentence = SentenceGenerator.sentence_generator(something)
        # \\\\\\\\\\
        # message.reply("----------変換後: " + sentence + "--food--")

        if "ない" in sentence or "いや" in sentence:
            message.reply("では、おすすめの食べ物ありますか？")
            food_talk()
        elif "リセット" in sentence:
            count_talk = 0
            main_talk()
        elif "元気" in sentence or ("本当" in sentence and ("?" in sentence or "？" in sentence)) or "かっこいい" in sentence or "かっこ良い" in sentence or "かわいい" in sentence or "高い" in sentence or "安い" in sentence or "難しい" in sentence or "簡単" in sentence or "面白" in sentence or "おもしろ" in sentence or (("体重" in sentence or "身長" in sentence or "スリーサイズ" in sentence) and ("?" in sentence or "？" in sentence)):
            main_talk()
        else:
            if f_count == 0:
                message.reply("では、５つ質問をするので答えてください。答えていただいた条件から当てます。")
                message.reply("晩御飯の種類は？（スープ系・どんぶり系・定食系・パン系など）")
                f_count = 1
            elif f_count == 1:
                message.reply("晩御飯の味は？")
                f_count = 2
            elif f_count == 2:
                message.reply("晩御飯の色は？")
                f_count = 3
            elif f_count == 3:
                message.reply("晩御飯は温かいもの？冷たいもの？")
                f_count = 4
            elif f_count == 4:
                message.reply("晩御飯の食感は？")
                f_count = 5
            elif f_count == 5:
                message.reply("予測したメニューを送ります。正解ですか？")
                f_count = 0
                c_name = "guided_bot_test"
                f_path = "food_result.pdf"
                slacker = Slacker(slackbot_settings.API_TOKEN)
                def upload():
                    try:
                        slacker.files.upload(f_path, channels=[c_name], title="晩御飯の予測結果")
                    except requests.exceptions.Timeout:
                        print("Timeout occurred")
                        upload()
                upload()
                main_talk()

def work_talk():
    @respond_to("(.*)")
    def sentence(message, something):
        global count_talk
        sentence = SentenceGenerator.sentence_generator(something)
        if "いい" in sentence or "送って" in sentence or "確認" in sentence or "大丈夫" in sentence or "わか" in sentence:
            message.reply("ありがとうございます。確認よろしくお願いします。")
            c_name = "guided_bot_test"
            f_path = "work.pdf"
            slacker = Slacker(slackbot_settings.API_TOKEN)
            def upload():
                try:
                    slacker.files.upload(f_path, channels=[c_name], title="議事録")
                except requests.exceptions.Timeout:
                    print("Timeout occurred")
                    upload()
            upload()
            main_talk()
        elif "リセット" in sentence:
            count_talk = 0
            main_talk()
        else:
            message.reply("了解しました。別の機会にお願いします。")
            main_talk()


def main_talk():
    # 話題選択
    @respond_to("(.*)")
    def talk(message, something):
        global count_talk
        if count_talk == 0:
            message.reply("何のお話をしましょうか？")
            count_talk = 2
        elif count_talk == 1:
            message.reply("何の話ですか？")
        else:
            pass

        @respond_to("(.*)")
        def sentence(message, something):
            global count_talk
            sentence = SentenceGenerator.sentence_generator(something)
            # \\\\\\\\\\
            # message.reply("----------変換後: " + sentence + "--main--")
            if "天気" in sentence:
                message.reply("あなたの地域の今日の天気はどうですか？")
                weather_talk()
                count_talk = 1
            elif "食" in sentence or "飯" in sentence:
                message.reply("昨日の晩御飯が何か当てましょうか？")
                food_talk()
                count_talk = 1
            elif "仕事" in sentence or "職場" in sentence:
                message.reply("急な連絡ですみません。前回の会議の件で少し気になったことがあったので、今晩確認してもらいたいのですがよろしいでしょうか？よろしければ、気になった部分の資料をすぐに送りますので確認してください。")
                work_talk()
                count_talk = 1

#--------------
#-----メイン-----
#--------------

t_count = 0
f_count = 0
count_talk = 0
# count()
symbol = ["", "！", "？"]
main_talk()


