import requests
from bs4 import BeautifulSoup

class BioskopPretrazivac:
    def __init__(self):
        stranica=requests.get('https://www.cineplexx.rs/filmovi/repertoar/')
        self.soup=BeautifulSoup(stranica.content, 'html.parser')

    def pretraga_filmovi_zanr(self):
        filmovi=dict()
        filmovi_div=self.soup.find_all('div',class_="starBoxSmall three-lines")
        for f in filmovi_div:
            naslov=str(f.find_all('p')[0]).replace('<p>','').replace('</p>','')
            zanr=str(f.find_all('p')[1])

            zanr=zanr.split('|',1)[0].replace('<p>',"").replace(" ","")

            for z in zanr.split(','):
                if z in filmovi:
                    filmovi[z].append(naslov)
                else:
                    filmovi[z]=[naslov]
        return filmovi

