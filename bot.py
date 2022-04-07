#!/usr/bin/python3
import datetime
import time
import vk_api
import pyjokes
import cowsay
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
def write_message(sender, message):
    authorize.method('messages.send',{'chat_id': sender, 'message': message, "random_id": get_random_id()})
def send_attachment(sender, message, attachment_id):
    authorize.method('messages.send',{'chat_id': sender, 'message': message, "random_id": get_random_id(), 'attachment_id': attachment_id})
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
token = ""
authorize = vk_api.VkApi(token = token)
longpoll = VkBotLongPoll(authorize, group_id=207217384)

#text,hour,minute,weekday

subs = [
        ["Physics fri 11:00  Voov: 249487498 5590 Canvas: https://oc.sjtu.edu.cn/courses/43746/external_tools/162",7,50,4],
        ["Elementary Chinese fri 13:00  VooV: 960944269 6821",9,50,4],
    
	["Solid mechanics mon 7:55 VooV: 488321911 6641 Canvas: https://oc.sjtu.edu.cn/courses/39700/external_tools/162",4,45,0],
	["Thermodynamics mon 11:00 VooV: 607336235 5714 Canvas: https://oc.sjtu.edu.cn/courses/39699/external_tools/162",7,50,0],
        ["Elementary Chinese mon 13:00 VooV: 960944269 6821",9,50,0],
    
        ["Aerodynamics tue 7:55 VooV: 509400075 1994 Canvas: https://oc.sjtu.edu.cn/courses/39723/external_tools/162",4,45,1],
        ["Design and manufacture tue 11:00 VooV: 917233837 8633 Canvas: https://oc.sjtu.edu.cn/courses/39421/external_tools/162",7,50,1],
        
        ["Thermodynamics wed 9:00 VooV: 607336235 5714 Canvas: https://oc.sjtu.edu.cn/courses/39699/external_tools/162",5,50,2],
    
        ["Engineering, Social and Professional ethics thu 7:55 VooV: 745123071 3233  Canvas: https://oc.sjtu.edu.cn/courses/39689/external_tools/162",4,45,3],
        ["Design and manufacture thu 11:00 VooV: 917233837 8633 Canvas: https://oc.sjtu.edu.cn/courses/39421/external_tools/162",7,50,3],
       ]

while(1):
    now = datetime.datetime.now()
            
    for sub in subs:
        if now.hour == sub[1] and now.minute == sub[2] and now.weekday() == sub[3]:
            write_message(2, sub[0])
            time.sleep(60)
            
    if now.hour == 21 and now.minute == 1 and now.day == 31 and now.month == 12:
        write_message(2,'Happy new year!')
        time.sleep(60)

    if now.hour == 12 and now.minute == 1 and now.day == 4 and now.month == 11:
        write_message(2,'Happy Use Your Common Sense Day')
        time.sleep(60)

    events = longpoll.check()
    k = 0
    
    if len(events)>0:
        for event in events:
            reseived_message = event.message.get('text')
            sender = event.chat_id
            if reseived_message == 'coming up' or reseived_message ==  'Coming up':
                for sub in subs:
                    if now.hour <= sub[1] and now.weekday() == sub[3]:
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
                     write_message(sender, subs[3][0])
                k = 0
            if reseived_message == 'id':
                write_message(sender, sender)
            if reseived_message == 'date':
                write_message(sender, now)
            if reseived_message == 'Midnight':
                send_attachment(sender, "Yeah, midnight",  'audio-207217384_456239018')
            if reseived_message == 'show all':
                sup=''
                for sub in subs:
                    sup=sup+sub[0]+"\n"
                write_message(sender, sup)
            if reseived_message[0:6] == 'cowsay' or reseived_message[0:6] == 'Cowsay':
                write_message(sender, cowsay.get_output_string('cow', reseived_message[7:].replace('\n', '\n|').replace(' ',' ')))
            if reseived_message == 'tell a joke' or reseived_message == 'Tell a joke':
                write_message(sender, pyjokes.get_joke())
