#!/usr/bin/env python3

import subprocess
import os
import configparser

config = configparser.ConfigParser()
config.read('/etc/burglar_warner/Burglar-Warner.conf')

botToken = config['Telegram']['BotToken']

chatIDs = config['Telegram']['Subscribers']

filesSortedByModifyDate = subprocess.Popen(["ls", "-t", "/etc/burglar_warner/motion/pics"], stdout=subprocess.PIPE).stdout.read()
filesSortedByModifyDate = filesSortedByModifyDate.splitlines()

lastModified = filesSortedByModifyDate [0]
lastModified = "/etc/burglar_warner/motion/pics/" + lastModified.decode("utf-8")

for chatID in chatIDs:
	url = "https://api.telegram.org/bot" + botToken + "/sendPhoto"
	os.system("curl -s -X POST " + url + " -F chat_id=" + chatID + " -F photo='@" + lastModified + "'")

