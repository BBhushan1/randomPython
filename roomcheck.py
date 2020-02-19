import json
import subprocess
from subprocess import DEVNULL
import requests, urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
Commented for now. Till I find resolution. 
'''
# def createTT(short_desc, details):
#     print("Creating Ticket")
#
#     category = 'AV/VC Support'
#     ticket_type = 'Issue'
#     item = 'Touch Panel'
#     requestor_login = 'bhbhu'
#     impact = '5'
#     assigned_group = 'IT-Support-APAC'
#     tt_url = "https://ticket-api.integ.amazon.com/tickets"
#     flxauth: tuple = ('flx-av-support', 'flx-av-support')
#     desc = short_desc
#     ttdetail = details
#     apiQuery = 'short_description={short_desc}&details={details}&category={category}&type={type}&' \
#                'item={item}&impact=5&requester_login=bhbhu'.format(short_desc=desc, details=ttdetail, category=category,
#                                                                    type=ticket_type, item=item)
#     print(tt_url + '\n' + apiQuery)
#     session = requests.Session()
#     session.auth = flxauth
#     session.verify = False
#     r = session.post(tt_url, data=apiQuery)
#     print(r)


t0 = time.time()
whurl = "https://hooks.chime.aws/incomingwebhooks/b79f7d1c-9c2f-4666-93df-a791ef9d6136?token=c2lHNmJxd2x8MXxaV3M5SE9QQmFpZ18ydVE2MExWVnc3NzQ0c2o5MnJCOXB2NU5CcG4yS2tz"
session = requests.Session()
headers = {"Content-Type": "application/json"}
messages = []
session.verify = False
message = "Check the output below:\n {rooms}"
room_count = 0
device_count = 0
devices_online = 0
devices_offline = 0
# print('-' * 70 + '\nExec started at {time}\n'.format(time=t0) + '-' * 70)
with open('rooms.json') as json_file:
    data = json.load(json_file)
    # print('-' * 80 + 'I am dataStart\n')
    # print(data)
    for room in data:
        # print('-' * 80 + 'I am Room Start\n')
        # print(room)
        messages.append(room['room_name'])
        room_count += 1
        for device in room['devices']:
            # print('-' * 80 + 'I am device Start\n')
            # print(device)
            device_count += 1
            room_name = room['room_name']
            device_name = device['device_name']
            ip_address = device['device_ip']
            ping_result = subprocess.call(["ping", "-n", "-W5", "-c3", ip_address], stdout=DEVNULL)
            if ping_result == 0:
                devices_online += 1
                emoji = ":white_check_mark:"
                chimetext = "{device_name} : {ip} - is active - {emoji}".format(emoji=emoji, device_name=device_name,
                                                                                ip=ip_address)
                messages.append((chimetext[:150] + '..') if len(chimetext) > 150 else chimetext)
            elif ping_result == 2:
                # shortdesc = device_name + ' is offline.'
                # details = device_name + '  in ' + room_name + ' is offline.   Kindly check. Details of the device is listed below:' + ip_address
                # createTT(shortdesc, details)
                devices_offline += 1
                emoji = ":rotating_light:"
                chimetext = "{device_name} : {ip} - is offline - {emoji}".format(emoji=emoji, device_name=device_name,
                                                                                 ip=ip_address)
                messages.append((chimetext[:150] + '..') if len(chimetext) > 150 else chimetext)
            else:
                emoji = ":rotating_light:"
                devices_offline += 1
                chimetext = "{device_name} : {ip} - is offline - {emoji}\n".format(emoji=emoji, device_name=device_name,
                                                                                   ip=ip_address)
                messages.append((chimetext[:150] + '..') if len(chimetext) > 150 else chimetext)
            # print('-' * 80 + 'I am device end\n')
        # print('-' * 80 + 'I am Room END\n')
    # print('-' * 80 + 'I am dataEnd\n')

t1 = time.time()
print('Phewww! I check {room_count} rooms today in {time} secs.\n I found {devices_online} Online out of {'
      'device_count}.\n I found {devices_offline} devices Offline'.format(time=t1 - t0, room_count=room_count,
                                                                          devices_online=devices_online,
                                                                          device_count=device_count,
                                                                          devices_offline=devices_offline))
report = 'Phewww! I check {room_count} rooms today in {time} secs.\n I found {devices_online} Online out of {' \
         'device_count}.\n I found {devices_offline} devices Offline'.format(time=t1 - t0, room_count=room_count,
                                                                             devices_online=devices_online,
                                                                             device_count=device_count,
                                                                             devices_offline=devices_offline)
messages = [report] + messages
r = session.post(whurl, headers=headers, json={"Content": message.format(rooms='\n'.join(messages))})
