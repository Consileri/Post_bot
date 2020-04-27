import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


dilivered_flag = False
status = ''
order_id = ''
sessionStorage = {}

def send_msg(msg, user_id, rndm, vk):
    vk.message.send(user_id=user_id,
                    message=msg,
                    random_id=rndm)

def main():
    vk_session = vk_api.VkApi(
        token="68b38a0e0b7e909d8535d5508795ae46d9c6175ffd694c28428dd3e63a0738d737667112f465e297887c8")
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, 193785456)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            handle_dialog(event, vk)



def handle_dialog(event, vk):

    user_id = event.obj.message['from_id']
    rndm = random.randint(0, 2 ** 64)
    send_msg()
    message = event.obj.message['text']
    if user_id in sessionStorage:
        quests = sessionStorage[user_id]['last_question']
        if quests == 1:
            vk.message.send(user_id=user_id,
                            message=f"Приятно познакомиться, {message}. Кем бы вы хотели быть, почтальоном или"
                                    f" заказчиком?",
                            random_id=rndm)
            sessionStorage[user_id]['name'] = message
            sessionStorage[user_id]['last_question'] = 2 # 2 - Выбор деятельности
            return
        if quests == 2:
            sessionStorage[user_id]['activity'] = None
            role = sessionStorage[user_id]['activity']
            while role is None:
                if message == 'Почтальон' or 'почтальон':
                    message = message.lower()
                    role = message
                    sessionStorage[user_id]['last_question'] = 3
                elif message == 'Заказчик' or 'заказчик':
                    message.lower()
                    sessionStorage[user_id]['last_question'] = 3 #авторизация завершена
                    send_msg('Вы успешно авторизованы как заказчик! Теперь Вам доступна "Помощь"', user_id, rndm, vk)
                    break
                else:
                    send_msg("Вам нужно написать 'почтальон' или 'заказчик'", user_id, rndm, vk)
                    continue
            return
        if quests == 3 and message == 'почтальон':
            if message == 'Помощь' or 'помощь':
                send_msg("По всем вопросам обращаться\nСписок доступных команд", user_id, rndm, vk)
            return
        if quests == 3 and message == 'заказчик':
            if message == 'Помощь' or 'помощь':
                send_msg("По всем вопросам обращаться\nСписок доступных команд", user_id, rndm, vk)
            return

    else:
        vk.messages.send(user_id=user_id,
                         message="Вас приветствует Post Bot! Как нам Вас стоит называть?(Напишите только имя)",
                         random_id=rndm)
        sessionStorage[user_id] = {
            'last_question' : 1      # 1 - как вас зовут
                                   }
        return

if __name__ == '__main__':
    main()