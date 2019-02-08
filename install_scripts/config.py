#!/usr/bin/env python3

import configparser

print("Now we will configure your telegram bot")
print("The token looks like this: 12345:ABCDE_FG_HI and is given to you by the BotFather")
token = input("Enter the token: ")

authorized = []
print("Now enter telegram usernames of people, that should be authorized to control this device")
tmp = input("Enter a username: ")
while(tmp != ''):
	authorized.append(tmp)
	tmp = input("Enter another username: ")

subscribers = []

config = configparser.ConfigParser()
config['Telegram'] = {	'BotToken': token, 
			'Authorized': authorized,
			'Subscribers': subscribers,
			'LastMsgID': 0,
			'Offset': 0
			}

with open('/etc/burglar_warner/Burglar-Warner.conf', 'w') as configfile:
	config.write(configfile)

print("Config file has been saved to /etc/burglar_warner/Burglar-Warner.conf")

