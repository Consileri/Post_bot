import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


dilivered_flag = False
status = ''
order_id = ''
sessionStorage = {}


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
                    sessionStorage[user_id]['activity'] = message
                    sessionStorage[user_id]['last_question'] = 3 #авторизация завершена
                    vk.message.send(user_id=user_id,
                                    message='Вы успешно авторизованы как заказчик! Теперь Вам доступна "Помощь"',
                                    random_id=rndm)
                    break
                else:
                    vk.message.send(user_id=user_id,
                                    message="Вам нужно написать 'почтальон' или 'заказчик'",
                                    random_id=rndm)
                    continue
            return
        if quests == 3 and sessionStorage[user_id]['activity'] == 'почтальон':
            if message == 'Помощь' or 'помощь':
                vk.message.send(user_id=user_id,
                                message="По всем вопросам обращаться\nhttps://vk.com/hakureireimu",
                                random_id=rndm)
            return
        if quests == 3 and sessionStorage[user_id]['activity'] == 'заказчик':
            if message == 'Помощь' or 'помощь':
                vk.message.send(user_id=user_id,
                                message="По всем вопросам обращаться\nhttps://vk.com/hakureireimu\nСписок доступных команд\nСтатус - статус текущего заказа",
                                random_id=rndm)
                return
            if message == 'Статус' or message == 'статус':
                pass



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