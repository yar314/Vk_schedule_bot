import datetime
import time
import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
def write_message(sender, message):
    authorize.method('messages.send',{'chat_id': sender, 'message': message, "random_id": get_random_id()})
def check(self):
        """ Получить события от сервера один раз

        :returns: `list` of :class:`Event`
        """
        values = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': self.wait,
            'mode': self.mode,
            'version': 3
        }

        response = self.session.get(
            self.url,
            params=values,
            timeout=self.wait + 10
        ).json()

        if 'failed' not in response:
            self.ts = response['ts']
            if self.pts:
                self.pts = response['pts']

            events = [
                self._parse_event(raw_event)
                for raw_event in response['updates']
            ]

            if self.preload_messages:
                self.preload_message_events_data(events)

            return events

        elif response['failed'] == 1:
            self.ts = response['ts']

        elif response['failed'] == 2:
            self.update_longpoll_server(update_ts=False)

        elif response['failed'] == 3:
            self.update_longpoll_server()

        return []
token = "871352a27a2e0e28118972f4ac850f5b5e3d9bf492cc4239bdd698daef723978b09ba2437fe3545a6409f"
authorize = vk_api.VkApi(token = token)
longpoll = VkBotLongPoll(authorize, group_id=207217384)

#text,hour,minute,weekday

subs = [["Circuit theory",8,50,4],["Elementary Chinese",10,50,4],["Complex analysis",12,50,4]]

while(1):
    now = datetime.datetime.now()
            
    for sub in subs:
        if now.hour == sub[1] and now.minute == sub[2] and now.weekday() == sub[3]:
            write_message(1, sub[0])
            time.sleep(60)
            
    events = longpoll.check()
    
    if len(events)>0:
        for event in events:
            reseived_message = event.message.get('text')
            sender = event.chat_id
            if reseived_message == 'coming up':
                for sub in subs:
                    if now.hour < sub[1] or now.minute < sub[2] or now.weekday() < sub[3]:
                        write_message(1, sub[0])
                        time.sleep(60)
