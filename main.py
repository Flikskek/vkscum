import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from store import tok

import requests,time,json



session = vk_api.VkApi(token=tok)

def get_price():
  url = f"https://api.bittrex.com/api/v1.1/public/getticker?market=USD-BTC"  
  print(url)
  j = requests.get(url)
  data = json.loads(j.text)  
  price = str(data['result']['Ask'])
  return 'Курс биткоина в долларах: ' + price + "💰"

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
            keyboard.add_button('BitCoin💳',VkKeyboardColor.POSITIVE)

            send_message(user_id,'Привет, пока что я могу показывать тебе курс биткоина, но это пока....',keyboard)
        elif text == 'bitcoin💳':
            keyboard = VkKeyboard()
            keyboard.add_button('BitCoin💳',VkKeyboardColor.POSITIVE)

            send_message(user_id,get_price(),keyboard)

        