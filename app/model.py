from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initials = db.Column(db.String(2))
    name = db.Column(db.String(50))
    ddds = db.relationship('Ddd' , backref='state' , lazy='dynamic')
    url = db.Column(db.String(255))

    # def __repr__(self):
    #     return '<State %r>' % self.ddds

class Ddd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    state_id = db.Column(db.Integer , db.ForeignKey('state.id'))
    url = db.Column(db.String(255))
    regions = db.relationship('Region' , backref='ddd' , lazy='dynamic')

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    url = db.Column(db.String(255))
    ddd_id = db.Column(db.Integer , db.ForeignKey('ddd.id'))
   
class Ad(db.Model):
    __tablename__ = 'ad'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    value = db.Column(db.String(20))
    publication = db.Column(db.String(20))
    description = db.Column(db.String(1000))
    cod = db.Column(db.String(20))
    category = db.Column(db.String(20))
    state = db.Column(db.String(2))
    region = db.Column(db.String(50))
    subregion = db.Column(db.String(50))
    url = db.Column(db.String(150))
    images = db.relationship('Image' , lazy='joined')

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer , db.ForeignKey('ad.id'))
    url = db.Column(db.String(150))
    def __repr__(self):
        return (self.url)