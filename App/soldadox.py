from flask import Blueprint , current_app , request
from .model import State , Ddd , Region
from .serealizer import StateSchema , DddSchema , RegionSchema

bp_soldadox = Blueprint('soldadox' , __name__ )

@bp_soldadox.route('/show', methods=['GET'])
def mostrar():
    ss = StateSchema(many=True)
    result = State.query.all()
    print(ss.jsonify(result))
    return ss.jsonify(result), 200

@bp_soldadox.route('/cadastrar' , methods=['POST'])
def cadastrar():
    request_json = request.json
    for x in request_json[0]:
        ss = StateSchema()
        # import ipdb; ipdb.set_trace()
        state = ss.load(x)
        current_app.db.session.add(state)
        current_app.db.session.commit()
    for x in request_json[1]:
        dds = DddSchema()
        ddd = dds.load(x)
        current_app.db.session.add(ddd)
        current_app.db.session.commit()
    # Fazer o for para cadastrar as info de regiao...
    return "ok",200