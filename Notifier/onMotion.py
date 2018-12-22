#!/usr/bin/env python3

import subprocess

botToken = open("/etc/burglar_warner/notifier/botToken", "r").read()
botToken = botToken.replace('\n','')

chatIDs = open("/etc/burglar_warner/notifier/chatIDs", "r").read()
chatIDs = chatIDs.split('\n')

for chatID in chatIDs:
	url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + str(chatID) + "&text=I%20think%20there%20is%20somethig..."
	subprocess.Popen(["curl", "-s", "-X", "POST", url])

