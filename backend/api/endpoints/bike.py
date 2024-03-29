from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.bike import BikeModel, BikeSchema
from flask_restplus import Resource, fields

ns = api.namespace('bike', description='Operations related to bike entries.')
bike_schema = BikeSchema()

bike_input_parameters = api.model('BikeInputParameters', {
    "operating_hours":
        fields.Float(description="operating hours", required=True, example=66.1),
    "manufacturer":
        fields.String(description="bike manufacturer", required=True, example="bike manufacturer"),
    "model":
        fields.String(description="bike model", required=True, example="bike model"),
    "year":
        fields.Integer(description="bike year", required=True, example=2020),
    "ccm":
        fields.Float(description="engine size", required=False, example=449.7),
    "stroke":
        fields.Float(description="engine stroke", required=False, example=63.0),
    "piston":
        fields.Float(description="engine piston", required=False, example=97.0),
    "slick_front_name":
        fields.String(description="name of front slick tire", required=False, example="front slick name"),
    "slick_front_notes":
        fields.String(description="front slick tire application notes", required=False, example="front slick notes"),
    "slick_front_pressure":
        fields.Raw(description="recommended pressure of front slick tire", required=False, example=[
            {
                "temperature": 40,
                "pressure": 1.7
            },
            {
                "temperature": 25,
                "pressure": 1.8
            },
        ]),
    "slick_rear_name":
        fields.String(description="name of rear slick tire", required=False, example="rear slick name"),
    "slick_rear_notes":
        fields.String(description="rear slick tire application notes", required=False, example="rear slick notes"),
    "slick_rear_pressure":
        fields.Raw(description="recommended pressure of rear slick tire", required=False, example=[
            {
                "temperature": 40,
                "pressure": 1.7
            },
            {
                "temperature": 25,
                "pressure": 1.8
            },
        ]),
    "rain_front_name":
        fields.String(description="name of front rain tire", required=False, example="front rain tire name"),
    "rain_front_notes":
        fields.String(description="front rain tire application notes", required=False, example="front rain tire notes"),
    "rain_front_pressure":
        fields.Raw(description="recommended pressure of front rain tire", required=False, example=[
            {
                "temperature": 40,
                "pressure": 1.7
            },
            {
                "temperature": 25,
                "pressure": 1.8
            },
        ]),
    "rain_rear_name":
        fields.String(description="name of rear rain tire", required=False, example="rear rain tire name"),
    "rain_rear_notes":
        fields.String(description="rear rain tire application notes", required=False, example="rear rain tire notes"),
    "rain_rear_pressure":
        fields.Raw(description="recommended pressure of rear rain tire", required=False, example=[
            {
                "temperature": 40,
                "pressure": 1.7
            },
            {
                "temperature": 25,
                "pressure": 1.8
            },
        ]),
    "setup":
        fields.Raw(description="bike suspension and engine setup", required=False, example=[
            {
                "category": "Engine",
                "group": None,
                "name": "Power Mode",
                "ticks_available": 1,
                "ticks_current": 1,
                "ticks_standard": 1,
            },  {
                "category": "Suspension",
                "group": "Fork",
                "name": "Compression",
                "ticks_available": 37,
                "ticks_current": 14,
                "ticks_standard": 15,
            },
        ]),
})


