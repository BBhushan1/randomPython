import json
import subprocess
from subprocess import DEVNULL
import requests, urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

whurl = "https://hooks.chime.aws/incomingwebhooks/b79f7d1c-9c2f-4666-93df-a791ef9d6136?token=c2lHNmJxd2x8MXxaV3M5SE9QQmFpZ18ydVE2MExWVnc3NzQ0c2o5MnJCOXB2NU5CcG4yS2tz"
session = requests.Session()
headers = {"Content-Type": "application/json"}
messages = []
session.verify = False
message = "Check the output below:\n {rooms}"
files = ["bom.json", "pnq.json"]


def mainHandler(filename):
    messages = []
    t0 = time.time()
    with open(filename) as json_file:
        room_count = 0
        device_count = 0
        devices_online = 0
        devices_offline = 0
        data = json.load(json_file)
        for room in data:
            messages.append(room['room_name'])
            room_count += 1
            for device in room['devices']:
                device_count += 1
                room_name = room['room_name']
                device_name = device['device_name']
                ip_address = device['device_ip']
                ping_result = subprocess.call(["ping", "-n", "-W5", "-c3", ip_address], stdout=DEVNULL)
                if ping_result == 0:
                    devices_online += 1
                    emoji = ":white_check_mark:"
                    chimetext = "{device_name} : {ip} - is active - {emoji}".format(emoji=emoji,
                                                                                    device_name=device_name,
                                                                                    ip=ip_address)
                    messages.append((chimetext[:150] + '..') if len(chimetext) > 150 else chimetext)
                elif ping_result == 2:
                    devices_offline += 1
                    emoji = ":rotating_light:"
                    chimetext = "{device_name} : {ip} - is offline - {emoji}".format(emoji=emoji,
                                                                                     device_name=device_name,
                                                                                     ip=ip_address)
                    messages.append((chimetext[:150] + '..') if len(chimetext) > 150 else chimetext)
                else:
                    emoji = ":rotating_light:"
                    devices_offline += 1
                    chimetext = "{device_name} : {ip} - is offline - {emoji}\n".format(emoji=emoji,
                                                                                       device_name=device_name,
                                                                                       ip=ip_address)
                    messages.append((chimetext[:150] + '..') if len(chimetext) > 150 else chimetext)

    t1 = time.time()
    report = 'Phewww! I checked {room_count} rooms today in {time} secs.\n I found {devices_online} devices online ' \
             'out of {device_count}.\n I found {devices_offline} devices Offline'.format(time=t1 - t0,
                                                                                         room_count=room_count,
                                                                                         devices_online=devices_online,
                                                                                         device_count=device_count,
                                                                                         devices_offline=devices_offline)
    messages = [report] + messages
    return messages


t0 = time.time()
print('-' * 80 + '\nExec started\n')
for site in files:
    report = mainHandler(site)
    text = "Reading file {site} for details of rooms and devices. Report below this message.".format(site=site)
    messages = [text] + report

    r = session.post(whurl, headers=headers, json={"Content": message.format(rooms='\n'.join(messages))})

t1 = time.time()
print('Exec Ended\nTotal Execution Time: {time} secs\n'.format(time=t1-t0) + '-' * 80)
