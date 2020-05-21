from backend.database.models.bike import BikeModel
from flask_restplus import Resource
from backend.api import api

ns = api.namespace('bike', description='Operations related to blog posts')


@ns.route('/')
class BikeResource(Resource):

    def get(self):
        bike = BikeModel.query.all()
        pass

    def post(self):
        pass
