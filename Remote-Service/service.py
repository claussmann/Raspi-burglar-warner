import time
import os
import json
import subprocess

########################################################
# main:
# every 10s:
#   retrieve latest messages
#     if new messages:
#       parse to json
#       extract username, chatid, messageid and message content
#       save new id of latest message (otherwise it would process messages twice)
#       save new offset (offset changes from time to time, max 100 massages can be send at once, see telegram api for details)
#       call process message
########################################################
def main():
	global offset
	global lastmsgID
	global botToken

	while(1):
		url = "https://api.telegram.org/bot" + botToken + "/getUpdates?offset=" + offset
		response = subprocess.Popen(["curl", "-s", "-X", "POST", url], stdout=subprocess.PIPE).stdout.read()
		data = json.loads(response)
		if(data["ok"] == True):
			result = data["result"]
			if(result[-1]["message"]["message_id"] <= int(lastmsgID)):
				continue
			username = result[-1]["message"]["from"]["username"]
			chatID = result[-1]["message"]["chat"]["id"]
			message = result[-1]["message"]["text"]
			lastmsgID = result[-1]["message"]["message_id"]
			open("lastmsgID", "w+").write(str(lastmsgID))
			try:
				newOffset = str(result[-1]["message"]["entities"][-1]["offset"])
				if(newOffset != offset):
					offset = newOffset
					open("offset", "w+").write(str(offset))
			except KeyError:
				continue
			processMsg(message, username, chatID)
		
		time.sleep(10)

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
	if(isSenderAuthorized(username) != True):
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
########################################################
# isSenderAuthorized
# returns True if 'username' is included in the File 'authorized'
########################################################
def isSenderAuthorized(username):
	users = open("authorized", "r").read()
	users = users.split('\n')
	if(username != ''):
		return username in users
	return False


########################################################
# remote functions
########################################################
def startMotion(chatID):
	global botToken
	os.system("motion")
	url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + str(chatID) + "&text=Motion%20started"
	subprocess.Popen(["curl", "-s", "-X", "POST", url])

def stopMotion(chatID):
	global botToken
	os.system("killall motion")
	url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + str(chatID) + "&text=Motion%20stopped"
	subprocess.Popen(["curl", "-s", "-X", "POST", url])

def sendStatus(chatID):
	global botToken
	url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + str(chatID) + "&text=I%20am%20alive"
	subprocess.Popen(["curl", "-s", "-X", "POST", url])

def sendPic(chatID):
	print ("foo")

def poweroff(chatID):
	global botToken
	url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + str(chatID) + "&text=Bye"
	subprocess.Popen(["curl", "-s", "-X", "POST", url])
	os.system("sudo poweroff")

def reboot(chatID):
	global botToken
	url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + str(chatID) + "&text=Bye"
	subprocess.Popen(["curl", "-s", "-X", "POST", url])
	os.system("sudo reboot")





########################################################
# startup and config
########################################################
def openConfig():
	global offset
	global lastmsgID
	global botToken
	try:
		offset = open("offset", "r").read()
		offset = offset.replace('\n','')
	except:
		offset = "0"
	try:
		lastmsgID = open("lastmsgID", "r").read()
		lastmsgID = lastmsgID.replace('\n','')
	except:
		lastmsgID = 0
	botToken = open("botToken", "r").read()
	botToken = botToken.replace('\n','')


openConfig()
main()
