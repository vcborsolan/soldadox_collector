from flask import Blueprint , current_app , request
from .model import State , Ddd , Region
from .serealizer import StateSchema , DddSchema , RegionSchema
from .crawler import Crawler
import json

bp_soldadox = Blueprint('soldadox' , __name__ )
ss = StateSchema()
dds = DddSchema()
rs = RegionSchema()
@bp_soldadox.route('/show', methods=['GET'])
def mostrar():
    result_ss = State.query.all()
    result_dds = Ddd.query.all()
    result_rs = Region.query.all()[0]
    return rs.jsonify(result_rs), 200

@bp_soldadox.route('/cadastrar' , methods=['POST'])
def cadastrar():
    request_json = request.json
    # import ipdb; ipdb.set_trace()
    ss = StateSchema()
    for x in request_json[0]:
        state = ss.load(x)
        current_app.db.session.add(state)
        current_app.db.session.commit()
    for x in request_json[1]:
        ddd = Ddd(name=x['name'] , url=x['url'],state=State.query.filter_by(id=x['state_id']).first())
        current_app.db.session.add(ddd)
        current_app.db.session.commit()
    for x in request_json[2]:
        region = Region(name=x['name'] , url=x['url'],ddd=Ddd.query.filter_by(id=x['ddd_id']).first())
        current_app.db.session.add(region)
        current_app.db.session.commit()
    # Fazer o for para cadastrar as info de regiao...
    return "ok",200

@bp_soldadox.route('/api', methods=['POST'])
def crawler_api():

    if 'region' in request.json.keys() and 'ddd' in request.json.keys():
        try:
            ddd = Ddd.query.filter_by(name = request.json['ddd']).first()
            region = ddd.regions.filter_by(name=request.json['region']).first()
            uri = region.url
        except AttributeError as error:
            return "Não constam esta combinação de região e ddd , favor verificar", 400
    elif 'ddd' in request.json.keys():
        uri = Ddd.query.filter_by(name = request.json['ddd']).first().url
    elif 'state' in request.json.keys():
        uri = State.query.filter_by(initials = request.json['state']).first().url
    else:
        uri = "https://olx.com.br/"

    # print(uri)

    result = Crawler().get_ads(url_ini=uri , itempesquisa=request.json['search'], limit_pag=1)

    result = json.dumps(result)
    
    return result,200    