import base64
import datetime
import telebot
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.shortcuts import render, redirect
from .models import Message, Photo, ToJson
from .forms import MessageForm, PhotoForm, ToJsonForm
from django.conf import settings
from django.db.models.signals import post_save


@receiver(post_save, sender=Message)
def update(created, **kwargs):
    pass


@login_required
def index(request):
    user_dict = {}
    msg = Message.objects.order_by("data")
    for i in msg:
        user_dict[i.user_id] = i.data
    msg_obj = [msg.filter(data=value, user_id=key) for key, value in user_dict.items()]
    msg_date = [i.values_list()[0][2] for i in msg_obj]
    msg_view = [x for _, x in sorted(zip(msg_date, msg_obj), reverse=True)]
    return render(request, 'page2/index.html', {'msg_obj': msg_view})


@login_required
def remove_items(request, parameter):
    msg = Message.objects.filter(user_id=parameter)
    msg.delete()
    return redirect('home')


@login_required
def update_args(request, parameter):
    msg = Message.objects.filter(user_id=parameter)
    obj = msg.latest('data')
    obj.is_lth_pnch = False
    obj.save()
    return redirect(f'/messenger/{parameter}')


@login_required
def messenger(request, parameter):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            answ = form['text'].value()
            us_id = parameter
            msg = Message.objects.order_by("data").filter(user_id=us_id)
            username = msg[0].user_info
            img_id = msg[(len(msg) - 1)].img
            save_answer(int(parameter), answ, username, True, img_id, True, True)
            return redirect(f'/messenger/{us_id}')
        else:
            pass
    form = MessageForm()
    us_id = parameter
    msg = Message.objects.order_by("data").filter(user_id=us_id)
    obj = msg.latest('data')
    obj.is_read = True
    obj.save()
    username = msg[0].user_info
    img_id = msg[(len(msg) - 1)].img
    if len(msg) <= 14:
        return render(request, 'page2/messenger.html',
                      {'msg': msg, 'username': username, 'img_id': img_id, 'us_id': us_id,
                       'form': form})
    else:
        return render(request, 'page2/messenger_low.html',
                      {'msg': msg[(len(msg) - 12):(len(msg))], 'username': username, 'img_id': img_id, 'us_id': us_id,
                       'form': form})


@login_required
def messenger_full(request, parameter):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            answ = form['text'].value()
            us_id = parameter
            msg = Message.objects.order_by("data").filter(user_id=us_id)
            username = msg[0].user_info
            img_id = msg[(len(msg) - 1)].img
            save_answer(int(parameter), answ, username, True, img_id, True, True)
            return redirect(f'/messenger/{us_id}')
        else:
            pass

    form = MessageForm()
    us_id = parameter
    msg = Message.objects.order_by("data").filter(user_id=us_id)
    obj = msg.latest('data')
    obj.is_read = True
    obj.save()
    username = msg[0].user_info
    img_id = msg[(len(msg) - 1)].img
    return render(request, 'page2/messenger.html',
                  {'msg': msg, 'username': username, 'img_id': img_id, 'us_id': us_id,
                   'form': form})


def save_answer(user_id, text, user_name, is_answer, img, is_read, is_lth_pnc):
    bot = telebot.TeleBot(settings.BOT_KEY)
    msg = bot.send_message(user_id, text)
    msg_id = msg.id

    Message.objects.create(
        user_id=int(user_id),
        data=datetime.datetime.now(),
        text=text,
        text_lit=text[0:10],
        user_info=user_name,
        is_answer=is_answer,
        img=img,
        is_read=is_read,
        is_lth_pnch=is_lth_pnc,
        type_msg="Text",
        msg_id=msg_id)


@login_required
def about(request):
    return render(request, 'page2/about.html')


@login_required
def feedback(request):
    if request.method == 'POST':
        form = ToJsonForm(request.POST)
        if form.is_valid():
            data = form['data'].value()
            question = form['question'].value()
            ToJson.objects.create(data=data, question=question)

    form = ToJsonForm()
    return render(request, 'page2/feedback.html', {'form': form})


@login_required
def contacts(request):
    return render(request, 'page2/contacts.html')


def save_user(user_id, date, text, text_lit, user_name, is_answer, img, is_read, is_lth_pnc, type_msg, message_id):
    Message.objects.create(
        user_id=int(user_id),
        data=date,
        text=text,
        text_lit=text_lit,
        user_info=user_name,
        is_answer=is_answer,
        img=img,
        is_read=is_read,
        is_lth_pnch=is_lth_pnc,
        type_msg=type_msg,
        msg_id=message_id)


@login_required
def load_image(request, parameter):
    if request.method == 'POST':
        path = f'page2/static/page2/img/{request.FILES["img"]}'
        instance = Photo(img=request.FILES['img'], user_id=parameter)
        instance.save()
        bot = telebot.TeleBot(settings.BOT_KEY)
        a = bot.send_photo(parameter, photo=open(f'{path}', 'rb'))
        msg_id = a.id
        photo = open(f'{path}', 'rb')
        image_read = photo.read()
        image_to_save = base64.encodestring(image_read).decode("utf-8")
        msg = Message.objects.order_by("data").filter(user_id=parameter)
        username = msg[0].user_info
        img_id = msg[(len(msg) - 1)].img
        save_user(parameter, datetime.datetime.now(), image_to_save, "", username, True,
                  img_id, True, True, "Image", msg_id)
        return redirect(f'/messenger/{parameter}')
    form = PhotoForm()
    us_id = parameter
    msg = Message.objects.order_by("data").filter(user_id=us_id)
    username = msg[0].user_info
    img_id = msg[(len(msg) - 1)].img
    return render(request, 'page2/load_image.html', {'form': form, 'username': username,
                                                     'img_id': img_id, 'us_id': us_id})


@login_required
def del_msg(request, parameter):
    msg = Message.objects.filter(msg_id=parameter)
    us_id = msg[0].user_id
    bot = telebot.TeleBot(settings.BOT_KEY)
    try:
        bot.delete_message(us_id, parameter)
        msg.delete()
        return redirect(f'/messenger/{us_id}')
    except:
        print(4)
        return redirect(f'/messenger/{us_id}')


@login_required
def groupe(request):
    bot = telebot.TeleBot(settings.BOT_KEY)
    if request.method == 'POST':
        list_of_input = request.POST.getlist('input')
        text = request.POST.get('text')
        if list_of_input and len(text) > 0:
            for i in list_of_input:
                msg = bot.send_message(int(i), text)
                msg_id = msg.id
                msg = Message.objects.order_by("data").filter(user_id=int(i))
                username = msg[0].user_info
                img_id = msg[(len(msg) - 1)].img
                save_user(int(i), datetime.datetime.now(), f"[Массовая рассылка]: {text}", text[0:10], username, True,
                          img_id, True, True, "Text", msg_id)
        return redirect('/groupe')
    user_dict = {}
    msg = Message.objects.order_by("data")
    for i in msg:
        user_dict[i.user_id] = i.data
    msg_obj = [msg.filter(data=value, user_id=key) for key, value in user_dict.items()]
    return render(request, 'page2/groupe.html', {'msg_obj': msg_obj})
