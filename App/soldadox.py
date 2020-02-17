from flask import Blueprint, current_app, request, jsonify
from .model import State, Ddd, Region
from .serealizer import StateSchema, DddSchema, RegionSchema
from .crawler import Crawler


bp_soldadox = Blueprint('soldadox', __name__)
ss = StateSchema()
dds = DddSchema()
rs = RegionSchema()
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
            return "Não constam esta combinação de região e ddd , favor verificar", 400
    elif 'ddd' in request.json.keys():
        uri = Ddd.query.filter_by(name=request.json['ddd']).first().url
    elif 'state' in request.json.keys():
        uri = State.query.filter_by(initials=request.json['state']).first().url
    else:
        uri = "https://olx.com.br/brasil/"

    search = {
        'url_ini': uri,
        'itempesquisa': request.json['search'],
        'limit_pag': request.json['nofp'] if request.json['nofp'] != None else 1
    }

    result = Crawler().get_ads(
        url_ini=search['url_ini'], itempesquisa=search['itempesquisa'], limit_pag=search['limit_pag'])

    return jsonify(result), 200


@bp_soldadox.route('/api/ad/<adcode>', methods=['GET'])
def get_ad(adcode):
    result = Crawler().get_ad(cod=adcode)
    return jsonify(result), 200