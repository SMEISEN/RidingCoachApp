from flask import jsonify, request
from backend.database.models.bike import BikeModel, BikeSchema
from flask_restplus import Resource, fields
from backend.api import api
from backend.database import db

ns = api.namespace('bike', description='Operations related to blog posts')

post_bike_parameters = api.model('Resource', {
    "operating_hours":
        fields.Float(description="operating hours", required=True),
    "manufacturer":
        fields.String(description="bike manufacturer", required=True),
    "model":
        fields.String(description="bike model", required=True),
    "ccm":
        fields.Float(description="engine size", required=False, example={}),
    "stroke":
        fields.Float(description="engine stroke", required=False, default=None),
    "piston":
        fields.Float(description="engine piston", required=False, default=None),
    "year":
        fields.Integer(description="bike year", required=True),
    "setup":
        fields.Raw(description="bike suspension and engine setup", required=False, default=None),
})


@ns.route('/')
class BikeResource(Resource):

    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        """
        Returns a list the bike characteristics.
        """
        bike_schema = BikeSchema()
        bike_all_entries = BikeModel.query.all()

        bike_list = []
        for bike_entry in bike_all_entries:
            bike_list.append(bike_schema.dump(bike_entry))

        response = jsonify(bike_list)
        response.status_code = 200

        return response

    @api.expect(post_bike_parameters)
    @api.response(201, 'Bike successfully added.')
    def post(self):
        """
        Adds a bike entry.
        """

        inserted_data = request.get_json()
        print(inserted_data)
        new_bike = BikeModel(
            operating_hours=inserted_data['operating_hours'],
            manufacturer=inserted_data['manufacturer'],
            model=inserted_data['model'],
            ccm=inserted_data['ccm'],
            stroke=inserted_data['stroke'],
            piston=inserted_data['piston'],
            year=inserted_data['year'],
            setup=inserted_data['setup'],
        )

        db.session.add(new_bike)
        db.session.commit()

        return None, 201
