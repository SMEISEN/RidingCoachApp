from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.laptime import LaptimeModel, LaptimeSchema
from flask_restplus import Resource, fields
from collections import defaultdict

ns = api.namespace('laptime', description='Operations related to lap time entries.')
laptime_schema = LaptimeSchema()

laptime_input_parameters = api.model('LaptimeInputParameters', {
    "session_id":
        fields.String(description="corresponding session ID", required=True),
    "lap_no":
        fields.Integer(description="Lap number of session", required=True),
    "valid":
        fields.Boolean(description="Validity of lap", required=False),
    "laptime_seconds":
        fields.Float(description="Lap time in seconds", required=False),
    "sectors":
        fields.Raw(description="Sector times", required=False),
    "datetime_display":
        fields.DateTime(description="", required=False)
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
            laptime_seconds=inserted_data.get('laptime_seconds'),
            sectors=inserted_data.get('sectors'),
            datetime_display=datetime.utcfromtimestamp(inserted_data.get('datetime_display')),
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

        if inserted_data.get('session_id') is not None:
            laptime_entry.session_id = inserted_data.get('session_id')
        if inserted_data.get('lap_no') is not None:
            laptime_entry.lap_no = inserted_data.get('lap_no')
        if inserted_data.get('valid') is not None:
            laptime_entry.valid = inserted_data.get('valid')
        if inserted_data.get('laptime_seconds') is not None:
            laptime_entry.laptime_seconds = inserted_data.get('laptime_seconds')
        if inserted_data.get('sectors') is not None:
            laptime_entry.sectors = inserted_data.get('sectors')
        if inserted_data.get('datetime_display') is not None:
            laptime_entry.datetime_display = datetime.utcfromtimestamp(inserted_data.get('datetime_display'))
        if bool(inserted_data) is True:
            laptime_entry.datetime_last_modified = datetime.utcnow()

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
