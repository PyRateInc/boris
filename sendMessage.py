from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

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