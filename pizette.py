from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import requests
import json
import random
import wikipedia
wikipedia.set_lang('pt')
import pyautogui
# from webdriver_manager.chrome import ChromeDriverManager

def inbox():
	try:
		vd = pyautogui.locateCenterOnScreen(r'find.bmp')
		pyautogui.click(vd[0]-10,vd[1])
	except Exception as ex:
		print(ex)
		pass

chatbot = ChatBot('Pizette')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.portuguese')
trainer.train('chatterbot.corpus.english')
trainerer = ListTrainer(chatbot)


dir_path = os.getcwd()

# O chrome_options2 cria e armazena tudo necessario para a entrada do app no wpp sem a necessicade de nova leitura de QR.
chrome_options2 = Options()
chrome_options2.add_argument(r"user-data-dir="+dir_path+"/profile/wpp")

# driver1 = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(chrome_options=chrome_options2)
driver.get('https://web.whatsapp.com/')
driver.implicitly_wait(15)

"""
	Funcao que identifica a ultima mensagem da conversa, de cada conversa.
"""
def catchConversation():
	try:
		post = driver.find_elements_by_class_name('_3zb-j') # Elemento classe achado por inspecao na pagina do wpp web. Muda de acordo com a maquina.
		last_received_message = len(post) - 1
		last_received_text = post[last_received_message].find_element_by_css_selector('span.selectable-text').text # Selecao do ultimo texto da conversa.
		return last_received_text
	except:
		pass

"""
	Funcao que e responsavel por enviar a mensagem do (no caso) Pizette.
"""
def sendMessage(message):
	text_box = driver.find_element_by_class_name("_2S1VP") # Elemento classe achado por inspecao na pagina do wpp web, no caso aqui caixa de texto. Muda de acordo com a maquina.
	value = '*Pizette:* '+str(message)
	for part in value.split('\n'):
		text_box.send_keys(part)
		ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform() # Simula o Shift+Enter, para que se quebre a linha da mensagem enviada.
	time.sleep(0.5) # Tempo de espera para envio e para se receber novas informacoes do usuario.
	send_botton = driver.find_element_by_class_name('_35EW6') # Elemento classe achado por inspecao na pagina do wpp web, no caso aqui e o botao. Muda de acordo com a maquina.
	send_botton.click()


"""
	Funcao que e responsavel pelo treino
"""
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

def dolar():
	try:
		requsd = requests.get("https://economia.awesomeapi.com.br/all")
		coins = json.loads(requsd.text)
		usd = coins['USD']['high']
		message = "Dólar agora: R${:.4}".format(usd)
		sendMessage(message)
	except:
		sendMessage("Agora não...")
		pass

def weather():
	try:
		#descoberta cidade
		town = str(catchConversation().lower().strip()[6:]) #tempo sãopaulo
		city = requests.get(f'http://apiadvisor.climatempo.com.br/api/v1/locale/city?name={town}&token=80d29a9f70b8f2c7eb385cf1b6463857')
		city2 = json.loads(city.text)
		print(city2)
		idd = city2[0]['id']
		county = city2[0]['name']
		state = city2[0]['state']
		#fazer consulta com id tempo agora
		city3 = requests.get(f'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/{idd}/current?token=80d29a9f70b8f2c7eb385cf1b6463857')
		city4 = json.loads(city3.text)
		print(city4)
		temperature = city4['data']['temperature']
		cond = city4['data']['condition']
		message = f'Tempo Agora para: *{county}-{state}*\n{temperature} Cº, {cond}'
		sendMessage(message)
	except:
		message = 'Da próxima vez tente: *"tempo +cidade brasileira"*'
		sendMessage(message)

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

while True:
	try:
		inbox()
		pass
		if catchConversation() != '' and catchConversation()[:7] != "Pizette: " and catchConversation() != save and catchConversation().strip() != "!" and catchConversation().strip() != ";" and catchConversation().strip().lower() == 'dolar' and catchConversation().strip().lower() == 'dólar' and catchConversation().lower().strip()[0:6] == 'tempo' and catchConversation().strip().lower() == 'notícias' and catchConversation().strip().lower() == 'noticias' and catchConversation().strip().lower()[0:2] != "w:":
			text = str(catchConversation().lower().strip())
			response = chatbot.get_response(text)
			if float(response.confidence) < 0.5:
				pratice(catchConversation())
			else:
				sendMessage(response)
		elif catchConversation().strip().lower() == 'dolar' or catchConversation().strip().lower() == 'dólar':
			dolar()
		elif catchConversation().lower().strip()[0:6] == 'tempo':
			weather()
		elif catchConversation().strip().lower() == 'noticias' or catchConversation().strip().lower() == 'notícias':
			news()
		elif catchConversation().strip().lower()[0:2] == "w:":
			try:
				search = str(catchConversation().strip().lower()[2:])
				message = "{}".format(wikipedia.summary(search))
				sendMessage(message)
			except:
				sendMessage("Nao encontrei nada relevante para '{}' na Wikipedia em portugues.".format(search))
		else:
			pass
	except:
		pass
