import asyncio
import math
import time
from vk import VK
import logging
from vk_api.bot_longpoll import CHAT_START_ID
from vk_api.tools import VkTools
from vk_function_methods import vk_get_25req_messages
import json
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
request_word = morph.parse('запрос')[0]

with open("config.json") as f:
    token = json.load(f)["token"]
vk = VK(access_token=token)


async def fetch_all_msg_from_chat(api, chat_id):
    result = await api.api_request("messages.getHistory", dict(peer_id=CHAT_START_ID + chat_id, count=0))
    count = result["count"]
    requests_count = math.ceil(count / 5000)
    print('Всего сообщений:', count)
    print(f'Нужно совершить {requests_count} {request_word.make_agree_with_number(requests_count).word}')
    counter = 0
    results = []
    items = []
    for i in range(requests_count):
        results.append(api.api_request("execute", dict(**vk_get_25req_messages(CHAT_START_ID + chat_id, 5000 * i))))
    for i in asyncio.as_completed(results):
        counter += 1
        print(f'Выполнено {counter} {request_word.make_agree_with_number(counter).word}')
        result = await i
        items.extend(result)
    return items


async def main():
    start = time.time()
    all_msgs = await fetch_all_msg_from_chat(vk, 133)
    with open('cache.json', 'w') as f:
        json.dump(sorted(all_msgs, key=lambda x: x['id']), f)
    print(len(all_msgs))
    print("Заняло секунд на выполнение", time.time() - start)


asyncio.get_event_loop().run_until_complete(main())
