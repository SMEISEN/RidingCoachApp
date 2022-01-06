from datetime import datetime, timezone
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.coach import CoachModel, CoachSchema
from flask_restplus import Resource, fields

ns = api.namespace('coach', description='Operations related to bike entries.')
coach_schema = CoachSchema()

coach_input_parameters = api.model('CoachInputParameters', {
    "category":
        fields.String(description="bike suspension end", required=True, example="category name"),
    "symptom":
        fields.Raw(description="suspension symptom", required=True, example={
            "id": "example ID",
            "name": "example name",
        }),
    "notes":
        fields.String(description="notes", required=False, example="notes on the symptom"),
    "questions":
        fields.Raw(description="array of questions in terms of troubleshouting", required=False, example=[
            "example question 1",
            "example question 2",
        ]),
    "advice":
        fields.Raw(description="object of possible problems and solutions", required=True, example={
            "A": {
                "problem": "problem A description",
                "solution": [
                    "solution approach 1 of the problem",
                    "solution approach 2 of the problem",
                ],
            },
            "B": {
                "problem": "problem B description",
                "solution": [
                    "solution approach 1 of the problem",
                    "solution approach 2 of the problem",
                ],
            },
        }),
})


@ns.route('/')
class CoachCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        """
        Returns a list the coach advices.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        coach_all_entries = CoachModel.query.all()

        coach_list = []
        for coach_entry in coach_all_entries:
            coach_list.append(coach_schema.dump(coach_entry))

        response = jsonify(coach_list)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(coach_input_parameters)
    @api.response(201, 'Coach advice successfully added.')
    def post(self):
        """
        Adds a coach advice.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        new_coach = CoachModel(
            category=inserted_data.get('category'),
            symptom=inserted_data.get('symptom'),
            notes=inserted_data.get('notes'),
            questions=inserted_data.get('questions'),
            advice=inserted_data.get('advice'),
        )

        db.session.add(new_coach)
        db.session.commit()

        response = jsonify(new_coach.coach_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Coach advice not found.')
class CoachItem(Resource):

    @api.doc(security='apikey')
    @api.response(200, "Coach advice with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a coach advice.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        coach_entry = CoachModel.query.filter(CoachModel.coach_id == id_).one()

        coach_data = coach_schema.dump(coach_entry)

        response = jsonify(coach_data)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(coach_input_parameters)
    @api.response(204, "Coach advice with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a coach advice.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        coach_entry = CoachModel.query.filter(CoachModel.coach_id == id_).one()

        if inserted_data.get('category', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            coach_entry.category = inserted_data.get('category')
        if inserted_data.get('symptom', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            coach_entry.symptom = inserted_data.get('symptom')
        if inserted_data.get('notes', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            coach_entry.notes = inserted_data.get('notes')
        if inserted_data.get('questions', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            coach_entry.questions = inserted_data.get('questions')
        if inserted_data.get('advice', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            coach_entry.advice = inserted_data.get('advice')
        if bool(inserted_data):
            coach_entry.datetime_last_modified = datetime.now(timezone.utc).replace(tzinfo=None)

        db.session.add(coach_entry)
        db.session.commit()

        return None, 204

    @api.doc(security='apikey')
    @api.response(204, "Coach advice entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a coach advice.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        coach_entry = CoachModel.query.filter(CoachModel.coach_id == id_).one()

        db.session.delete(coach_entry)
        db.session.commit()

        return None, 204
