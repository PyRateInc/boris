from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

def pratice(message):
	answer = "Como respondo isso? me ensine com *;texto com a resposta* ou *!* para desativar o aprendizado para:" + str(message)
	sendMessage(answer)
	new = []
	try:
		while True:
			last_talk = catchConversation()
			if last_talk == "!":
				sendMessage("Você desativou meu aprendizado.")
				break
			elif last_talk.replace(";","") != "" and last_talk != message and last_talk[0] == ";":
				auxiliary = last_talk
				new.append(message.lower().strip())
				new.append(last_talk.replace(";","").strip())
				trainerer.train(new)
				print(message.lower().strip())
				print(last_talk.replace(";","").strip())
				sendMessage("Pronto, aprendizado realizado com sucesso. Obrigado.")
				break
	except:
		pass