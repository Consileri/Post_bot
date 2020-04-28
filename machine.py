import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from config import code_for_validation
from data.users import User
from data import db_session
from data.oder import Order

dilivered_flag = False
status = ''
order_id = ''
sessionStorage = {}
session = db_session.create_session()


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
    rndm = random.randint(0, 2 ** 64)
    user_id = event.obj.message['from_id']
    message = event.obj.message['text']
    if user_id in sessionStorage:
        quests = sessionStorage[user_id]['last_question']
        if quests == 1:
            vk.messages.send(user_id=user_id,
                             message=f"Приятно познакомиться, {message}. Кем бы вы хотели быть, почтальоном или"f" заказчиком?",
                             random_id=rndm)
            sessionStorage[user_id]['name'] = message
            sessionStorage[user_id]['last_question'] = 2  # 2 - Выбор деятельности
            return
        if quests == 2:
            sessionStorage[user_id]['activity'] = None
            role = sessionStorage[user_id]['activity']
            while role is None:
                if message == 'Почтальон' or 'почтальон':
                    message.lower()
                    sessionStorage[user_id]['activity'] = message
                    sessionStorage[user_id]['last_question'] = 3  # авторизация завершена
                    vk.messages.send(user_id=user_id,
                                     message='Вы успешно авторизованы как почтальон! Теперь Вам нужно указать вашу почту',
                                     random_id=rndm)
                    break
                elif message == 'Заказчик' or 'заказчик':
                    message.lower()
                    sessionStorage[user_id]['activity'] = message
                    sessionStorage[user_id]['last_question'] = 3  # авторизация завершена
                    vk.messages.send(user_id=user_id,
                                     message='Вы успешно авторизованы как заказчик! Теперь Вам нужно указать вашу почту',
                                     random_id=rndm)
                    break
                else:
                    vk.messages.send(user_id=user_id,
                                     message="Вам нужно написать 'почтальон' или 'заказчик'",
                                     random_id=rndm)
                    continue
            return
        if quests == 3:
            sessionStorage[user_id]['mail'] = None
            mail = message.split()
            counter = 0
            for i in mail:
                if i == '@':
                    counter += 1
            while sessionStorage[user_id]['mail'] == None:
                if counter == 1:
                    vk.messages.send(user_id=user_id,
                                     message="Теперь придумайте пароль",
                                     random_id=rndm)
                    sessionStorage[user_id]['mail'] = message
                    sessionStorage[user_id]['last_question'] = 4  # Запрос эл. почты
                    return
                else:
                    vk.messages.send(user_id=user_id,
                                     message="Почта не действительна",
                                     random_id=rndm)
                    continue
        if quests == 4:
            sessionStorage[user_id]['password'] = message
            sessionStorage[user_id]['last_question'] = 5  # Создание пароля
            return
        if quests == 5 and sessionStorage[user_id]['activity'] == 'почтальон':
            sessionStorage[user_id]['validation'] = False
            vk.messages.send(user_id=user_id,
                             message="Введите ваш код валидации",
                             random_id=rndm)
            while sessionStorage[user_id]['validation'] == False:
                if message == code_for_validation:
                    sessionStorage[user_id]['validation'] = True
                    vk.messages.send(user_id=user_id,
                                     message="Вы ввели верный код валидации. Вы успешно приняты!",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 6
                    return
                else:
                    vk.messages.send(user_id=user_id,
                                     message="Попробуйте ещё раз",
                                     random_id=rndm)
                    continue
        if quests == 6 and sessionStorage[user_id]['activity'] == 'почтальон':
            if message == 'Помощь' or 'помощь':
                vk.messages.send(user_id=user_id,
                                 message="По всем вопросам обращаться\nhttps://vk.com/hakureireimu",
                                 random_id=rndm)
                return
        if quests == 5 and sessionStorage[user_id]['activity'] == 'заказчик':
            if message == 'Помощь' or 'помощь':
                vk.messages.send(user_id=user_id,
                                 message="По всем вопросам обращаться\nhttps://vk.com/hakureireimu\nСписок доступных команд\nСтатус - статус текущего заказа",
                                 random_id=rndm)
                return
            if message == 'Статус' or message == 'статус':
                sessionStorage[user_id]['status'] = None
                vk.message.send(user_id=user_id,
                                message='Введите номер вашего заказа',
                                random_id=rndm)
                sessionStorage[user_id]['last_question'] = 228 # заказ есть
                order = session.query(Order).filter(Order.id == message).first()
                if order.is_adopted:
                    sessionStorage[user_id]['status'] = 'Принят'
                if order.is_getting_ready:
                    sessionStorage[user_id]['status'] = 'Готовится к отправке'
                if order.is_delivering:
                    sessionStorage[user_id]['status'] = 'Доставляетс'
                if order.is_waiting:
                    sessionStorage[user_id]['status'] = 'Ожидает отгрузки'
                if order.is_done:
                    sessionStorage[user_id]['status'] = 'Завершен'
                if order.is_not_adopted:
                    sessionStorage[user_id]['status'] = 'Пока не принят'

            if quests == 228:
                vk.message.send(user_id=user_id,
                                message=f"Ваш заказ {sessionStorage[user_id]['status']}",
                                random_id=rndm)

    else:
        vk.messages.send(user_id=user_id,
                         message="Вас приветствует Post Bot! Как нам Вас стоит называть?(Напишите только имя)",
                         random_id=rndm)
        sessionStorage[user_id] = {
            'last_question': 1  # 1 - как вас зовут
        }
        return

    if sessionStorage[user_id]['activity'] == 'почтальон':
        user = User(
            name=sessionStorage[user_id]['name'],
            email=sessionStorage[user_id]['mail'],
            is_postman=True)
    else:
        user = User(
            name=sessionStorage[user_id]['name'],
            email=sessionStorage[user_id]['mail'],
            is_postman=False)
    user.set_password(sessionStorage[user_id]['password'])
    session.add(user)
    session.commit()


if __name__ == '__main__':
    main()
