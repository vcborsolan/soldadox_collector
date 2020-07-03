from flask import Blueprint, current_app, request, jsonify
from .model import State, Ddd, Region  ,Ad , Image
from .serealizer import StateSchema, DddSchema, RegionSchema , AdSchema , ImageSchema
from .crawler import Crawler
import time


bp_soldadox = Blueprint('soldadox', __name__)
ss = StateSchema()
dds = DddSchema()
rs = RegionSchema()
ads = AdSchema()
@bp_soldadox.route('/show', methods=['GET'])
def mostrar():
    result_ss = State.query.all()
    result_dds = Ddd.query.all()
    result_rs = Region.query.all()[0]
    return rs.jsonify(result_rs), 200


@bp_soldadox.route('/cadastrar', methods=['POST'])
def cadastrar():
    request_json = request.json
    ss = StateSchema()
    for x in request_json[0]:
        state = ss.load(x)
        current_app.db.session.add(state)
        current_app.db.session.commit()
    for x in request_json[1]:
        ddd = Ddd(name=x['name'], url=x['url'],
                  state=State.query.filter_by(id=x['state_id']).first())
        current_app.db.session.add(ddd)
        current_app.db.session.commit()
    for x in request_json[2]:
        region = Region(name=x['name'], url=x['url'],
                        ddd=Ddd.query.filter_by(id=x['ddd_id']).first())
        current_app.db.session.add(region)
        current_app.db.session.commit()
    return "ok", 200


@bp_soldadox.route('/api/ads', methods=['POST'])
def crawler_api():

    if 'region' in request.json.keys() and 'ddd' in request.json.keys():
        try:
            ddd = Ddd.query.filter_by(name=request.json['ddd']).first()
            region = ddd.regions.filter_by(name=request.json['region']).first()
            uri = region.url
        except AttributeError as error:
            return f"Não constam esta combinação de região e ddd , favor verificar | erro {error}", 400
    elif 'ddd' in request.json.keys():
        uri = Ddd.query.filter_by(name=request.json['ddd']).first().url
    elif 'state' in request.json.keys():
        uri = State.query.filter_by(initials=request.json['state']).first().url
    else:
        uri = "https://olx.com.br/brasil/"

    search = {
        'url_ini': uri,
        'itempesquisa': request.json['search'],
        'limit_pag': request.json['nofp'] if request.json['nofp'] != None else 1 ,
        'ult_anuncio': request.json['lastAd'] if request.json['lastAd'] != None else "0"
    }

    result = Crawler().get_ads(
            url_ini=search['url_ini'],
            itempesquisa=search['itempesquisa'],
            limit_pag=search['limit_pag'] ,
            ult_anuncio=search['ult_anuncio']
        )

    if result != None:

        for x in result:
            
            salvaAd(x)
            time.sleep(0.2)

        
    else:
        return f"Erro linha 75", 400
    
    return jsonify(result), 200


@bp_soldadox.route('/api/ad/<adcode>', methods=['GET'])
def get_ad(adcode):
    # import ipdb; ipdb.set_trace()

    ad = Ad.query.filter_by(cod=adcode).first()
    if ad == None:

        result = Crawler().get_ad(cod=adcode)

        if result == None:
            return "erro anuncio nao disponivel", 400

        else:            

            if salvaAd(result):

                time.sleep(0.2)
                return ads.jsonify(result), 200
            else:
                return f"erro ao salvar anuncio", 400
            # return ads.jsonify(result), 200 if salvaAd(result) else f"erro ao salvar anuncio", 400
            # linha 97 ate 102 deveria funcionar com a linha 103 mas n sei explicar pq falha
    a = []
    for x in ad.images:
        a.append(x.url)
    return jsonify(id= ad.id , images= a , value= ad.value , publication= ad.publication , description= ad.description , cod= ad.cod , category = ad.category , state = ad.state , region= ad.region , subregion= ad.subregion , url= ad.url),200


@bp_soldadox.route('/cron', methods=['POST'])
def cron_do():
    # import ipdb; ipdb.set_trace()

    print("começou o cron")

    last_ad = Ad.query.order_by(Ad.id.desc()).first()

    result = Crawler().get_ads(
	    url_ini = "https://sp.olx.com.br/regiao-de-bauru-e-marilia" ,
	    itempesquisa = "",
	    limit_pag = 5,
	    ult_anuncio = last_ad.cod
    )

    if result != None:

        for x in result:
            
            salvaAd(x)

        time.sleep(0.5)

        return "ok",200

    else:
        return "Erro ao coletar os dados",400


def salvaAd(result):
    
    try:
        ad = Ad(value=result['value'],publication=result['publication'],description=result['description'],cod=result['cod'],category=result['category'],state=result['state'],region=result['region'],subregion=result['sub-region'],url=result['url'])

        current_app.db.session.add(ad)
        current_app.db.session.commit()

        for i in result['images']:
            image = Image(ad_id=Ad.query.filter_by(cod=result['cod']).first().id,url=i)
            current_app.db.session.add(image)
            current_app.db.session.commit()
    except Exception as error:
           return False

    return True