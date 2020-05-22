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
        history_all_posts = HistoryModel.query.all()

        history_post_list = []
        for history_post in history_all_posts:
            history_post_list.append(history_schema.dump(history_post))

        response = jsonify(history_post_list)
        response.status_code = 200

        return response

    @api.response(201, 'Maintenance history successfully added.')
    def post(self):
        """
        Adds a maintenance history posts.
        """
        last_history_post = HistoryModel.query.order_by(HistoryModel.hist_id.desc()).first()
        if last_history_post is None:
            last_id = -1
        else:
            last_id = last_history_post.hist_id

        inserted_data = request.get_json()
        new_history = HistoryModel(
            hist_id=last_id+1,
            category=inserted_data['category'],
            name=inserted_data['name'],
            hours=inserted_data['hours'],
            comment=inserted_data['comment'],
            datetime_created=datetime.utcnow(),
            datetime_last_modified=datetime.utcnow(),
            datetime_display=datetime.utcfromtimestamp(inserted_data['datetime_display']/1000)
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

        history_post = HistoryModel.query.filter(HistoryModel.hist_id == id_).one()
        history_post.category = inserted_data['category']
        history_post.name = inserted_data['name']
        history_post.hours = inserted_data['hours']
        history_post.comment = inserted_data['comment']
        history_post.datetime_display = datetime.utcfromtimestamp(inserted_data['datetime_display']/1000)
        history_post.datetime_last_modified = datetime.utcnow()

        db.session.add(history_post)
        db.session.commit()

        return None, 204

    @api.response(204, 'Post successfully deleted.')
    def delete(self, id_):
        """
        Deletes maintenance history post.
        """
        history_post = HistoryModel.query.filter(HistoryModel.hist_id == id_).one()

        db.session.delete(history_post)
        db.session.commit()

        return None, 204
