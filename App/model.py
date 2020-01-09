from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initials = db.Column(db.String(2))
    name = db.Column(db.String(15))
    ddds = db.relationship('Ddd' , backref='state')
    url = db.Column(db.String(255))


class Ddd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    state_id = db.Column(db.Integer , db.ForeignKey('state.id'))
    url = db.Column(db.String(255))
    regions = db.relationship('Region' , backref='ddd')

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))
    ddd_id = db.Column(db.Integer , db.ForeignKey('ddd.id'))


# if (enviou state)
#   if (enviou ddd)
#       if (enviou regiao)
#           retorna full link
#       else:
#           retorna link ddd
#   else:    
#       retorn link state
# else:
#     retorna link br 