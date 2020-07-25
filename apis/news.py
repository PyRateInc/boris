from pizette import *
import requests
import json
import random

def news():
	try:
		req = requests.get('https://newsapi.org/v2/top-headlines?country=br&category=technology&apiKey=f5890e93feef4c049ea5aae620f34174')
		tidings = json.loads(req.text)
		for news in tidings['articles']:
			title = news['title']
			link = news['url']
			desc = news['description']
			message = "{}\n{}\n{}".format(title,desc,link)
			sendMessage(message)
			time.sleep(random.randrange(6/15)/10)
	except:
		sendMessage("agora não...")
		pass

save = catchConversation()
