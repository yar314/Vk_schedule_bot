#!/usr/bin/python3
import datetime
import time
import vk_api
import pyjokes
import cowsay
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
def write_message(sender, message):
    authorize.method('messages.send',{'chat_id': sender, 'message': message, "random_id": get_random_id()})
def send_attachment(sender, message, attachment_id):
    authorize.method('messages.send',{'chat_id': sender, 'message': message, "random_id": get_random_id(), 'attachment': ','.join(attachments)})
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
image = "F:/schedule.jpg"
authorize = vk_api.VkApi(token = token)
longpoll = VkBotLongPoll(authorize, group_id=207217384)
upload = VkUpload(authorize)

#text,hour,minute,weekday

subs = [
        ["Aerodynamics fri 7:55",4,45,4],
        ["Chinese language fri 13:00 Canvas: https://oc.sjtu.edu.cn/courses/49385/external_tools/162",9,50,4],
    
	["Flight dynamics mon 7:55 Canvas: https://oc.sjtu.edu.cn/courses/48237/external_tools/162",4,45,0],
    
        ["Aviation economics tue 9:00",5,50,1],
        
        ["Chinese language wed 13:00 Canvas: https://oc.sjtu.edu.cn/courses/49385/external_tools/162",9,50,2],
    
        ["Aerodynamic labs thu 9:00 Canvas: https://oc.sjtu.edu.cn/courses/48177/external_tools/162",5,50,3],
        ["Academic communication in English thu 11:00",7,50,3],
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
            attachments = []
            upload_image = upload.photo_messages(photos=image)[0]
            attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
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
            if reseived_message == 'schedule' or reseived_message == 'Schedule':
                send_attachment(sender, "Schedule of lessons:", attachments)
            if reseived_message == 'date':
                write_message(sender, now)
            if reseived_message == 'help' or reseived_message == 'Help':
                write_message(sender, "Coming up - link of nearest lecture"+"\n"+"Show all - links of all lectures"+"\n"+"Schedule - shedule of lectures"+"\n"+"Tell a joke - random joke")
            if reseived_message == 'show all' or reseived_message == 'Show all':
                sup=''
                for sub in subs:
                    sup=sup+sub[0]+"\n"
                write_message(sender, sup)
            if reseived_message[0:5] == 'frame':
                text=''
                for i in range(len(reseived_message[6:])):
                    text=text+'—'
                text=text+'\n| '+reseived_message[6:]+' |\n'
                for i in range(len(reseived_message[6:])):
                    text=text+'—'
                write_message(sender, text)
            if reseived_message == 'tell a joke' or reseived_message == 'Tell a joke':
                write_message(sender, pyjokes.get_joke())
            if reseived_message[0:6] == 'cowsay' or reseived_message[0:6] == 'Cowsay':
                write_message(sender, cowsay.get_output_string('cow', reseived_message[7:]).replace('\n', '\n|').replace(' ',' '))
