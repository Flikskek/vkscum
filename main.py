import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from store import tok #python файл с переменной в которой содержится токен

import requests
import json

session = vk_api.VkApi(token=tok) #ваш токен (tok)


def get_price_usd():
    url_usd = f"http://apilayer.net/api/live?access_key=f70d8094d6921b42003c41652d03c31b&currencies=RUB,GBP,CAD,PLN&source=USD&format=1"
    print(url_usd)
    u = requests.get(url_usd)
    datausd = json.loads(u.text)
    priceu = str(datausd["quotes"]["USDRUB"])
    return 'Курс доллара в рублях 1USD = ' + priceu + "💰"


def get_price_btc():
    url_btc = f"https://api.bittrex.com/api/v1.1/public/getticker?market=USD-BTC"
    print(url_btc)
    j = requests.get(url_btc)
    data = json.loads(j.text)
    price = str(data['result']['Ask'])
    return 'Курс биткоина в долларах 1BTC = ' + price + "💰"


def send_message(user_id, message, keyboard=None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()

    session.method("messages.send", post)


for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id

        if text == 'начать':
            keyboard = VkKeyboard()
            keyboard.add_button('BitCoin💳', VkKeyboardColor.POSITIVE)
            keyboard.add_button('USD💵', VkKeyboardColor.NEGATIVE)

            send_message(user_id, 'Привет, пока что я могу показывать тебе курс биткоина и доллара, но это пока....',
                         keyboard)
        elif text == 'bitcoin💳':
            keyboard = VkKeyboard()
            keyboard.add_button('BitCoin💳', VkKeyboardColor.POSITIVE)
            keyboard.add_button('USD💵', VkKeyboardColor.NEGATIVE)
            send_message(user_id, get_price_btc(), keyboard)
        elif text == 'usd💵':
            keyboard = VkKeyboard()
            keyboard.add_button('BitCoin💳', VkKeyboardColor.POSITIVE)
            keyboard.add_button('USD💵', VkKeyboardColor.NEGATIVE)
            send_message(user_id, get_price_usd(), keyboard)
