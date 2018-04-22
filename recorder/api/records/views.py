"""
View module for working with categories
add, delete, get
"""
import os
from flask import Blueprint, request, jsonify, json

from recorder.api.records.models import RecordsSet, VideoCollectionItem, Video
from recorder.database import db
from recorder.error_helper import InvalidUsage

blueprint_records = Blueprint('records', __name__)


@blueprint_records.route('/', methods=['GET'])
def get_recordings():
    if request.method == 'GET':
        recordsets = RecordsSet.query.all()
        return jsonify([c.serialize for c in recordsets])


@blueprint_records.route('/', methods=['POST'])
def add_new_recording():
    if request.method == 'POST':

        recordsSet = RecordsSet()
        form_data = None

        try:
            if hasattr(request, 'data') and request.content_type == 'application/json':
                form_data = json.loads(request.data)
            elif 'multipart/form-data' in request.content_type:
                form_data = request.form
            else:
                db.session.rollback()
                raise InvalidUsage('Incorrect content type.', status_code=500)
        except:
            db.session.rollback()
            raise InvalidUsage('Get post data error.', status_code=500)

        # print(form_data)

        try:
            if 'name' not in form_data or not form_data['name'].strip():
                db.session.rollback()
                raise InvalidUsage('Field name is empty', status_code=400)
            name = form_data['name']
            recordsSet.name = name
        except:
            db.session.rollback()
            raise InvalidUsage('Wrong input data', status_code=400)

        db.session.add(recordsSet)
        db.session.commit()

        new_record_set = RecordsSet.query.get(recordsSet.id)

        try:
            if 'recording' not in form_data or not form_data['recording']:
                db.session.rollback()
                raise InvalidUsage('Field recording is empty', status_code=400)
            recording = form_data['recording']
        except:
            db.session.rollback()
            raise InvalidUsage('Wrong input data', status_code=400)

        try:
            for video_item in recording:

                video = Video.query.get(video_item['video']['id'])

                if not video:
                    new_video = Video(id=video_item['video']['id'], name='video-{0}'.format(video_item['video']['id']),
                                      url=video_item['video']['url'])
                    db.session.add(new_video)
                    db.session.commit()

                collection_item = VideoCollectionItem()
                collection_item.records_set_id = recordsSet.id
                collection_item.video_id = video_item['video']['id']
                collection_item.start_time = video_item['startTime']
                collection_item.finish_time = video_item['finishTime']

                db.session.add(collection_item)
                db.session.commit()
        except:
            db.session.rollback()
            raise InvalidUsage('Wrong input data', status_code=400)

        return jsonify(dict(success=True))


@blueprint_records.route('/<int:set_id>', methods=['DELETE'])
def delete_records_set(set_id=None):
    records_set = RecordsSet.query.get(set_id)

    if records_set:
        db.session.delete(records_set)
        db.session.commit()
        return jsonify(dict(success=True))
    else:
        return jsonify(dict(success=False, message='record set does not exists'))
