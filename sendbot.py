import vk_api, json, requests, traceback
from vk_api.bot_longpoll import VkBotEventType

vk_session = vk_api.VkApi(token='token')
vk = vk_session.get_api()
longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, id, wait=25)

while True:
    try:

        for event in longpoll.listen():

            obj = event.object.message
            peer = obj['peer_id']

            if event.type == VkBotEventType.MESSAGE_NEW:
                result = json.loads(requests.post(vk.docs.getMessagesUploadServer(type='doc', peer_id=peer)['upload_url'],
                                                  files={'file': open('bot.py', 'rb')}).text)
                jsonAnswer = vk.docs.save(file=result['file'], title='title', tags=[])

                vk.messages.send(
                    peer_id=peer,
                    random_id=0,
                    attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
                )

    except:
        print(traceback.format_exc())
