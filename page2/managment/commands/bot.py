from django.core.management.base import BaseCommand
from django.conf import settings
import json
import re
import datetime
import nltk
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import telebot
from sklearn.model_selection import GridSearchCV
from page2.models import Message
from page2 import views
import base64


class Command(BaseCommand):
    help = 'TG Bot'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.BOT_KEY)
        config_file = open("page2/static/page2/json/big_bot_config.json",
                           "r", encoding="utf-8")
        BOT_CONFIG = json.load(config_file)
        X = []
        y = []

        for name, data in BOT_CONFIG["intents"].items():
            for example in data['examples']:
                X.append(example)
                y.append(name)

        vectorizer = CountVectorizer()
        vectorizer.fit(X)
        vecX = vectorizer.transform(X)

        model = RandomForestClassifier(n_estimators=300, min_samples_split=3)
        model.fit(vecX, y)

        model.score(vecX, y)

        ideal_model = RandomForestClassifier()
        param = {
            "n_estimators": [60, 140],
            "criterion": ["gini", "entropy"]
        }
        cv = GridSearchCV(ideal_model, param)
        cv.fit(vecX, y)

        def filter(text):
            alphabet = 'абвгджзеёийклмнопрстуфхцчшщьыъэюя -'
            result = [c for c in text if c in alphabet]
            return ''.join(result)

        def filter_hel(text):
            text = re.sub(r"(?i)\добрый день\b", "", text)
            text = re.sub(r'(?i)\добрый вечер\b', "", text)
            text = re.sub(r'(?i)\доброе утро\b', "", text)
            text = re.sub(r'(?i)\здравствуйте\b', "", text)
            text = re.sub(r'(?i)\привет\b', "", text)
            text = re.sub(r"(?i)\подскажите\b", "", text)
            text = re.sub(r'(?i)\пожалуйста\b', "", text)
            text = re.sub(r"(?i)\спасибо\b", "", text)
            return re.sub(r"(?i)\приветствую\b", "", text)

        def match(text, example):
            text = filter(text.lower())
            example = example.lower()
            distance = nltk.edit_distance(text, example) / len(example)
            return distance < 0.4

        def get_intent(text):
            for intent in BOT_CONFIG["intents"]:
                for example in BOT_CONFIG["intents"][intent]["examples"]:
                    if match(text, example):
                        return intent

        chat_history = ["Абоба"]
        leather_punch = {}

        def bot_answer(text, text_lit, user_id, date_time, text_1, user_info, type_msg, message_id):
            intent = get_intent(text)

            if intent:
                answ(user_id, BOT_CONFIG["intents"][intent]["responses"])

            else:
                save_user(user_id, date_time, text_1, text_lit, user_name(user_info), False, save_img(user_id), False, True,
                          type_msg, message_id)
                answ(user_id, BOT_CONFIG["failure_phrases"])

        def answ(user_id, text):
            bot.send_message(user_id, text=text)

        def save_img(user_id):
            try:
                img = bot.get_user_profile_photos(user_id)
                img_id = img.photos[0][0].file_id
                img_1 = bot.get_file(img_id).file_path
                img_b2 = bot.download_file(img_1)
                img_id = base64.b64encode(img_b2).decode("utf-8")
                return img_id
            except:
                return 'https://kirox.ru/images/avatar-default.png'

        def user_name(user_info):
            if user_info.username != None:
                return user_info.username
            else:
                return f"{user_info.first_name if user_info.first_name != None else ''} {user_info.last_name if user_info.last_name != None else ''}"

        def save_user(user_id, data, text, text_lit, user_name, is_answer, img, is_read, is_lth_pnc, type_msg, message_id):
            views.save_user(user_id, data, text, text_lit, user_name, is_answer, img, is_read, is_lth_pnc, type_msg, message_id)


        @bot.message_handler(commands=['start'])
        def start(message):
            leather_punch[message.chat.id] = False
            bot.send_message(message.chat.id,
                             text="Добро пожаловать, задай мне вопрос и я постораюсь на него ответить!".format(
                                 message.from_user))

        @bot.message_handler(content_types=['text'])
        def react_on_msg(message):
            user_dict = {}
            msg = Message.objects.order_by("data")
            for i in msg:
                user_dict[i.user_id] = i.data
            msg_obj = [Message.objects.filter(user_id=key, data=value) for key, value in user_dict.items()]
            for i in msg_obj:
                for el in i:
                    leather_punch[el.user_id] = el.is_lth_pnch
            user_id = message.chat.id
            user_info = message.from_user
            date_time = datetime.datetime.now()
            message_id = message.message_id


            if message.text != "нет" and message.text != "Нет" and leather_punch.get(user_id) != True:
                text = message.text
                chat_history.append(text)
                text_lit = text[0:10]
                bot_answer(filter_hel(str(text)), text_lit, user_id, date_time, text, user_info, "Text", message_id)

            elif message.text == "нет" or message.text == "Нет" and leather_punch.get(user_id) != True:
                bot.send_message(message.chat.id, text="Переключаю...")
                text = str(chat_history[-1])
                save_user(user_id, date_time, text, text[0:10], user_name(user_info), False, save_img(user_id), False, True, "Text", message_id)

            else:
                text_lit = message.text[0:10]
                save_user(user_id, date_time, message.text, text_lit, user_name(user_info), False, save_img(user_id), False, True,
                          "Text", message_id)

        @bot.message_handler(content_types=['photo'])
        def react_on_msg(message):
            text = message.caption
            message_id = message.message_id
            if text is None:
                text = ""
            else:
                text = text[0:10]
            img = bot.get_file(message.photo[-1].file_id).file_path
            img_b2 = bot.download_file(img)
            msg = base64.b64encode(img_b2).decode("utf-8")
            user_id = message.chat.id
            date_time = datetime.datetime.now()
            user_info = message.from_user
            save_user(user_id, date_time, msg, text, user_name(user_info), False, save_img(user_id), False, True,
                      "Image", message_id)

        @bot.message_handler(content_types=['sticker'])
        def react_on_msg(message):
            message_id = message.message_id
            if not message.sticker.is_animated and not message.sticker.is_video:
                sticker = bot.get_file(message.sticker.file_id).file_path
                uni_sticker = bot.download_file(sticker)
                msg = base64.b64encode(uni_sticker).decode("utf-8")
                user_id = message.chat.id
                date_time = datetime.datetime.now()
                user_info = message.from_user
                text = ""
                save_user(user_id, date_time, msg, text, user_name(user_info), False, save_img(user_id), False, True,
                          "ImageWb", message_id)

            else:
                if message.sticker.is_video:
                    sticker = bot.get_file(message.sticker.file_id).file_path
                    msg = f'https://api.telegram.org/file/bot{settings.BOT_KEY}/{sticker}'
                    user_id = message.chat.id
                    date_time = datetime.datetime.now()
                    user_info = message.from_user
                    text = ""
                    save_user(user_id, date_time, msg, text, user_name(user_info), False, save_img(user_id), False, True,
                              "VideoSt", message_id)
                else:
                    stick = bot.get_file(message.sticker.thumb.file_id).file_path
                    im = bot.download_file(stick)
                    msg = base64.b64encode(im).decode("utf-8")
                    user_id = message.chat.id
                    date_time = datetime.datetime.now()
                    user_info = message.from_user
                    text = ""
                    save_user(user_id, date_time, msg, text, user_name(user_info), False, save_img(user_id), False,
                              True,
                              "ImageWb", message_id)

        @bot.message_handler(content_types=['video'])
        def react_on_msg(message):
            message_id = message.message_id
            sticker = bot.get_file(message.video.file_id).file_path
            msg = f'https://api.telegram.org/file/bot{settings.BOT_KEY}/{sticker}'
            user_id = message.chat.id
            date_time = datetime.datetime.now()
            user_info = message.from_user
            text = "Нажмите для воспроизведения"
            save_user(user_id, date_time, msg, text, user_name(user_info), False, save_img(user_id), False, True,
                      "Video", message_id)

        bot.infinity_polling()
