import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


class Crawler:

    def __init__(self):

        self.loop = True
        self.ads = []

    def status(self, url):

        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.94',
            'Cookie': 'r_id=91f6ef4f-dd52-4df0-9642-0aa6b04b9d2f; xtvrn=$483760$; xtan=-; xtant=1; session_id=bafba320-0b89-11ea-ac40-45814e740b17; fbm_106401512762894=base_domain=.olx.com.br; ACC_LL=1|NzcxNzY5NTMyODMzNzYz; loginIdentifier=YzMzOTQ3N2ZiZTY1NGZmYjA1MWFhNWZmMThkZDNjMDA6ZWQzODRlNGU2ZTAyMzIwNjkyZGY1NDk1ZDQ3OWQ0M2QzYjQ5MDJmNzQ4NTk4ZGIwMjljODAyNTA1OTJhZDE0MGViMmIwYmI5NDA3YzhlZjEzOWM1NWMyZDljMWUzMGE4NWVkN2RiODJkYTE0ZmFhNzhkZGE5NmE3Y2IwZGQ3MDk0ZWEyNDQxNjVmOTJiNWM5OGY1OGJmZmQwMzA0NGUwNGI3ODJhMjE1OTEyMzQ4ZDc1ZGMxNTc2NGM0OWMyZmNkMDcwZThiM2JlNWIxNjgwM2JlYjhjYjI3MDM1Zjg3YzE1MTkxMGFjZDk1YmMxZTVhMDEzMDU4N2JmMDhiOGQxNjJiMmQ1ZDU4NTg3MTZhZjQwYzc1NTliZjY5ODBlMTJj; _hjid=a2f7fc03-3314-47ae-b2be-767fb50ae24b; default_reg=11; s=mc1x118db819523382a810cc64b8c3dd0fc98acb183b; las=712169206-705328112-702495993-713430444-718035733; TestAB_Groups=advAfshNativo_A.ast-showphone-flow_new.autos-completion-popup_fullFeedback.bj-HelpMeDecide_SellerOnlineTitle.bj-listItemOpenInANewTab_A.bj-new-listing-desktop-partial_lazy-load-online-sellers.cars-adview-fipe_enabled.cars-ai-data-seller_control.fixedBar2_box.helpcenter-live-agent_control.imo-597-preview_show.mes-warning-message_new.mfg-autos-market-place-selected-options_early.mfg-autos-market-place_control.myads-new-expired_A.myads-new-pendingpay_A.myads-new-pendingpublish_A.myads-new-published_A.osp-flex-plan-cars-subscription_control.osp-flex-plan-realestate-subscription_control.osp-insidesales-phone-web_withphone.osp-new-layout-ai-web_scroll.osp-step-choice-cars-subscription-web_control.osp-step-choice-real-estate-web_control.passwordless-sign-in-on-login_control.passwordless-sign-in-on-register_yes.payments-boletoProgressButton_A.remember-last-login-on-home_control.removalAdOnboard_A.smart-lock-login_yes.upr-cards-infinite-scroll_control.upr-chat-adview-profilelink_A.upr-chat-listing-profilelink_A.upr-profile-cards_A.upr-profile-new-account-validation-icons_A.upr-profile-trust-profile-links_A.uprNewMiniProfile_control.uprNewMonthActivityRule_control',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive'
        }

        # Vai ter q dar um jeito de gerar o cookie , fudeu...
        # aparentemente o cookie sendo valido nao importa a qtd de request ou limite de tempo ent~ao ta ok ...

        req = requests.get(url, headers=hdr)

        return {'status': True, 'request': req} if req.status_code == 200 else {'status': False, 'request': req}

    def get_ads(self, url_ini, itempesquisa, ult_anuncio="0", limit_pag=1):

        i = 1

        while self.loop:
            URL = f"{url_ini}?o={i}&q={itempesquisa}&sf=1"
            # import ipdb; ipdb.set_trace()
            if i <= limit_pag:
                status = self.status(URL)
                # ^ "https://www.olx.com.br/brasil?o=2&q=guitarra&sf=1"  o=pagina | q=query | sf= ordenação da pagina 1>> mais recente
                if status['status']:
                    soup = BeautifulSoup(
                        status['request'].content, 'html.parser')
                    links = soup.find_all(
                        "a", attrs={"data-lurker-detail": "list_id"})
                    for link in links:
                        if link.attrs['data-lurker_list_id'] > ult_anuncio:
                            self.ads.append(self.get_ad(
                                url=link.attrs['href']))
                        else:
                            self.loop = False
                            break

                    i += 1
                else:
                    break
            else:
                self.loop = False

        return self.ads

    def get_ad(self, url="", cod=""):

        return self.get_ad_by_url(url) if url != "" else self.get_ad_by_cod(cod)

    def get_content(self  ,soup , status):

        imgs = []
        tmp = soup.find_all('img', class_='image')

        try:
            a = soup.find('dt', text='Categoria').findNext('a').get_text() 
        except AttributeError:
            a = soup.find('span' , text='Categoria').findNext('a').get_text()
            
        for x in tmp:
            imgs.append(x.attrs['src'])

        pub = ""
        cod = ""
        for x in soup.find_all('span'):
            if "Publicado em" in x.get_text() :
                pub = x.get_text()
            if "cód." in x.get_text() :
                cod = x.get_text()

        ad = {
            "value": soup.find_all('h2')[0].get_text(),
            "publication": self.correct_time(pub),
            "description": soup.find_all('p')[0].get_text() ,
            "cod": cod.replace('cód. ', ''),
            "category": a ,
            "images": imgs,
            "state": status['request'].url[8:10].upper(),
            "region": status['request'].url.split('/')[3],
            "sub-region": soup.find_all('a')[9].get_text(),
            "url": status['request'].url
        }

        return ad

    def get_ad_by_cod(self, cod):

        status = self.status(f"https://www.olx.com.br/vi/{cod}.htm?ca=")

        if status['status']:
            soup = BeautifulSoup(status['request'].content, 'html.parser', from_encoding="utf-8")
            ad = self.get_content(soup , status)

            return ad

        else:
            return False

    def get_ad_by_url(self, url):

        status = self.status(url)
        if status['status']:
            soup = BeautifulSoup(status['request'].content, 'html.parser', from_encoding="utf-8")
            ad = self.get_content(soup , status)
            return ad

        else:
            return False

    def correct_time(self, str):

        t = str.replace("Publicado em ", "").replace(
            " às ", f"/{datetime.now().year} ")
        # t = datetime.strptime(t ,"%d/%m/%Y %H:%M")
        return t

# print(Crawler().get_ads(url_ini="https://olx.com.br/brasil" , itempesquisa="Guitarra" ))
# print(Crawler().get_ad_by_cod(cod='736932129'))