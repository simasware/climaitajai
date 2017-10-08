# Clima Itajai 
# Fernando de Simas - 2017
# 
# Busca informações do openWeather e posta na conta twitter.com/climaitajai

import json
import codecs
import datetime
import twitter
from urllib.request import urlopen

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?id={}&lang=pt&APPID={}&units=metric'
TWEET_STR = 'Em {} faz {} graus. Nebulosidade: {} %. Umidade relativa do ar: {} %. [{}] #itajai #climaitajai'

def carrega_config():
	return json.loads(open('config.json').read())	

def retorna_info_tempo(cidade_id, openweather_key):
	f = urlopen(WEATHER_URL.format(cidade_id, openweather_key))		
	reader = codecs.getreader("utf-8")
	return json.load(reader(f))

def tweet(config, info_tempo):		
	api = twitter.Api(config['consumer_key'],
                      config['consumer_secret'],
                      config['access_token_key'],
                      config['access_token_secret'])
	status = TWEET_STR.format(
			info_tempo['name'],
			info_tempo['main'].get('temp'), 
			info_tempo['clouds'].get('all'),
			info_tempo['main'].get('humidity'),
			datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
	print("Enviando tweet: {}".format(status))
	api.PostUpdate(status)

def main():
	config = carrega_config()
	info_tempo = retorna_info_tempo(config['CIDADE_ID'],config["OPENWEATHER_KEY"])
	try:
		tweet(config, info_tempo)			
	except Exception as e:
		print("Erro ao enviar tweet: " + str(e))
	else:
		pass
	finally:
		pass
	

if __name__ == "__main__":
    main()