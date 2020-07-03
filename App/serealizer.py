from flask_marshmallow import Marshmallow
from .model import State,Ddd,Region,Ad,Image

ma = Marshmallow()

def configure(app):
    ma.init_app(app)

class StateSchema(ma.ModelSchema):
    class Meta:
        model = State


class DddSchema(ma.ModelSchema):
    class Meta:
        model = Ddd


class RegionSchema(ma.ModelSchema):
    class Meta:
        model = Region


class AdSchema(ma.ModelSchema):
    class Meta:
        model = Ad


class ImageSchema(ma.ModelSchema):
    class Meta:
        model = Image