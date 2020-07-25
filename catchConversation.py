from selenium import webdriver
import os
from pizette import *


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