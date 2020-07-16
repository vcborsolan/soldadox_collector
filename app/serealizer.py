from flask_marshmallow import Marshmallow
from .model import State,Ddd,Region,Ad,Image

ma = Marshmallow()

def configure(app):
    ma.init_app(app)

class StateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = State


class DddSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ddd


class RegionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Region


class AdSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ad


class ImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Image