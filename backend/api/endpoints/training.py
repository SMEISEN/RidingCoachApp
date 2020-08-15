from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.database import db
from backend.database.models.training import TrainingModel, TrainingSchema
from backend.database.models.setup import SetupModel, SetupSchema
from flask_restplus import Resource, fields
from collections import defaultdict

ns = api.namespace('training', description='Operations related to training entries.')
training_schema = TrainingSchema()
setup_schema = SetupSchema()

training_input_parameters = api.model('TrainingInputParameters', {
    "location":
        fields.String(description="location of the training", required=True),
    "weather_hourly":
        fields.Raw(description="hourly track weather data", required=False),
    "datetime_display":
        fields.Float(description="utc time stamp in seconds", required=True, example=datetime.utcnow().timestamp()),
})
training_query_parameters = api.model('TrainingQueryParameters', {
    "location":
        fields.String(description="location to be queried", required=False),
    "bike_id":
        fields.String(description="bike_id to be queried", required=False),
    "operating_hours":
        fields.Float(description="operating hours to be queried", required=False),
    "datetime_created":
        fields.DateTime(description="datetime of creation to be queried", required=False),
    "datetime_last_modified":
        fields.DateTime(description="datetime of last modification to be queried", required=False),
    "datetime_display":
        fields.DateTime(description="displayed datetime to be queried", required=False)
})


@ns.route('/')
class TrainingCollection(Resource):

    @api.response(200, 'Training history list successfully fetched.')
    def get(self):
        """
        Returns a list of all training history entries.
        """

        training_all_entries = TrainingModel.query.order_by(TrainingModel.datetime_display.desc()).all()

        training_entry_list = []
        for training_entry in training_all_entries:
            setup_data = setup_schema.dump(training_entry.setups, many=True)
            training_data = training_schema.dump(training_entry)
            training_data['setups'] = []
            if len(setup_data) > 0:
                for setup_entry in setup_data:
                    training_data['setups'].append(setup_entry)
            training_entry_list.append(training_data)

        response = jsonify(training_entry_list)
        response.status_code = 200

        return response

    @api.expect(training_input_parameters)
    @api.response(201, 'Training history successfully added.')
    def post(self):
        """
        Adds a training history entry.
        """

        inserted_data = request.get_json()
        new_training = TrainingModel(
            location=inserted_data.get('location'),
            weather_hourly=inserted_data.get('weather_hourly'),
            datetime_created=datetime.utcnow(),
            datetime_last_modified=datetime.utcnow(),
            datetime_display=datetime.utcfromtimestamp(inserted_data.get('datetime_display'))
        )

        db.session.add(new_training)
        db.session.commit()

        response = jsonify(new_training.training_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Training history entry not found.')
class TrainingItem(Resource):

    @api.response(200, "Training history with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a training history entry.
        """

        training_entry = TrainingModel.query.filter(TrainingModel.training_id == id_).one()

        training_data = training_schema.dump(training_entry)
        setup_data = setup_schema.dump(training_entry.setups, many=True)

        training_data['setups'] = []
        if len(setup_data) > 0:
            for setup_entry in setup_data:
                training_data['setups'].append(setup_entry)

        response = jsonify(training_data)
        response.status_code = 200

        return response

    @api.expect(training_input_parameters)
    @api.response(204, "Training entry with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a training history entry.
        """

        inserted_data = request.get_json()

        training_entry = TrainingModel.query.filter(TrainingModel.training_id == id_).one()

        if inserted_data.get('location') is not None:
            training_entry.location = inserted_data.get('location')
        if inserted_data.get('weather_hourly') is not None:
            training_entry.weather_hourly = inserted_data.get('weather_hourly')
        if inserted_data.get('datetime_display') is not None:
            training_entry.datetime_display = datetime.utcfromtimestamp(inserted_data.get('datetime_display'))
        if bool(inserted_data) is True:
            training_entry.datetime_last_modified = datetime.utcnow()

        db.session.add(training_entry)
        db.session.commit()

        return None, 204

    @api.response(204, "History entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a training history entry.
        """

        training_entry = TrainingModel.query.filter(TrainingModel.training_id == id_).one()

        db.session.delete(training_entry)
        db.session.commit()

        return None, 204


@ns.route('/query')
@api.response(404, 'Query parameters not found.')
class TrainingQuery(Resource):

    @api.expect(training_query_parameters)
    def post(self):
        """
        Returns a list of all training entries that match the query.
        """

        requested = request.get_json()
        filter_by_data = {
            'location': requested.get('location'),
        }
        filter_by_data = {key: value for (key, value) in filter_by_data.items() if value}

        training_query = TrainingModel.query.filter_by(**filter_by_data)

        filter_data = {}
        if requested.get('datetime_created') is not None:
            filter_data['datetime_created'] = {
                'values': [datetime.utcfromtimestamp(ts) for ts in requested.get('datetime_created')['values']],
                'operators': requested.get('datetime_created')['operators'],
            }
        elif requested.get('datetime_last_modified') is not None:
            filter_data['datetime_last_modified'] = {
                'values': [datetime.utcfromtimestamp(ts) for ts in requested.get('datetime_last_modified')['values']],
                'operators': requested.get('datetime_last_modified')['operators'],
            }
        elif requested.get('datetime_display') is not None:
            filter_data['datetime_display'] = {
                'values': [datetime.utcfromtimestamp(ts) for ts in requested.get('datetime_display')['values']],
                'operators': requested.get('datetime_display')['operators'],
            }

        for attr, item in filter_data.items():
            for operator, value in zip(item['operators'], item['values']):
                if operator == '==':
                    training_query = training_query.filter(getattr(TrainingModel, attr) == value)
                elif operator == '<=':
                    training_query = training_query.filter(getattr(TrainingModel, attr) <= value)
                elif operator == '>=':
                    training_query = training_query.filter(getattr(TrainingModel, attr) >= value)
                elif operator == '<':
                    training_query = training_query.filter(getattr(TrainingModel, attr) < value)
                elif operator == '>':
                    training_query = training_query.filter(getattr(TrainingModel, attr) > value)
                elif operator == '!=':
                    training_query = training_query.filter(getattr(TrainingModel, attr) != value)
                else:
                    raise ValueError('Given operator does not match available operators!')

        training_query = training_query\
            .order_by(TrainingModel.datetime_display.desc())\
            .all()

        training_entry_list = []
        for training_entry in training_query:
            setup_data = setup_schema.dump(training_entry.setups, many=True)
            training_data = training_schema.dump(training_entry)
            training_data['setups'] = []
            if len(setup_data) > 0:
                for setup_entry in setup_data:
                    training_data['setups'].append(setup_entry)
            training_entry_list.append(training_data)

        response = jsonify(training_entry_list)
        response.status_code = 200

        return response
