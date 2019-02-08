#!/usr/bin/env python3

import time
import os
import json
import subprocess
import configparser
from urllib.parse import quote_plus

########################################################
# main:
# every 10s:
#   retrieve latest messag
#     if new messages:
#       extract username, chatid, messageid and message content
#       save new id of latest message (otherwise it would process messages twice)
#       call process message
########################################################
def main():
	global lastmsgID
	while(1): 
		message = getLatestMessage()
		if(message != ""):
			if(message["message"]["message_id"] > int(lastmsgID)):
				username = message["message"]["from"]["username"]
				chatID = message["message"]["chat"]["id"]
				content = message["message"]["text"]
				lastmsgID = message["message"]["message_id"]
				config['Telegram']['LastMsgID'] = str(lastmsgID)
				with open('/etc/burglar_warner/Burglar-Warner.conf', 'w') as configfile:
					config.write(configfile)
				processMsg(content, username, chatID)
		time.sleep(10)


def getLatestMessage():
	global offset
	global botToken
	global config
	url = "https://api.telegram.org/bot" + botToken + "/getUpdates?offset=" + offset
	response = subprocess.Popen(["curl", "-s", "-X", "POST", url], stdout=subprocess.PIPE).stdout.read()
	try:
		data = json.loads(response.decode('utf-8'))
	except:
		return ""
	if(data["ok"] == True):
			result = data["result"][-1]
			try:
				newOffset = str(result["update_id"])
				if(newOffset != offset):
					offset = newOffset
					config['Telegram']['Offset'] = offset
					with open('/etc/burglar_warner/Burglar-Warner.conf', 'w') as configfile:
						config.write(configfile)
			except KeyError:
				return ""
			return result
	else:
		print("Error. Cannot recieve messages")
		return ""





########################################################
# processMsg
# if sender is authorized, the command will be executed.
# valid commands:
# /start (start motion)
# /stop (stop motion)
# /status (send 'alive-signal')
# /now (send a picture right now)
# /poweroff (poweroff the system)
# /reboot (reboot the system)
########################################################
def processMsg(message, username, chatID):
	global authorized
	if(username not in authorized):
		return
	if(message == "/start"):
		startMotion(chatID)
	if(message == "/stop"):
		stopMotion(chatID)
	if(message == "/status"):
		sendStatus(chatID)
	if(message == "/now"):
		sendPic(chatID)
	if(message == "/poweroff"):
		poweroff(chatID)
	if(message == "/reboot"):
		reboot(chatID)
	if(message == "/subscribe"):
		subscribe(chatID)
	if(message == "/unsubscribe"):
		unsubscribe(chatID)


########################################################
# remote functions
########################################################
def startMotion(chatID):
	subprocess.Popen(["motion", "-c", "/etc/burglar_warner/motion/motion.conf", "-b"])
	sendMsg(chatID, "Started.")

def stopMotion(chatID):
	subprocess.Popen(["killall", "motion"])
	sendMsg(chatID, "Stopped.")

def sendStatus(chatID):
	sendMsg(chatID, "I am still here.")

def sendPic(chatID):
	sendMsg(chatID, "One second...")
	photoLocation = "/etc/burglar_warner/motion/pics/latest_snapshot.jpeg"
	subprocess.Popen(["raspistill", "-w", "500", "-h", "300", "-q", "90", "-o", photoLocation]).wait()
	sendImg(chatID, photoLocation)

def poweroff(chatID):
	sendMsg(chatID, "Bye.")
	time.sleep(2)
	os.system("sudo poweroff")

def reboot(chatID):
	sendMsg(chatID, "Back soon...")
	time.sleep(2)
	os.system("sudo reboot")

def subscribe(chatID):
	global config
	chatIDs = eval(config['Telegram']['Subscribers'])
	if(str(chatID) not in chatIDs):
		chatIDs.append(str(chatID))
		config['Telegram']['Subscribers'] = str(chatIDs)
		with open('/etc/burglar_warner/Burglar-Warner.conf', 'w') as configfile:
			config.write(configfile)
		sendMsg(chatID, "Subscribed.")
	else:
		sendMsg(chatID, "Already subscribed")

def unsubscribe(chatID):
	global config
	chatIDs = eval(config['Telegram']['Subscribers'])
	if(str(chatID) in chatIDs):
		chatIDs.remove(str(chatID))
		config['Telegram']['Subscribers'] = str(chatIDs)
		with open('/etc/burglar_warner/Burglar-Warner.conf', 'w') as configfile:
			config.write(configfile)
		sendMsg(chatID, "Removed")
	else:
		sendMsg(chatID, "You are no subscriber")

########################################################
# methods to send text and photos
########################################################
def sendMsg(chatID, msg):
	global botToken
	msg = quote_plus(msg)
	url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + str(chatID) + "&text=" + msg
	subprocess.Popen(["curl", "-s", "-X", "POST", url])

def sendImg(chatID, imgPath):
	global botToken
	url = "https://api.telegram.org/bot" + botToken + "/sendPhoto"
	os.system("curl -s -X POST " + url + " -F chat_id=" + str(chatID) + " -F photo='@" + imgPath + "'")


########################################################
# startup and config
########################################################
def openConfig():
	global offset
	global lastmsgID
	global botToken
	global authorized
	global config
	config = configparser.ConfigParser()
	config.read('/etc/burglar_warner/Burglar-Warner.conf')
	botToken = config['Telegram']['BotToken']
	offset = config['Telegram']['Offset']
	lastmsgID = config['Telegram']['LastMsgID']
	authorized = eval(config['Telegram']['Authorized'])

openConfig()
main()
