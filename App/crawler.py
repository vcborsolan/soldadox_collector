import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Crawler:
        
    def __init__(self):

        self.loop = True
        self.ads = []

    def status(self , url , redirect=False):
        req = requests.get(url) if redirect == False else requests.get(url , allow_redirects=True)
        return True if (req.status_code == 200 and (req.url == url or req.url == url.replace("o=1&",""))) else False

    def get_ads(self , url_ini , itempesquisa , ult_anuncio = "0" , limit_pag = ""):

        i = 1
        
        while self.loop:
            URL = f"{url_ini}?o={i}&q={itempesquisa}&sf=1"
            if i <= limit_pag:
                # ^ "https://www.olx.com.br/brasil?o=2&q=guitarra&sf=1"  o=pagina | q=query | sf= ordenação da pagina 1>> mais recente
                if self.status(URL):
                    request = requests.get(URL)
                    soup = BeautifulSoup(request.content, 'html.parser')
                    links = soup.find_all("a" , class_="OLXad-list-link")
                    for link in links:                
                        if link.attrs['id'] > ult_anuncio :
                            self.ads.append(self.get_ad(link.attrs['href']))
                        else:
                            self.loop = False
                            break

                    i += 1
                else:
                    break
            else:
                self.loop = False

        return self.ads

    def get_ad(self , url="" , cod=""):

        return self.get_ad_by_url(url) if url != "" else self.get_ad_by_cod(cod)
        
    def get_ad_by_cod(self , cod):

        if self.status(f"https://www.olx.com.br/brasil?q={cod}" , True):
            request = requests.get(f"https://www.olx.com.br/brasil?q={cod}" , allow_redirects=True)
            soup = BeautifulSoup(request.content, 'html.parser')
            imgs = []
            tmp = soup.find_all('img' , class_='image')

            for x in tmp:
                imgs.append(x.attrs['src'])
            
            ad = {
                "value":  soup.find('h2' , class_='sc-bZQynM sc-1wimjbb-0 dSAaHC').get_text() ,
                "publication": self.correct_time(soup.find('span' , class_='sc-bZQynM sc-1oq8jzc-0 dxMPwC').get_text()) ,
                "description": soup.find('p' , class_='sc-1kv8vxj-0 hAhJaI').get_text() ,
                "cod": soup.find('span' , class_='sc-bZQynM sc-16iz3i7-0 cPAPOU').get_text().replace('cód. ' , '') ,
                "category": soup.find('a' , class_='sc-57pm5w-0 sc-1f2ug0x-2 dBeEuJ').get_text() ,
                "images": imgs ,
                "state": request.url[8:10].upper() ,
                "region": request.url.split('/')[3] ,
                "sub-region": soup.find('a' , class_="sc-jKJlTe sc-1aze3je-1 clkGwd").get_text() ,
                "url": request.url
            }

            return ad

        else:
            return False

    def get_ad_by_url(self , url):

        if self.status(url):
            request = requests.get(url)
            soup = BeautifulSoup(request.content, 'html.parser')
            imgs = []
            tmp = soup.find_all('img' , class_='image')

            for x in tmp:
                imgs.append(x.attrs['src'])
            
            ad = {
                "value":  soup.find('h2' , class_='sc-bZQynM sc-1wimjbb-0 dSAaHC').get_text() ,
                "publication": self.correct_time(soup.find('span' , class_='sc-bZQynM sc-1oq8jzc-0 dxMPwC').get_text()) ,
                "description": soup.find('p' , class_='sc-1kv8vxj-0 hAhJaI').get_text() ,
                "cod": soup.find('span' , class_='sc-bZQynM sc-16iz3i7-0 cPAPOU').get_text().replace('cód. ' , '') ,
                "category": soup.find('a' , class_='sc-57pm5w-0 sc-1f2ug0x-2 dBeEuJ').get_text() ,
                "images": imgs ,
                "state": request.url[8:10].upper() ,
                "region": request.url.split('/')[3] ,
                "sub-region": soup.find('a' , class_="sc-jKJlTe sc-1aze3je-1 clkGwd").get_text() ,
                "url": request.url
            }

            return ad

        else:
            return False

            
    def correct_time(self , str):

        t = str.replace("Publicado em ","").replace(" às ", f"/{datetime.now().year} ")
        # t = datetime.strptime(t ,"%d/%m/%Y %H:%M")
        return t