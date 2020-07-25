from pizette import *
import requests
import json
import random


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

save = catchConversation()