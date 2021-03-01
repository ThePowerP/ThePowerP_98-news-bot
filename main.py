import json
import logging
import twitter
import coloredlogs
import requests
from time import sleep
from sys import exit
from util import Utility

log = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="[%(asctime)s] %(message)s", datefmt="%I:%M:%S")


class Athena:
    """Fortnite news bot"""

    def main(self):
        print('Generador de noticias')
        print('Creado por ThePowerP_98')

        initialized = Athena.LoadConfiguration(self)

        if initialized is True:
            if self.delay > 0:
                log.info(
                    f'Retrasando ejecución del programa por {self.delay}s...')
                sleep(self.delay)

            self.newsInfo = Utility.GET(
                self,
                "https://fortnite-api.com/v2/news/br",
                {"x-api-key": self.apiKey},
                {"language": self.language},
            )
            if self.newsInfo is not None:
                self.newsInfo = json.loads(self.newsInfo)['data']
                date = Utility.ISOtoHuman(
                    self, self.newsInfo["date"].split("T")[0], self.language
                )
                log.info(f'Buscando noticias del {date}')
                print('Guardando imagen...')
                url = self.newsInfo['motds'][0]['image']
                r = requests.get(url, allow_redirects=True)
                open("Imagenes/"+self.newsInfo['motds'][0]['id']+'.png', 'wb').write(r.content)
                print("Imagen guardado: "+self.newsInfo['motds'][0]['id'])
                # try:
                #     print('Guardando...' + newsInfo['motds'][0])
                if self.twitterEnabled is True:
                    Athena.Tweet(self, date)
    def LoadConfiguration(self):

        configuration = json.loads(
            Utility.ReadFile(self, "configuracion", "json"))

        try:
            self.delay = configuration["delayStart"]
            self.apiKey = configuration["fortniteAPI"]["apiKey"]
            self.language = configuration["language"]
            self.twitterEnabled = configuration["twitter"]["enabled"]
            self.twitterAPIKey = configuration["twitter"]["apiKey"]
            self.twitterAPISecret = configuration["twitter"]["apiSecret"]
            self.twitterAccessToken = configuration["twitter"]["accessToken"]
            self.twitterAccessSecret = configuration["twitter"]["accessSecret"]
            log.info('Cargando configuración')
            return True
        except Exception as e:
            log.critical(f'Error al cargar la configuración, {e}')

    def Tweet(self, date: str):
        try:
            twitterAPI = twitter.Api(
                consumer_key=self.twitterAPIKey,
                consumer_secret=self.twitterAPISecret,
                access_token_key=self.twitterAccessToken,
                access_token_secret=self.twitterAccessSecret,
            )
            twitterAPI.VerifyCredentials()
        except Exception as e:
            log.critical(f'Error al autentificar con Twitter, {e}')

            return
        body = self.newsInfo['motds'][0]['body']
        try:
            with open('Imagenes/'+self.newsInfo['motds'][0]['id']+'.png', 'rb') as newsImage:
                twitterAPI.PostUpdate(body, media=newsImage)
            log.info('Tweet de las noticias enviado.')
        except Exception as e:
            log.critical(f'Error al Twittear las noticias, {e}')

if __name__ == '__main__':
    try: 
        Athena.main(Athena)
    except KeyboardInterrupt:
        log.info('Saliendo...')
        exit()