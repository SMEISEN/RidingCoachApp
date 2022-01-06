from datetime import datetime, timezone
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.laptime import LaptimeModel, LaptimeSchema
from flask_restplus import Resource, fields

ns = api.namespace('laptime', description='Operations related to lap time entries.')
laptime_schema = LaptimeSchema()

laptime_input_parameters = api.model('LaptimeInputParameters', {
    "session_id":
        fields.String(description="corresponding session ID", required=True, example="UUID4"),
    "lap_no":
        fields.Integer(description="lap number of session", required=True, example=1),
    "valid":
        fields.Boolean(description="validity of lap", required=False, example=True),
    "laptime_seconds":
        fields.Float(description="lap time in seconds", required=False, example=66.61),
    "sectors":
        fields.Raw(description="sector times", required=False, example={
            "Sector 1": 39.9,
            "Sector 2": 36.57
        }),
    "datetime_display":
        fields.DateTime(description="utc time stamp in seconds", required=False,
                        example=datetime.now(timezone.utc).timestamp())
})


@ns.route('/')
class LaptimeCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Lap time list successfully fetched.')
    def get(self):
        """
        Returns a list of all lap time entries.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        laptime_all_entries = LaptimeModel.query.order_by(LaptimeModel.datetime_display.desc()).all()

        laptime_entry_list = []
        for laptime_entry in laptime_all_entries:
            laptime_data = laptime_schema.dump(laptime_entry)
            laptime_entry_list.append(laptime_data)

        response = jsonify(laptime_entry_list)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(laptime_input_parameters)
    @api.response(201, 'Lap time successfully added.')
    def post(self):
        """
        Adds a lap time entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()
        new_laptime = LaptimeModel(
            session_id=inserted_data.get('session_id'),
            lap_no=inserted_data.get('lap_no'),
            valid=inserted_data.get('valid'),
            track_layout=inserted_data.get('track_layout'),
            laptime_seconds=inserted_data.get('laptime_seconds'),
            sectors=inserted_data.get('sectors'),
            datetime_display=datetime.fromtimestamp(inserted_data.get('datetime_display'), tz=timezone.utc),
        )

        db.session.add(new_laptime)
        db.session.commit()

        response = jsonify(new_laptime.lap_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Lap time entry not found.')
class LaptimeItem(Resource):

    @api.doc(security='apikey')
    @api.response(200, "Lap time with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a lap time entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        laptime_entry = LaptimeModel.query.filter(LaptimeModel.lap_id == id_).one()

        laptime_data = laptime_schema.dump(laptime_entry)

        response = jsonify(laptime_data)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(laptime_input_parameters)
    @api.response(204, "Lap time entry with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a lap time entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        laptime_entry = LaptimeModel.query.filter(LaptimeModel.lap_id == id_).one()

        if inserted_data.get('session_id', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            laptime_entry.session_id = inserted_data.get('session_id')
        if inserted_data.get('lap_no', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            laptime_entry.lap_no = inserted_data.get('lap_no')
        if inserted_data.get('valid', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            laptime_entry.valid = inserted_data.get('valid')
        if inserted_data.get('track_layout', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            laptime_entry.track_layout = inserted_data.get('track_layout')
        if inserted_data.get('laptime_seconds', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            laptime_entry.laptime_seconds = inserted_data.get('laptime_seconds')
        if inserted_data.get('sectors', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            laptime_entry.sectors = inserted_data.get('sectors')
        if inserted_data.get('datetime_display', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            laptime_entry.datetime_display = datetime\
                .fromtimestamp(inserted_data.get('datetime_display'), tz=timezone.utc)

        db.session.add(laptime_entry)
        db.session.commit()

        return None, 204

    @api.doc(security='apikey')
    @api.response(204, "Lap time entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a lap time entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        laptime_entry = LaptimeModel.query.filter(LaptimeModel.lap_id == id_).one()

        db.session.delete(laptime_entry)
        db.session.commit()

        return None, 204
