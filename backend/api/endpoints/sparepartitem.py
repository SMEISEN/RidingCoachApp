from datetime import datetime, timezone
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.sparepartitem import SparepartitemModel, SparepartitemSchema
from backend.database.models.sparepart import SparepartSchema
from flask_restplus import Resource, fields

ns = api.namespace('sparepartitem', description='Operations related to spare part items.')
sparepartitem_schema = SparepartitemSchema()
sparepart_schema = SparepartSchema()

sparepartitem_input_parameters = api.model('SparepartitemInputParameters', {
    "sparepart_id":
        fields.String(description="id of the parent spare part item", required=True, example="UUID4"),
    "condition":
        fields.String(description="condition of the spare part item child", required=True, example="good"),
    "description":
        fields.String(description="description of the spare part item child", required=True, example="new"),
})


@ns.route('/')
class SparepartitemCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Sparepart item list successfully fetched.')
    def get(self):
        """
        Returns a list of all spare part item childs.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        sparepartitem_all_entries = SparepartitemModel.query.order_by(SparepartitemModel.datetime_display.desc()).all()

        sparepartitem_entry_list = []
        for sparepartitem_entry in sparepartitem_all_entries:
            sparepartitem_data = sparepartitem_schema.dump(sparepartitem_entry)
            sparepartitem_data['sparepart'] = sparepart_schema.dump(sparepartitem_entry.sparepart)
            sparepartitem_entry_list.append(sparepartitem_data)

        response = jsonify(sparepartitem_entry_list)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(sparepartitem_input_parameters)
    @api.response(201, 'Spare part item successfully added.')
    def post(self):
        """
        Creates a new spare part item child.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        new_sparepartitem = SparepartitemModel(
            sparepart_id=inserted_data.get('sparepart_id'),
            condition=inserted_data.get('condition'),
            description=inserted_data.get('description'),
            stock=inserted_data.get('stock'),
        )
        db.session.add(new_sparepartitem)
        db.session.commit()

        response = jsonify(new_sparepartitem.sparepartitem_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Spare part item not found.')
class SparepartitemItem(Resource):

    @api.doc(security='apikey')
    @api.response(200, f"Spare part item with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a spare part item child.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        sparepart_item = SparepartitemModel.query.filter(SparepartitemModel.sparepartitem_id == id_).one()

        response = jsonify(sparepartitem_schema.dump(sparepart_item))
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(sparepartitem_input_parameters)
    @api.response(204, f"Spare part item with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a spare part item child.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        sparepart_item = SparepartitemModel.query.filter(SparepartitemModel.sparepartitem_id == id_).one()

        if inserted_data.get('condition', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            sparepart_item.condition = inserted_data.get('condition')
        if inserted_data.get('description', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            sparepart_item.description = inserted_data.get('description')
        if inserted_data.get('stock', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            sparepart_item.stock = inserted_data.get('stock')
        if bool(inserted_data):
            sparepart_item.datetime_last_modified = datetime.now(timezone.utc).replace(tzinfo=None)

        db.session.add(sparepart_item)
        db.session.commit()

        return None, 204

    @api.doc(security='apikey')
    @api.response(204, f"Spare part item with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a spare part item child.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        sparepart_item = SparepartitemModel.query.filter(SparepartitemModel.sparepartitem_id == id_).one()

        db.session.delete(sparepart_item)
        db.session.commit()

        return None, 204
