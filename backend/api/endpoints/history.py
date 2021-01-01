from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.history import HistoryModel, HistorySchema
from backend.database.models.maintenance import MaintenanceSchema
from flask_restplus import Resource, fields

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
        fields.DateTime(description="utc time stamp in seconds", required=True, example=datetime.utcnow().timestamp()),
})
history_query_parameters = api.model('HistoryQueryParameters', {
    "bike_id":
        fields.String(description="corresponding bike ID", required=False, example="UUID4"),
    "operating_hours":
        fields.Float(description="operating hours of the bike when the maintenance work was done"
                     , required=False, example=66.1),
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
        fields.DateTime(description="utc time stamp in seconds", required=False, example=datetime.utcnow().timestamp()),
    "datetime_last_modified":
        fields.DateTime(description="utc time stamp in seconds", required=False, example=datetime.utcnow().timestamp()),
    "datetime_display":
        fields.DateTime(description="utc time stamp in seconds", required=False, example=datetime.utcnow().timestamp()),
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
            datetime_display=datetime.utcfromtimestamp(inserted_data.get('datetime_display'))
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
            history_entry.datetime_display = datetime.utcfromtimestamp(inserted_data.get('datetime_display'))
        if bool(inserted_data):
            history_entry.datetime_last_modified = datetime.utcnow()

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
        filter_by_data = {
            'bike_id': requested.get('bike_id'),
            'comment': requested.get('comment'),
        }
        filter_by_data = {key: value for (key, value) in filter_by_data.items() if value}

        history_query = HistoryModel.query.filter_by(**filter_by_data)

        filter_data = {}
        if requested.get('datetime_created', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            filter_data['datetime_created'] = {
                'values': [datetime.utcfromtimestamp(ts) for ts in requested.get('datetime_created')['values']],
                'operators': requested.get('datetime_created')['operators'],
            }
        elif requested.get('datetime_last_modified', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            filter_data['datetime_last_modified'] = {
                'values': [datetime.utcfromtimestamp(ts) for ts in requested.get('datetime_last_modified')['values']],
                'operators': requested.get('datetime_last_modified')['operators'],
            }
        elif requested.get('datetime_display', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            filter_data['datetime_display'] = {
                'values': [datetime.utcfromtimestamp(ts) for ts in requested.get('datetime_display')['values']],
                'operators': requested.get('datetime_display')['operators'],
            }
        elif requested.get('operating_hours', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            filter_data['operating_hours'] = {
                'values': requested.get('operating_hours')['values'],
                'operators': requested.get('datetime_display')['operators'],
            }
        elif requested.get('tags', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            filter_data['tags'] = {
                'values': requested.get('tags')['values'],
                'operators': requested.get('tags')['operators'],
            }

        for attr, item in filter_data.items():
            for operator, value in zip(item['operators'], item['values']):
                if operator == '==':
                    history_query = history_query.filter(getattr(HistoryModel, attr) == value)
                elif operator == '<=':
                    history_query = history_query.filter(getattr(HistoryModel, attr) <= value)
                elif operator == '>=':
                    history_query = history_query.filter(getattr(HistoryModel, attr) >= value)
                elif operator == '<':
                    history_query = history_query.filter(getattr(HistoryModel, attr) < value)
                elif operator == '>':
                    history_query = history_query.filter(getattr(HistoryModel, attr) > value)
                elif operator == '!=':
                    history_query = history_query.filter(getattr(HistoryModel, attr) != value)
                else:
                    raise ValueError('Given operator does not match available operators!')

        history_query = history_query\
            .order_by(HistoryModel.datetime_display.desc())\
            .all()

        history_entry_list = []
        for history_entry in history_query:
            maintenance_data = maintenance_schema.dump(history_entry.maintenance)
            history_data = history_schema.dump(history_entry)
            history_entry_list.append({**maintenance_data, **history_data})

        response = jsonify(history_entry_list)
        response.status_code = 200

        return response
