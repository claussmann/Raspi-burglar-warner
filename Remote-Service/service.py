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


########################################################
# methods to send text and photos
########################################################
def sendMsg(chatID, msg):
	global botToken
	msg = msg.replace(' ', '%20')
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
