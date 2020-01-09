from flask import Blueprint

bp_soldadox = Blueprint('soldadox' , __name__ )

@bp_soldadox.route('/show', methods=['GET'])
def mostrar():
    ...