#!/usr/bin/env python3

import subprocess
import os

botToken = open("/etc/burglar_warner/notifier/botToken", "r").read()
botToken = botToken.replace('\n','')

chatIDs = open("/etc/burglar_warner/notifier/chatIDs", "r").read()
chatIDs = chatIDs.split('\n')

filesSortedByModifyDate = subprocess.Popen(["ls", "-t", "/etc/burglar_warner/motion/pics"], stdout=subprocess.PIPE).stdout.read()
filesSortedByModifyDate = filesSortedByModifyDate.split('\n')

lastModified = filesSortedByModifyDate [0]
lastModified = "/etc/burglar_warner/motion/pics/" + lastModified

for chatID in chatIDs:
	url = "https://api.telegram.org/bot" + botToken + "/sendPhoto"
	os.system("curl -s -X POST " + url + " -F chat_id=" + chatID + " -F photo='@" + lastModified + "'")

