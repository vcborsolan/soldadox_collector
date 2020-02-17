from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initials = db.Column(db.String(2))
    name = db.Column(db.String(20))
    ddds = db.relationship('Ddd' , backref='state' , lazy='dynamic')
    url = db.Column(db.String(255))

    # def __repr__(self):
    #     return '<State %r>' % self.ddds

class Ddd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    state_id = db.Column(db.Integer , db.ForeignKey('state.id'))
    url = db.Column(db.String(255))
    regions = db.relationship('Region' , backref='ddd' , lazy='dynamic')

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))
    ddd_id = db.Column(db.Integer , db.ForeignKey('ddd.id'))