import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

dilivered_flag = False
status = ''
order_id = ''
adress = ''




def main():
    vk_session = vk_api.VkApi(
        token="68b38a0e0b7e909d8535d5508795ae46d9c6175ffd694c28428dd3e63a0738d737667112f465e297887c8")


    longpoll = VkBotLongPoll(vk_session, 193785456)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            if event.obj.message['text'] == 'помощь' or event.obj.message['text'] == 'Помощь':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"На этой странице можно задать вопрос\nhttps://vk.com/hakureireimu\nСписок доступных команд:\nСтатус - просмотреть статус вашего заказа",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'] == 'статус' or event.obj.message['text'] == 'Статус':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Ваш заказ {status}",
                                 random_id=random.randint(0, 2 ** 64))
            elif dilivered_flag:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f'Ваш заказ {order_id} ожидает в пункте выдачи {adress}',
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Ничего не понял',
                                 random_id=random.randint(0, 2 ** 64))

if __name__ == '__main__':
    main()