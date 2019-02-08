#!/usr/bin/env python3

import subprocess
import configparser

config = configparser.ConfigParser()
config.read('/etc/burglar_warner/Burglar-Warner.conf')

botToken = config['Telegram']['BotToken']

chatIDs = eval(config['Telegram']['Subscribers'])

for chatID in chatIDs:
	url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + str(chatID) + "&text=I%20think%20there%20is%20somethig..."
	subprocess.Popen(["curl", "-s", "-X", "POST", url])

