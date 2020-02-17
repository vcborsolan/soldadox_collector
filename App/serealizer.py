from flask_marshmallow import Marshmallow
from .model import State,Ddd,Region

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