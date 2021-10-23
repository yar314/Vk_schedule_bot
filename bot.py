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

subs = [
        ["Circuit theory fri 9:00 Canvas: https://oc.sjtu.edu.cn/courses/33999/external_tools/162",5,50,4],
        ["Elementary Chinese fri 11:00 VooV: 405119539 8988",7,50,4],
        ["Complex analysis fri 13:00 VooV: 684404375 8988",9,50,4],
    
        ["Theoretical mechanics mon 5:00 Canvas: https://oc.sjtu.edu.cn/courses/33925/external_tools/162",1,50,0],
    
        ["Physics tue 5:00 Canvas: https://oc.sjtu.edu.cn/courses/33874/external_tools/162",1,50,1],
        ["Circuit theory tue 11:00 Canvas: https://oc.sjtu.edu.cn/courses/33999/external_tools/162",7,50,1],
        ["Probability and statistics tue 13:00 VooV: 491570291 9373",9,50,1],
        
        ["Elementary chinese wed 11:00 VooV: 405119539 8988",7,50,2],
        ["Theoretical mechanics wed 13:00 Canvas: https://oc.sjtu.edu.cn/courses/33925/external_tools/162",9,50,2],
    
        ["Numerical methods thu 11:00 Canvas: https://oc.sjtu.edu.cn/courses/34120/external_tools/162",7,50,3],
        ["Physics tue 13:00 Canvas: https://oc.sjtu.edu.cn/courses/33874/external_tools/162",9,50,3],
    
        ["Probability and statistics sat 11:00 VooV: 491570291 9373",7,50,5],
       ]

while(1):
    now = datetime.datetime.now()
            
    for sub in subs:
        if now.hour == sub[1] and now.minute == sub[2] and now.weekday() == sub[3]:
            write_message(1, sub[0])
            time.sleep(60)
            
    events = longpoll.check()
    k = 0
    
    if len(events)>0:
        for event in events:
            reseived_message = event.message.get('text')
            sender = event.chat_id
            if reseived_message == 'coming up' or 'Coming up':
                for sub in subs:
                    if now.hour <= sub[1] and now.minute <= sub[2] and now.weekday() == sub[3]:
                        write_message(1, sub[0])
                        k = 1
                        break  
                if k == 0:
                    for sub in subs:
                        if sub[3] == now.weekday()+1:
                            write_message(1, sub[0])
                            k = 1
                            break
                if k == 0:
                     write_message(1, subs[3][0])
                k = 0
            if reseived_message == 'coming up' or 'Coming up':
