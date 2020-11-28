from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.sparepartitem import SparepartitemModel, SparepartitemSchema
from backend.database.models.sparepart import SparepartModel, SparepartSchema
from flask_restplus import Resource, fields

ns = api.namespace('sparepartitem', description='Operations related to sparepart items.')
sparepartitem_schema = SparepartitemSchema()
sparepart_schema = SparepartSchema()


@ns.route('/')
class SparepartitemCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Sparepart item list successfully fetched.')
    def get(self):
        """
        Returns a list of all sparepart items.
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
