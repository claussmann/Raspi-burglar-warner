import subprocess

botToken = open("botToken", "r").read()
botToken = botToken.replace('\n','')

chatIDs = open("chatIDs", "r").read()
chatIDs = chatIDs.split('\n')

for chatID in chatIDs:
	url = "https://api.telegram.org/bot" + botToken + "/sendMessage?chat_id=" + str(chatID) + "&text=I%20think%20there%20is%20somethig..."
	subprocess.Popen(["curl", "-s", "-X", "POST", url])

