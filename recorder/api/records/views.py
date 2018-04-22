"""
View module for working with categories
add, delete, get
"""
import os
from flask import Blueprint, request, jsonify, json

from recorder.api.records.models import RecordsSet
from recorder.database import db
from recorder.error_helper import InvalidUsage
from recorder.helper_utils import is_ascii

blueprint_records = Blueprint('records', __name__)


@blueprint_records.route('/', methods=['GET'])
def get_recordings():
    if request.method == 'GET':
        recordsets = RecordsSet.query.all()
        return jsonify([c.serialize for c in recordsets])


@blueprint_records.route('/', methods=['POST'])
def add_new_recording():
    pass


@blueprint_records.route('/<int:set_id>', methods=['DELETE'])
def delete_records_set(set_id=None):
    pass
