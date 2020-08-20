from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.session import SessionModel, SessionSchema
from backend.database.models.laptime import LaptimeModel, LaptimeSchema
from flask_restplus import Resource, fields
from collections import defaultdict

ns = api.namespace('session', description='Operations related to training sessions.')
session_schema = SessionSchema()
laptime_schema = LaptimeSchema()

session_input_parameters = api.model('SessionInputParameters', {
    "training_id":
        fields.String(description="corresponding training ID", required=True),
    "bike_id":
        fields.String(description="corresponding bike ID", required=True),
    "setup_id":
        fields.Float(description="corresponding setup ID", required=True),
    "datetime_display":
        fields.DateTime(description="utc time stamp in seconds", required=True, example=datetime.utcnow().timestamp()),
})


@ns.route('/')
class SessionCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Training session list successfully fetched.')
    def get(self):
        """
        Returns a list of all training session entries.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        session_all_entries = SessionModel.query.order_by(SessionModel.datetime_display.desc()).all()


        session_entry_list = []
        for session_entry in session_all_entries:
            laptime_data = laptime_schema.dump(session_entry.laptimes, many=True)
            session_data = session_schema.dump(session_entry)
            session_data['laptimes'] = []
            if len(laptime_data) > 0:
                for laptime_entry in laptime_data:
                    session_data['laptimes'].append(laptime_entry)
            session_entry_list.append(session_data)

        response = jsonify(session_entry_list)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(session_input_parameters)
    @api.response(201, 'Training session successfully added.')
    def post(self):
        """
        Adds a training session entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()
        new_session = SessionModel(
            training_id=inserted_data.get('training_id'),
            bike_id=inserted_data.get('bike_id'),
            setup_id=inserted_data.get('setup_id'),
            application=inserted_data.get('application'),
            datetime_display=datetime.utcfromtimestamp(inserted_data.get('datetime_display'))
        )

        db.session.add(new_session)
        db.session.commit()

        response = jsonify(new_session.session_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Session entry not found.')
class SessionItem(Resource):

    @api.doc(security='apikey')
    @api.response(200, "Training session with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a training session entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        session_entry = SessionModel.query.filter(SessionModel.session_id == id_).one()

        session_data = session_schema.dump(session_entry)

        response = jsonify(session_data)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(session_input_parameters)
    @api.response(204, "Training session entry with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a training session entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        session_entry = SessionModel.query.filter(SessionModel.session_id == id_).one()

        if inserted_data.get('training_id') is not None:
            session_entry.training_id = inserted_data.get('training_id')
        if inserted_data.get('bike_id') is not None:
            session_entry.bike_id = inserted_data.get('bike_id')
        if inserted_data.get('setup_id') is not None:
            session_entry.setup_id = inserted_data.get('setup_id')
        if inserted_data.get('application') is not None:
            session_entry.application = inserted_data.get('application')
        if inserted_data.get('datetime_display') is not None:
            session_entry.datetime_display = datetime.utcfromtimestamp(inserted_data.get('datetime_display'))
        if bool(inserted_data) is True:
            session_entry.datetime_last_modified = datetime.utcnow()

        db.session.add(session_entry)
        db.session.commit()

        return None, 204

    @api.doc(security='apikey')
    @api.response(204, "Session entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a training session entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        session_entry = SessionModel.query.filter(SessionModel.session_id == id_).one()

        db.session.delete(session_entry)
        db.session.commit()

        return None, 204
