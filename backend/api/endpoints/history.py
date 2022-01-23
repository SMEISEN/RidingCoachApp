from datetime import datetime, timezone
from flask import jsonify, request
from flask_restplus import Resource, fields
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.api.routines.common import query_intervals
from backend.database import db
from backend.database.models.history import HistoryModel, HistorySchema
from backend.database.models.maintenance import MaintenanceSchema
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import ARRAY

ns = api.namespace('history', description='Operations related to history entries.')
history_schema = HistorySchema()
maintenance_schema = MaintenanceSchema()

history_input_parameters = api.model('HistoryInputParameters', {
    "maintenance_id":
        fields.String(description="corresponding maintenance ID", required=True, example="UUID4"),
    "bike_id":
        fields.String(description="corresponding bike ID", required=True, example="UUID4"),
    "operating_hours":
        fields.Float(description="operating hours of the bike when the maintenance work was done",
                     required=True, example=66.1),
    "comment":
        fields.String(description="comment on the maintenance entry",
                      required=False, example="comment on the maintenance entry"),
    "tags":
        fields.Raw(description="tags", required=False, example=[
            "checked",
            "fixed",
            "replaced",
        ]),
    "datetime_display":
        fields.DateTime(description="utc time stamp in seconds", required=True,
                        example=datetime.now(timezone.utc).timestamp()),
})
history_query_parameters = api.model('HistoryQueryParameters', {
    "bike_id":
        fields.String(description="corresponding bike ID", required=False, example="UUID4"),
    "operating_hours":
        fields.Raw(description="operating hours of the bike when the maintenance work was done",
                     required=False, example=
                     {
                         "values": [66.0, 99.6],
                         "operators": ['>=', '<='],
                     }),
    "comment":
        fields.String(description="comment on the maintenance entry",
                      required=False, example="comment on the maintenance entry"),
    "tags":
        fields.Raw(description="tags", required=False, example=[
            "checked",
            "fixed",
            "replaced",
        ]),
    "datetime_created":
        fields.Raw(description="utc time stamp in seconds", required=False, example={
            "values": [
                datetime.now(timezone.utc).timestamp() - 2000,
                datetime.now(timezone.utc).timestamp()
            ],
            "operators": ['>=', '<='],
        }),
    "datetime_last_modified":
        fields.Raw(description="utc time stamp in seconds", required=False, example={
            "values": [
                datetime.now(timezone.utc).timestamp() - 2000,
                datetime.now(timezone.utc).timestamp()
            ],
            "operators": ['>=', '<='],
        }),
    "datetime_display":
        fields.Raw(description="utc time stamp in seconds", required=False, example={
            "values": [
                datetime.now(timezone.utc).timestamp() - 2000,
                datetime.now(timezone.utc).timestamp()
            ],
            "operators": ['>=', '<='],
        }),
})


@ns.route('/')
class HistoryCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Maintenance history list successfully fetched.')
    def get(self):
        """
        Returns a list of all maintenance history entries.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        history_all_entries = HistoryModel.query.order_by(HistoryModel.datetime_display.desc()).all()

        history_entry_list = []
        for history_entry in history_all_entries:
            maintenance_data = maintenance_schema.dump(history_entry.maintenance)
            history_data = history_schema.dump(history_entry)
            history_entry_list.append({**maintenance_data, **history_data})

        response = jsonify(history_entry_list)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(history_input_parameters)
    @api.response(201, 'Maintenance history successfully added.')
    def post(self):
        """
        Adds a maintenance history entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()
        new_history = HistoryModel(
            maintenance_id=inserted_data.get('maintenance_id'),
            bike_id=inserted_data.get('bike_id'),
            operating_hours=inserted_data.get('operating_hours'),
            comment=inserted_data.get('comment'),
            tags=inserted_data.get('tags'),
            datetime_display=datetime.fromtimestamp(
                inserted_data.get('datetime_display'), tz=timezone.utc).replace(tzinfo=None),
        )

        db.session.add(new_history)
        db.session.commit()

        response = jsonify(new_history.history_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Maintenance history entry not found.')
class HistoryItem(Resource):

    @api.doc(security='apikey')
    @api.response(200, "Maintenance history with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a maintenance history entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        history_entry = HistoryModel.query.filter(HistoryModel.history_id == id_).one()

        maintenance_data = maintenance_schema.dump(history_entry.maintenance)
        history_data = history_schema.dump(history_entry)

        response = jsonify({**maintenance_data, **history_data})
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(history_input_parameters)
    @api.response(204, "History entry with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a maintenance history entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        history_entry = HistoryModel.query.filter(HistoryModel.history_id == id_).one()

        if inserted_data.get('maintenance_id', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            history_entry.maintenance_id = inserted_data.get('maintenance_id')
        if inserted_data.get('operating_hours', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            history_entry.operating_hours = inserted_data.get('operating_hours')
        if inserted_data.get('comment', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            history_entry.comment = inserted_data.get('comment')
        if inserted_data.get('tags', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            history_entry.tags = inserted_data.get('tags')
        if inserted_data.get('datetime_display', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            history_entry.datetime_display = datetime.fromtimestamp(
                inserted_data.get('datetime_display'), tz=timezone.utc).replace(tzinfo=None)

        db.session.add(history_entry)
        db.session.commit()

        return None, 204

    @api.doc(security='apikey')
    @api.response(204, "History entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a maintenance history entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        history_entry = HistoryModel.query.filter(HistoryModel.history_id == id_).one()

        db.session.delete(history_entry)
        db.session.commit()

        return None, 204


@ns.route('/query')
@api.response(404, 'Query parameters not found.')
class HistoryQuery(Resource):

    @api.doc(security='apikey')
    @api.expect(history_query_parameters)
    def post(self):
        """
        Returns a list of all maintenance history entries that match the query.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        requested = request.get_json()
        valid_keys = ["bike_id", "comment", "datetime_created", "datetime_last_modified", "datetime_display",
                      "operating_hours", "tags"]
        if not all(x in valid_keys for x in requested.keys()):
            response = jsonify([])
            response.status_code = 404

            return response

        filter_by_data = {
            'bike_id': requested.get('bike_id'),
            'comment': requested.get('comment'),
        }
        filter_by_data = {key: value for (key, value) in filter_by_data.items() if value is not None}

        history_query = HistoryModel.query.filter_by(**filter_by_data)

        history_query = query_intervals(filter_keys=[
            "datetime_created",
            "datetime_last_modified",
            "datetime_display",
            "operating_hours",
        ], query=history_query, request=requested, model=HistoryModel)

        if requested.get('tags', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            history_query = history_query \
                .filter(HistoryModel.tags.contains(cast(requested.get('tags'), ARRAY(db.String))))

        history_query = history_query \
            .order_by(HistoryModel.datetime_display.desc()) \
            .all()

        history_entry_list = []
        for history_entry in history_query:
            maintenance_data = maintenance_schema.dump(history_entry.maintenance)
            history_data = history_schema.dump(history_entry)
            history_entry_list.append({**maintenance_data, **history_data})

        response = jsonify(history_entry_list)
        response.status_code = 200

        return response
