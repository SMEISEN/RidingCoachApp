from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.tire import TireModel, TireSchema
from flask_restplus import Resource, fields

ns = api.namespace('tire', description='Operations related to tire entries.')
tire_schema = TireSchema()

tire_input_parameters = api.model('TireInputParameters', {
    "bike_id":
        fields.String(description="corresponding bike ID", required=True, example="UUID4"),
    "rim":
        fields.String(description="rim on which the tire is mounted", required=False, example="Alpina black"),
    "category":
        fields.String(description="slick or rain tire", required=True, example="slick"),
    "manufacturer":
        fields.String(description="manufacturer of the tire", required=True, example="Metzeler"),
    "name":
        fields.String(description="name of the tire", required=False, example="Metzeler"),
    "compound":
        fields.String(description="compound of the tire", required=False, example="K1"),
    "axis":
        fields.String(description="front or rear", required=True, example="front"),
    "dimension":
        fields.String(description="dimension of the tire", required=False, example="125/75R420"),
    "dot":
        fields.String(description="production week and year of the tire", required=True, example="1521"),
    "condition":
        fields.Raw(description="condition of the tire", required=True, example={
            "left_outer": 1.0,
            "left_middle": 1.0,
            "center": 1.0,
            "right_middle": 1.0,
            "right_outer": 1.0
        }),
    "operating_hours":
        fields.Float(description="operating hours of the tires", required=True, example=0.0),
    "comment":
        fields.String(description="comment on the tire", required=False, example="comment on the tire")
})


@ns.route('/')
class TireCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Tire list successfully fetched.')
    def get(self):
        """
        Returns a list of all tire entries.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        tire_all_entries = TireModel.query.order_by(TireModel.datetime_last_modified.desc()).all()

        tire_entry_list = []
        for tire_entry in tire_all_entries:
            tire_data = tire_schema.dump(tire_entry)
            tire_entry_list.append(tire_data)

        response = jsonify(tire_entry_list)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(tire_input_parameters)
    @api.response(201, 'Tire successfully added.')
    def post(self):
        """
        Adds a tire entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()
        new_tire = TireModel(
            bike_id=inserted_data.get('bike_id'),
            rim=inserted_data.get('rim'),
            category=inserted_data.get('category'),
            manufacturer=inserted_data.get('manufacturer'),
            name=inserted_data.get('name'),
            compound=inserted_data.get('compound'),
            axis=inserted_data.get('axis'),
            dimension=inserted_data.get('dimension'),
            dot=inserted_data.get('dot'),
            condition=inserted_data.get('condition'),
            operating_hours=inserted_data.get('operating_hours'),
            comment=inserted_data.get('comment'),
        )

        db.session.add(new_tire)
        db.session.commit()

        response = jsonify(new_tire.tire_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Tire entry not found.')
class TireItem(Resource):

    @api.doc(security='apikey')
    @api.response(200, "Tire with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a tire entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        tire_entry = TireModel.query.filter(TireModel.tire_id == id_).one()

        tire_data = tire_schema.dump(tire_entry)

        response = jsonify(tire_data)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(tire_input_parameters)
    @api.response(204, "Tire entry with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a tire entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        tire_entry = TireModel.query.filter(TireModel.tire_id == id_).one()

        if inserted_data.get('bike_id', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.bike_id = inserted_data.get('bike_id')
        if inserted_data.get('rim', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.rim = inserted_data.get('rim')
        if inserted_data.get('category', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.category = inserted_data.get('category')
        if inserted_data.get('manufacturer', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.manufacturer = inserted_data.get('manufacturer')
        if inserted_data.get('name', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.name = inserted_data.get('name')
        if inserted_data.get('compound', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.compound = inserted_data.get('compound')
        if inserted_data.get('axis', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.axis = inserted_data.get('axis')
        if inserted_data.get('dimension', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.dimension = inserted_data.get('dimension')
        if inserted_data.get('dot', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.dot = inserted_data.get('dot')
        if inserted_data.get('condition', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.condition = inserted_data.get('condition')
        if inserted_data.get('operating_hours', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.operating_hours = inserted_data.get('operating_hours')
        if inserted_data.get('comment', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            tire_entry.comment = inserted_data.get('comment')
        if bool(inserted_data):
            tire_entry.datetime_last_modified = datetime.utcnow()

        db.session.add(tire_entry)
        db.session.commit()

        return None, 204

    @api.doc(security='apikey')
    @api.response(204, "Tire entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a tire entry.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        tire_entry = TireModel.query.filter(TireModel.tire_id == id_).one()

        db.session.delete(tire_entry)
        db.session.commit()

        return None, 204
