from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.database import db
from backend.database.models.history import HistoryModel, HistorySchema
from flask_restplus import Resource

ns = api.namespace('maintenance/history', description='Operations related to blog posts')


@ns.route('/')
class HistoryCollection(Resource):

    @api.response(200, 'Maintenance history list successfully fetched.')
    def get(self):
        """
        Returns a list of all maintenance history posts.
        """
        history_schema = HistorySchema()
        history = HistoryModel.query.all()

        history_list = []
        for item in history:
            history_list.append(history_schema.dump(item))

        response = jsonify(history_list)
        response.status_code = 200

        return response

    @api.response(201, 'Maintenance history successfully added.')
    def post(self):
        """
        Adds a maintenance history posts.
        """
        last_history = HistoryModel.query.order_by(HistoryModel.hist_id.desc()).first()
        if last_history is None:
            last_id = -1
        else:
            last_id = last_history.hist_id

        inserted_data = request.get_json()
        new_history = HistoryModel(
            hist_id=last_id+1,
            category=inserted_data['category'],
            name=inserted_data['name'],
            hours=inserted_data['hours'],
            comment=inserted_data['comment'],
            date=datetime.utcnow(),
        )

        db.session.add(new_history)
        db.session.commit()

        return None, 201


@ns.route('/<int:id_>')
@api.response(404, 'Maintenance history post not found.')
class HistoryItem(Resource):

    @api.response(200, 'Maintenance history with id <int:id> successfully fetched.')
    def get(self, id_):
        """
        Returns a maintenance history post.
        """
        history_schema = HistorySchema()
        history_post = HistoryModel.query.filter(HistoryModel.hist_id == id_).one()

        response = jsonify(history_schema.dump(history_post))
        response.status_code = 200

        return response

    @api.response(204, 'Post successfully updated.')
    def put(self, id_):
        """
        Updates a maintenance history post.
        """
        inserted_data = request.get_json()

        maintenance_history = HistoryModel.query.filter(HistoryModel.hist_id == id_).one()
        maintenance_history.category = inserted_data['category']
        maintenance_history.name = inserted_data['name']
        maintenance_history.hours = inserted_data['hours']
        maintenance_history.comment = inserted_data['comment']
        maintenance_history.date = datetime.utcnow()

        db.session.add(maintenance_history)
        db.session.commit()

        return None, 204

    @api.response(204, 'Post successfully deleted.')
    def delete(self, id_):
        """
        Deletes maintenance history post.
        """
        maintenance_history = HistoryModel.query.filter(HistoryModel.hist_id == id_).one()

        db.session.delete(maintenance_history)
        db.session.commit()

        return None, 204
