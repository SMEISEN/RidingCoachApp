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
