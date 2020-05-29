from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.database import db
from backend.database.models.history import HistoryModel, HistorySchema
from backend.database.models.maintenance import MaintenanceSchema
from flask_restplus import Resource

ns = api.namespace('history', description='Operations related to history entries')
history_schema = HistorySchema()
maintenance_schema = MaintenanceSchema()


@ns.route('/')
class HistoryCollection(Resource):

    @api.response(200, 'Maintenance history list successfully fetched.')
    def get(self):
        """
        Returns a list of all maintenance history entries.
        """

        history_all_entries = HistoryModel.query.all()

        history_entry_list = []
        for history_entry in history_all_entries:
            maintenance_data = maintenance_schema.dump(history_entry.maintenance)
            history_data = history_schema.dump(history_entry)
            history_entry_list.append({**maintenance_data, **history_data})

        response = jsonify(history_entry_list)
        response.status_code = 200

        return response

    @api.response(201, 'Maintenance history successfully added.')
    def post(self):
        """
        Adds a maintenance history entries.
        """

        inserted_data = request.get_json()
        new_history = HistoryModel(
            maintenance_id=inserted_data['maintenance_id'],
            bike_id=inserted_data['bike_id'],
            operating_hours=inserted_data['operating_hours'],
            comment=inserted_data['comment'],
            datetime_created=datetime.utcnow(),
            datetime_last_modified=datetime.utcnow(),
            datetime_display=datetime.utcfromtimestamp(inserted_data['datetime_display']/1000)
        )

        db.session.add(new_history)
        db.session.commit()

        return None, 201


@ns.route('/<string:id_>')
@api.response(404, 'Maintenance history entry not found.')
class HistoryItem(Resource):

    @api.response(200, f"Maintenance history with requested id successfully fetched.")
    def get(self, id_):
        """
        Returns a maintenance history entry.
        """

        history_entry = HistoryModel.query.filter(HistoryModel.history_id == id_).one()

        maintenance_data = maintenance_schema.dump(history_entry.maintenance)
        history_data = history_schema.dump(history_entry)

        response = jsonify({**maintenance_data, **history_data})
        response.status_code = 200

        return response

    @api.response(204, f"History entry with requested id successfully updated.")
    def put(self, id_):
        """
        Updates a maintenance history entry.
        """
        inserted_data = request.get_json()

        history_entry = HistoryModel.query.filter(HistoryModel.history_id == id_).one()
        history_entry.maintenance_id = inserted_data['maintenance_id']
        history_entry.operating_hours = inserted_data['operating_hours']
        history_entry.comment = inserted_data['comment']
        history_entry.datetime_display = datetime.utcfromtimestamp(inserted_data['datetime_display']/1000)
        history_entry.datetime_last_modified = datetime.utcnow()

        db.session.add(history_entry)
        db.session.commit()

        return None, 204

    @api.response(204, f"History entry with requested id successfully deleted.")
    def delete(self, id_):
        """
        Deletes maintenance history entry.
        """
        history_entry = HistoryModel.query.filter(HistoryModel.history_id == id_).one()

        db.session.delete(history_entry)
        db.session.commit()

        return None, 204
