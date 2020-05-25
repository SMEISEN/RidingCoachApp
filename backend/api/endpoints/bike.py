from flask import jsonify
from backend.database.models.bike import BikeModel, BikeSchema
from flask_restplus import Resource
from backend.api import api

ns = api.namespace('bike', description='Operations related to blog posts')


@ns.route('/')
class BikeResource(Resource):

    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        """
        Returns a list the bike characteristics.
        """
        bike_schema = BikeSchema()
        bike_data = BikeModel.query.first()
        bike_data = bike_schema.dump(bike_data)

        response = jsonify(bike_data)
        response.status_code = 200

        return response

    def post(self):
        pass
