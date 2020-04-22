import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from commander import Commander
from vk_api.longpoll import VkEventType

from vk_bot import VkBot


def main():
    vk_session = vk_api.VkApi(
        token="68b38a0e0b7e909d8535d5508795ae46d9c6175ffd694c28428dd3e63a0738d737667112f465e297887c8")

    longpoll = VkBotLongPoll(vk_session, 193785456)
    
    commander = Commander()
    
    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:

                print(f'New message from {event.user_id}', end='')

                bot = VkBot(event.user_id)

                if event.text[0] == "/":
                    write_msg(event.user_id, commander.do(event.text[1::]))
                else:
                    write_msg(event.user_id, bot.new_message(event.text))

                print('Text: ', event.text)
                print("-------------------")
