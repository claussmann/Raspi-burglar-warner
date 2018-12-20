import time
import json
import subprocess

def main():
	offset = open("offset", "r").read()
	botToken = open("botToken", "r").read()
	lastmsgID = open("lastmsgID", "r").read()
	offset = offset.replace('\n','')
	botToken = botToken.replace('\n','')
	lastmsgID = lastmsgID.replace('\n','')
	
	while(1):
		url = "https://api.telegram.org/bot" + botToken + "/getUpdates?offset=" + offset
		response = subprocess.Popen(["curl", "-s", "-X", "POST", url], stdout=subprocess.PIPE).stdout.read()

		data = json.loads(response)
		if(data["ok"] == True):
			result = data["result"]
			if(result[-1]["message"]["message_id"] <= int(lastmsgID)):
				continue
			username = result[-1]["message"]["from"]["username"]
			message = result[-1]["message"]["text"]
			lastmsgID = result[-1]["message"]["message_id"]
			open("lastmsgID", "w").write(str(lastmsgID))
			try:
				newOffset = str(result[-1]["message"]["entities"][-1]["offset"])
				if(newOffset != offset):
					offset = newOffset
					open("offset", "w").write(str(offset))
			except KeyError:
				continue
			if(isSenderAuthorized(username)):
				processMsg(message)
		
		time.sleep(10)

def processMsg(message):
	print(message)

def isSenderAuthorized(username):
	return username == "claussmann"

main()
