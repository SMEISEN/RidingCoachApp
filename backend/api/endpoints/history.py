from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.database import db
from backend.database.models.history import HistoryModel, HistorySchema
from backend.database.models.maintenance import MaintenanceSchema
from flask_restplus import Resource, fields

ns = api.namespace('history', description='Operations related to history entries.')
history_schema = HistorySchema()
maintenance_schema = MaintenanceSchema()

history_input_parameters = api.model('HistoryInputParameters', {
    "maintenance_id":
        fields.String(description="corresponding maintenance ID", required=True),
    "bike_id":
        fields.String(description="corresponding bike ID", required=True),
    "operating_hours":
        fields.Float(description="operating hours", required=True),
    "comment":
        fields.String(description="comment", required=False),
    "tags":
        fields.Raw(description="tags", required=False),
    "datetime_display":
        fields.Float(description="utc time stamp in seconds", required=True, example=datetime.utcnow().timestamp()),
})
history_query_parameters = api.model('HistoryQueryParameters', {
    "bike_id":
        fields.String(description="", required=False),
    "operating_hours":
        fields.Float(description="", required=False),
    "comment":
        fields.String(description="", required=False),
    "tags":
        fields.Raw(description="", required=False),
    "datetime_created":
        fields.DateTime(description="", required=False),
    "datetime_last_modified":
        fields.DateTime(description="", required=False),
    "datetime_display":
        fields.DateTime(description="", required=False)
})


@ns.route('/')
class HistoryCollection(Resource):

    @api.response(200, 'Maintenance history list successfully fetched.')
    def get(self):
        """
        Returns a list of all maintenance history entries.
        """

        history_all_entries = HistoryModel.query.order_by(HistoryModel.datetime_display.desc()).all()

        history_entry_list = []
        for history_entry in history_all_entries:
            maintenance_data = maintenance_schema.dump(history_entry.maintenance)
            history_data = history_schema.dump(history_entry)
            history_entry_list.append({**maintenance_data, **history_data})

        response = jsonify(history_entry_list)
        response.status_code = 200

        return response

    @api.expect(history_input_parameters)
    @api.response(201, 'Maintenance history successfully added.')
    def post(self):
        """
        Adds a maintenance history entry.
        """

        inserted_data = request.get_json()
        new_history = HistoryModel(
            maintenance_id=inserted_data.get('maintenance_id'),
            bike_id=inserted_data.get('bike_id'),
            operating_hours=inserted_data.get('operating_hours'),
            comment=inserted_data.get('comment'),
            tags=inserted_data.get('tags'),
            datetime_created=datetime.utcnow(),
            datetime_last_modified=datetime.utcnow(),
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

    @api.response(200, "Maintenance history with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a maintenance history entry.
        """

        history_entry = HistoryModel.query.filter(HistoryModel.history_id == id_).one()

        maintenance_data = maintenance_schema.dump(history_entry.maintenance)
        history_data = history_schema.dump(history_entry)

        response = jsonify({**maintenance_data, **history_data})
        response.status_code = 200

        return response

    @api.expect(history_input_parameters)
    @api.response(204, "History entry with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a maintenance history entry.
        """

        inserted_data = request.get_json()

        history_entry = HistoryModel.query.filter(HistoryModel.history_id == id_).one()

        if inserted_data.get('maintenance_id') is not None:
            history_entry.maintenance_id = inserted_data.get('maintenance_id')
        if inserted_data.get('operating_hours') is not None:
            history_entry.operating_hours = inserted_data.get('operating_hours')
        if inserted_data.get('comment') is not None:
            history_entry.comment = inserted_data.get('comment')
        if inserted_data.get('tags') is not None:
            history_entry.tags = inserted_data.get('tags')
        if inserted_data.get('datetime_display') is not None:
            history_entry.datetime_display = datetime.utcfromtimestamp(inserted_data.get('datetime_display'))
        if bool(inserted_data) is True:
            history_entry.datetime_last_modified = datetime.utcnow()

        db.session.add(history_entry)
        db.session.commit()

        return None, 204

    @api.response(204, "History entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a maintenance history entry.
        """

        history_entry = HistoryModel.query.filter(HistoryModel.history_id == id_).one()

        db.session.delete(history_entry)
        db.session.commit()

        return None, 204


@ns.route('/query')
@api.response(404, 'Query parameters not found.')
class HistoryQuery(Resource):

    @api.expect(history_query_parameters)
    def post(self):
        """
        Returns a list of all maintenance history entries that match the query.
        """

        requested = request.get_json()
        filter_data = {
            'bike_id': requested.get('bike_id'),
            'operating_hours': requested.get('operating_hours'),
            'comment': requested.get('comment'),
            'tags': requested.get('tags'),
            'datetime_created': requested.get('datetime_created'),
            'datetime_last_modified': requested.get('datetime_last_modified'),
            'datetime_display': requested.get('datetime_display'),
        }
        filter_data = {key: value for (key, value) in filter_data.items() if value}

        history_query = HistoryModel.query.filter_by(**filter_data).all()

        history_entry_list = []
        for history_entry in history_query:
            maintenance_data = maintenance_schema.dump(history_entry.maintenance)
            history_data = history_schema.dump(history_entry)
            history_entry_list.append({**maintenance_data, **history_data})

        response = jsonify(history_entry_list)
        response.status_code = 200

        return response
