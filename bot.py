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
token = "***"
authorize = vk_api.VkApi(token = token)
longpoll = VkBotLongPoll(authorize, group_id=207217384)

#text,hour,minute,weekday

subs = [
        ["Physics fri 9:55 Canvas: https://oc.sjtu.edu.cn/courses/43746/external_tools/162",6,45,4],
        ["Elementary Chinese fri 11:55 VooV: 960944269 6821",8,45,4],
    
        ["Solid mechanics mon 7:55 Canvas: https://oc.sjtu.edu.cn/courses/39700/external_tools/162",4,45,0],
        ["Thermodynamics mon 11:00 Canvas: https://oc.sjtu.edu.cn/courses/39699/external_tools/162",7,50,0],
        ["Elementary Chinese mon 13:00 VooV: 960944269 6821",9,50,0],
    
        ["Aerodynamics tue 7:55 Canvas: https://oc.sjtu.edu.cn/courses/39723/external_tools/162",4,45,1],
        ["Design and manufacture tue 11:00 Canvas: https://oc.sjtu.edu.cn/courses/39421/external_tools/162",7,50,1],
        
        ["Thermodynamics wed 9:00 Canvas: https://oc.sjtu.edu.cn/courses/39699/external_tools/162",5,50,2],
    
        ["Engineering, Social and Professional ethics thu 7:55 Canvas: https://oc.sjtu.edu.cn/courses/39689/external_tools/162",4,45,3],
        ["Design and manufacture thu 11:00 Canvas: https://oc.sjtu.edu.cn/courses/39421/external_tools/162",7,50,3],
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
                        write_message(sender, sub[0])
                        k = 1
                        break  
                if k == 0:
                    for sub in subs:
                        if sub[3] == now.weekday()+1:
                            write_message(sender, sub[0])
                            k = 1
                            break
                if k == 0:
                     write_message(1, subs[3][0])
                k = 0
