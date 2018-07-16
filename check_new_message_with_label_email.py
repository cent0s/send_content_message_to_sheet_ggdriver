#!/usr/bin/python

import datetime
import json
import time
import urllib

import playsound

get_data = urllib.urlopen("https://api.hipchat.com/v2/room/2131073/history?auth_token=doOiTUfbrYXQsMgUZAfpkmOg1DIwJtVkJKpw1fai")
#with open("/tmp/abc.json") as json_file:
json_data = json.load(get_data)
lastest_message = (json_data.values()[0][99])
#    count = len(content_chat)
#    print(count)
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print "Content_last_message: ",(lastest_message['message'])


time.sleep(62)
get_data = urllib.urlopen("https://api.hipchat.com/v2/room/2131073/history?auth_token=doOiTUfbrYXQsMgUZAfpkmOg1DIwJtVkJKpw1fai")
#with open("/tmp/abc.json") as json_file:
json_data = json.load(get_data)
lastest_message_after = (json_data.values()[0][99])
#    count = len(content_chat)
#    print(count)
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print "Content_last_message: ",(lastest_message_after['message'])

if lastest_message == lastest_message_after:
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("We don't have new message , Fine!!!")
#        playsound.playsound('http://www.freesfx.co.uk/rx2/mp3s/6/18145_1464355134.mp3', True)
else:
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("We have new message in Trouble Room, Answer Now !!!")
        playsound.playsound('http://www.freesfx.co.uk/rx2/mp3s/6/18145_1464355134.mp3', True)
#        playsound.playsound('https://www.youtube.com/watch?v=ej_L8Zb2WSM', True)
