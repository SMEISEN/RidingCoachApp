from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.setup import SetupModel, SetupSchema
from flask_restplus import Resource, fields

ns = api.namespace('setup', description='Operations related to bike setup entries.')
setup_schema = SetupSchema()

setup_input_parameters = api.model('SetupInputParameters', {
    "training_id":
        fields.String(description="corresponding training ID", required=True, example="UUID4"),
    "bike_id":
        fields.String(description="corresponding bike ID", required=True, example="UUID4"),
    "operating_hours":
        fields.Float(description="operating hours", required=True, example=66.1),
    "weather_current":
        fields.Raw(description="current track weather data", required=False, example={
            "lat": 49.2966279,
            "lon": 8.601037,
            "temp": {
                "value": 30.04,
                "units": "C"
            },
            "type": "measurement"
        }),
    "slick_pressure_front":
        fields.Float(description="pressure of front slick tire", required=False, example=2.0),
    "slick_pressure_rear":
        fields.Float(description="pressure of rear slick tire", required=False, example=2.0),
    "rain_pressure_front":
        fields.Float(description="pressure of front rain tire", required=False, example=2.0),
    "rain_pressure_rear":
        fields.Float(description="pressure of front rear tire", required=False, example=2.0),
    "setup":
        fields.Raw(description="bike suspension and engine setup", required=False, example=[
            {
                "category": "Engine",
                "group": None,
                "name": "Power Mode",
                "ticks_available": 1,
                "ticks_current": 1,
                "ticks_standard": 1
            },
            {
                "category": "Suspension",
                "group": "Fork",
                "name": "Compression",
                "ticks_available": 37,
                "ticks_current": 14,
                "ticks_standard": 15
            },
        ]),
    "comment":
        fields.String(description="comment", required=False, example="comment"),
    "datetime_display":
        fields.DateTime(description="utc time stamp in seconds", required=True, example=datetime.utcnow().timestamp()),
})


@ns.route('/')
class SetupCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Setup list successfully fetched.')
    def get(self):
        """
        Returns a list of all setup entries.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        setup_all_entries = SetupModel.query.order_by(SetupModel.datetime_display.desc()).all()

        setup_entry_list = []
        for setup_entry in setup_all_entries:
            setup_data = setup_schema.dump(setup_entry)
            setup_entry_list.append(setup_data)

        response = jsonify(setup_entry_list)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(setup_input_parameters)
    @api.response(201, 'Training history successfully added.')
    def post(self):
        """
        Adds a training history entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()
        new_setup = SetupModel(
            training_id=inserted_data.get('training_id'),
            bike_id=inserted_data.get('bike_id'),
            operating_hours=inserted_data.get('operating_hours'),
            weather_current=inserted_data.get('weather_current'),
            slick_pressure_front=inserted_data.get('slick_pressure_front'),
            slick_pressure_rear=inserted_data.get('slick_pressure_rear'),
            rain_pressure_front=inserted_data.get('rain_pressure_front'),
            rain_pressure_rear=inserted_data.get('rain_pressure_rear'),
            setup=inserted_data.get('setup'),
            comment=inserted_data.get('comment'),
            datetime_display=datetime.utcfromtimestamp(inserted_data.get('datetime_display'))
        )

        db.session.add(new_setup)
        db.session.commit()

        response = jsonify(new_setup.setup_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Setup entry not found.')
class SetupItem(Resource):

    @api.doc(security='apikey')
    @api.response(200, "Setup with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a setup entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        setup_entry = SetupModel.query.filter(SetupModel.setup_id == id_).one()

        setup_data = setup_schema.dump(setup_entry)

        response = jsonify(setup_data)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(setup_input_parameters)
    @api.response(204, "Training entry with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a training history entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        setup_entry = SetupModel.query.filter(SetupModel.setup_id == id_).one()

        if inserted_data.get('training_id', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.training_id = inserted_data.get('training_id')
        if inserted_data.get('bike_id', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.bike_id = inserted_data.get('bike_id')
        if inserted_data.get('operating_hours', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.operating_hours = inserted_data.get('operating_hours')
        if inserted_data.get('weather_current', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.weather_current = inserted_data.get('weather_current')
        if inserted_data.get('slick_pressure_front', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.slick_pressure_front = inserted_data.get('slick_pressure_front')
        if inserted_data.get('slick_pressure_rear', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.slick_pressure_rear = inserted_data.get('slick_pressure_rear')
        if inserted_data.get('rain_pressure_front', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.rain_pressure_front = inserted_data.get('rain_pressure_front')
        if inserted_data.get('rain_pressure_rear', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.rain_pressure_rear = inserted_data.get('rain_pressure_rear')
        if inserted_data.get('setup', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.setup = inserted_data.get('setup')
        if inserted_data.get('comment', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.comment = inserted_data.get('comment')
        if inserted_data.get('datetime_display', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            setup_entry.datetime_display = datetime.utcfromtimestamp(inserted_data.get('datetime_display'))
        if bool(inserted_data) is True:
            setup_entry.datetime_last_modified = datetime.utcnow()

        db.session.add(setup_entry)
        db.session.commit()

        return None, 204

    @api.doc(security='apikey')
    @api.response(204, "Setup entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a training history entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        setup_entry = SetupModel.query.filter(SetupModel.setup_id == id_).one()

        db.session.delete(setup_entry)
        db.session.commit()

        return None, 204
