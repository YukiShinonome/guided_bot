# coding: utf-8

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

def weather(number):
    try: citycode = sys.argv[1]
    except: citycode = '130010' #東京
    resp = urllib2.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read().decode('utf-8')

    # 読み込んだJSONデータをディクショナリ型に変換
    resp = json.loads(resp)
    # 明日の天気
    if number == 1:
        print("BOT: " + "私の住んでいるところ" + resp['title'][7:] + "は" + resp['forecasts'][1]['telop'] + "になると思います。")
    # 今日の天気
    else:
        print("BOT: " + "私の住んでいるところ" + resp['title'][7:] + "は" + resp['forecasts'][0]['telop'] + "です。")

# weather(0)
# weather(1)



#現在時刻
def time_now():
    todaydetail = datetime.datetime.today()
    print("BOT: " + "現在時刻は" + str(todaydetail.hour) + ":" + str(todaydetail.minute) + "です。")

#挨拶
def greeting():
    todaydetail = datetime.datetime.today()

    if 4 <= todaydetail.hour <= 10:
        print("BOT:" + ChatBotScript.greeting[0] + symbol[random.randrange(2)])
    elif 11 <= todaydetail.hour <= 17:
        print("BOT:" + ChatBotScript.greeting[1] + symbol[random.randrange(2)])
    else:
        print("BOT:" + ChatBotScript.greeting[2])


# 天気の会話
def weather_talk():
    count_weather = 1
    while True:
        # 入力
        speech = input("user: ")
        sentence = SentenceGenerator.sentence_generator(speech)
        # \\\\\\\\\\
        print("----------変換後: " + sentence)

        # パターンマッチング
        if ("天気" in sentence or "晴れ" in sentence or "曇り" in sentence or "雨" in sentence) and ("?" in sentence or "？" in sentence or "何" in sentence) and ("明日" not in sentence):
            weather(0)
        elif ("天気" in sentence or "晴れ" in sentence or "曇り" in sentence or "雨" in sentence) and ("?" in sentence or "？" in sentence or "何" in sentence) and ("明日" in sentence):
            count_weather = 1
            weather(1)
        elif ("どこに" in sentence and "住んで" in sentence) or ("どこ住み" in sentence):
            print("BOT: " + "どこかです。")
        elif "晴れ" in sentence and "?" not in sentence and "？" not in sentence:
            print("BOT: " + random.choice(ChatBotScript.sunny))
        elif "曇" in sentence and "?" not in sentence and "？" not in sentence:
            print("BOT: " + random.choice(ChatBotScript.cloudy))
        elif "雨" in sentence and "?" not in sentence and "？" not in sentence:
            print("BOT: " + random.choice(ChatBotScript.rainy))
        elif ("風" in sentence and "強い" in sentence) or ("強風" in sentence):
            print("BOT: " + "吹き飛ばされないように気をつけてくださいね")
        elif "台風" in sentence:
            print("BOT: " + random.choice(ChatBotScript.typhoon))
        elif "元気" in sentence:
            print("BOT: " + random.choice(ChatBotScript.physical_condition))
        elif "本当" in sentence and ("?" in sentence or "？" in sentence):
            print("BOT: " + random.choice(ChatBotScript.response2))
        elif "今何時" in sentence:
            time_now()
        elif "元気" in sentence or ("本当" in sentence and ("?" in sentence or "？" in sentence)) or "朝食" in sentence or "昼食" in sentence or "晩飯" in sentence  or "夜食" in sentence or "食事" in sentence or "ご飯" in sentence or "ランチ" in sentence or "ディナー" in sentence or "かっこいい" in sentence or "かっこ良い" in sentence or "かわいい" in sentence or "高い" in sentence or "安い" in sentence or "難しい" in sentence or "簡単" in sentence or "面白" in sentence or "おもしろ" in sentence or "おいし" in sentence or "美味し" in sentence or (("体重" in sentence or "身長" in sentence or "スリーサイズ" in sentence) and ("?" in sentence or "？" in sentence)):
            break
        else:
            if count_weather == 1:
                count_weather += 1
                print("BOT: " + "今週の天気は安定しそうですか？")
            else:
                print("BOT: " + "天気を調べてみましょうか？")
                speech = input("user: ")
                sentence = SentenceGenerator.sentence_generator(speech)
                # \\\\\\\
                print("----------変換後: " + sentence)
                if "はい" in sentence or "よろ" in sentence or "お願い" in sentence or "調べて" in sentence:
                    url = 'weather_service.html'
                    webbrowser.open(url)
                else:
                    print("BOT: " + "わかりました。何か別の話をしませんか？")
                    break

def food_talk():
    while True:
        # 入力
        speech = input("user: ")
        sentence = SentenceGenerator.sentence_generator(speech)
        # \\\\\\\\\\
        print("----------変換後: " + sentence)

        if "ない" in sentence or "いや" in sentence:
            print("BOT:" + "では、おすすめの食べ物ありますか？")
        elif "元気" in sentence or ("本当" in sentence and ("?" in sentence or "？" in sentence)) or "かっこいい" in sentence or "かっこ良い" in sentence or "かわいい" in sentence or "高い" in sentence or "安い" in sentence or "難しい" in sentence or "簡単" in sentence or "面白" in sentence or "おもしろ" in sentence or (("体重" in sentence or "身長" in sentence or "スリーサイズ" in sentence) and ("?" in sentence or "？" in sentence)):
            break
        else:
            print("BOT:" + "では、質問のページを開くので選択肢から選んでください")
            time.sleep(2)
            url = 'food_quiz.html'
            webbrowser.open(url)

#--------------
#-----メイン-----
#--------------

count_talk = 0
symbol = ["", "！", "？"]

greeting()
input("user: ")
# 話題選択
while True:
    if count_talk == 0:
        print("BOT: " + "何のお話をしましょうか？")
    elif count_talk == 1:
        print("BOT:" + "何の話ですか？")
    else:
        pass

    speech = input("user: ")
    sentence = SentenceGenerator.sentence_generator(speech)
    # \\\\\\\\\\
    print("----------変換後: " + sentence)
    if "天気" in sentence:
        print("BOT: " + "あなたの地域の今日の天気はどうですか？")
        weather_talk()
        count_talk = 1
    elif "食" in sentence or "飯" in sentence:
        print("BOT:" + "昨日の晩御飯が何か当てましょうか？")
        food_talk()
        count_talk = 1
