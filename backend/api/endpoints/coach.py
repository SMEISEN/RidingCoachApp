from datetime import datetime
from flask import jsonify, request
from backend.database.models.coach import CoachModel, CoachSchema
from flask_restplus import Resource, fields
from backend.api import api
from backend.database import db

ns = api.namespace('coach', description='Operations related to bike entries.')
coach_schema = CoachSchema()

coach_input_parameters = api.model('CoachInputParameters', {
    "category":
        fields.String(description="bike suspension end", required=True),
    "symptom":
        fields.Raw(description="suspension symptom", required=True),
    "notes":
        fields.String(description="notes", required=False),
    "questions":
        fields.Raw(description="array of questions in terms of troubleshouting", required=False),
    "advice":
        fields.Raw(description="object of possible problems and solutions", required=True),
})


@ns.route('/')
class CoachCollection(Resource):

    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        """
        Returns a list the coach advices.
        """

        coach_all_entries = CoachModel.query.all()

        coach_list = []
        for coach_entry in coach_all_entries:
            coach_list.append(coach_schema.dump(coach_entry))

        response = jsonify(coach_list)
        response.status_code = 200

        return response

    @api.expect(coach_input_parameters)
    @api.response(201, 'Coach advice successfully added.')
    def post(self):
        """
        Adds a coach advice.
        """

        inserted_data = request.get_json()

        new_coach = CoachModel(
            category=inserted_data.get('category'),
            symptom=inserted_data.get('symptom'),
            notes=inserted_data.get('notes'),
            questions=inserted_data.get('questions'),
            advice=inserted_data.get('advice'),
            datetime_created=datetime.utcnow(),
            datetime_last_modified=datetime.utcnow(),
        )

        db.session.add(new_coach)
        db.session.commit()

        response = jsonify(new_coach.coach_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Coach advice not found.')
class CoachItem(Resource):

    @api.response(200, "Coach advice with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a coach advice.
        """

        coach_entry = CoachModel.query.filter(CoachModel.coach_id == id_).one()

        coach_data = coach_schema.dump(coach_entry)

        response = jsonify(bike_data)
        response.status_code = 200

        return response

    @api.expect(coach_input_parameters)
    @api.response(204, "Coach advice with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a coach advice.
        """

        inserted_data = request.get_json()

        coach_entry = CoachModel.query.filter(CoachModel.coach_id == id_).one()

        if inserted_data.get('category') is not None:
            coach_entry.operating_hours = inserted_data.get('category')
        if inserted_data.get('symptom') is not None:
            coach_entry.manufacturer = inserted_data.get('symptom')
        if inserted_data.get('notes') is not None:
            coach_entry.model = inserted_data.get('notes')
        if inserted_data.get('questions') is not None:
            coach_entry.year = inserted_data.get('questions')
        if inserted_data.get('advice') is not None:
            coach_entry.ccm = inserted_data.get('advice')
        if bool(inserted_data) is True:
            coach_entry.datetime_last_modified = datetime.utcnow()

        db.session.add(coach_entry)
        db.session.commit()

        return None, 204

    @api.response(204, "Coach advice entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a coach advice.
        """

        coach_entry = CoachModel.query.filter(CoachModel.coach_id == id_).one()

        db.session.delete(coach_entry)
        db.session.commit()

        return None, 204