@ns.route('/')
class BikeCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        """
        Returns a list the bike characteristics.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        bike_all_entries = BikeModel.query \
            .order_by(BikeModel.manufacturer.asc()) \
            .order_by(BikeModel.model.asc()) \
            .order_by(BikeModel.year.asc()) \
            .all()

        bike_list = []
        for bike_entry in bike_all_entries:
            bike_list.append(bike_schema.dump(bike_entry))

        response = jsonify(bike_list)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(bike_input_parameters)
    @api.response(201, 'Bike successfully added.')
    def post(self):
        """
        Adds a bike entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        new_bike = BikeModel(
            operating_hours=inserted_data.get('operating_hours'),
            manufacturer=inserted_data.get('manufacturer'),
            model=inserted_data.get('model'),
            year=inserted_data.get('year'),
            ccm=inserted_data.get('ccm'),
            stroke=inserted_data.get('stroke'),
            piston=inserted_data.get('piston'),
            slick_front_name=inserted_data.get('slick_front_name'),
            slick_front_notes=inserted_data.get('slick_front_notes'),
            slick_front_pressure=inserted_data.get('slick_front_pressure'),
            slick_rear_name=inserted_data.get('slick_rear_name'),
            slick_rear_notes=inserted_data.get('slick_rear_notes'),
            slick_rear_pressure=inserted_data.get('slick_rear_pressure'),
            rain_front_name=inserted_data.get('rain_front_name'),
            rain_front_notes=inserted_data.get('rain_front_notes'),
            rain_front_pressure=inserted_data.get('rain_front_pressure'),
            rain_rear_name=inserted_data.get('rain_rear_name'),
            rain_rear_notes=inserted_data.get('rain_rear_notes'),
            rain_rear_pressure=inserted_data.get('rain_rear_pressure'),
            setup=inserted_data.get('setup'),
        )

        db.session.add(new_bike)
        db.session.commit()

        response = jsonify(new_bike.bike_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Bike not found.')
class BikeItem(Resource):

    @api.doc(security='apikey')
    @api.response(200, "Bike with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a bike.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        bike_entry = BikeModel.query.filter(BikeModel.bike_id == id_).one()

        bike_data = bike_schema.dump(bike_entry)

        response = jsonify(bike_data)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(bike_input_parameters)
    @api.response(204, "Bike with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a bike.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        bike_entry = BikeModel.query.filter(BikeModel.bike_id == id_).one()

        if inserted_data.get('operating_hours', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.operating_hours = inserted_data.get('operating_hours')
        if inserted_data.get('manufacturer', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.manufacturer = inserted_data.get('manufacturer')
        if inserted_data.get('model', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.model = inserted_data.get('model')
        if inserted_data.get('year', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.year = inserted_data.get('year')
        if inserted_data.get('ccm', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.ccm = inserted_data.get('ccm')
        if inserted_data.get('stroke', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.stroke = inserted_data.get('stroke')
        if inserted_data.get('piston', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.piston = inserted_data.get('piston')
        if inserted_data.get('slick_front_name', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.slick_front_name = inserted_data.get('slick_front_name')
        if inserted_data.get('slick_front_notes', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.slick_front_notes = inserted_data.get('slick_front_notes')
        if inserted_data.get('slick_front_pressure', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.slick_front_pressure = inserted_data.get('slick_front_pressure')
        if inserted_data.get('slick_rear_name', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.slick_rear_name = inserted_data.get('slick_rear_name')
        if inserted_data.get('slick_rear_notes', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.slick_rear_notes = inserted_data.get('slick_rear_notes')
        if inserted_data.get('slick_rear_pressure', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.slick_rear_pressure = inserted_data.get('slick_rear_pressure')
        if inserted_data.get('rain_front_name', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.rain_front_name = inserted_data.get('rain_front_name')
        if inserted_data.get('rain_front_notes', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.rain_front_notes = inserted_data.get('rain_front_notes')
        if inserted_data.get('rain_front_pressure', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.rain_front_pressure = inserted_data.get('rain_front_pressure')
        if inserted_data.get('rain_rear_name', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.rain_rear_name = inserted_data.get('rain_rear_name')
        if inserted_data.get('rain_rear_notes', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.rain_rear_notes = inserted_data.get('rain_rear_notes')
        if inserted_data.get('rain_rear_pressure', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.rain_rear_pressure = inserted_data.get('rain_rear_pressure')
        if inserted_data.get('setup', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_entry.setup = inserted_data.get('setup')

        db.session.add(bike_entry)
        db.session.commit()

        return None, 204

    @api.doc(security='apikey')
    @api.response(204, "History entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a bike.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        bike_entry = BikeModel.query.filter(BikeModel.bike_id == id_).one()

        db.session.delete(bike_entry)
        db.session.commit()

        return None, 204
