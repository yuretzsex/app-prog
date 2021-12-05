from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from models import User, Announcement, Local, Public, Session
from validation_schemas import announcement_schema
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import json

announcement = Blueprint('announcement', __name__)
session = Session()

@announcement.route('/announcement', methods=['POST'])
@jwt_required()
def create_announcement():
    data = request.json

    try:
        announcement_schema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    username = get_jwt_identity()
    user = session.query(User).filter_by(username=username).first()

    announcement = Announcement(title=data['title'],
                                content=data['content'],
                                authorid=user.id)

    session.add(announcement)
    session.commit()
    if data['isLocal']:
        session.add(Local(announcementid=announcement.id))
    else:
        session.add(Public(announcementid=announcement.id))
    session.commit()
    session.close()
    return Response(response='Announcement was successfuly created')


@announcement.route('/announcement', methods=['GET'])
def get_list():

    announcement_list = session.query(Announcement).join(Public, Public.announcementid == Announcement.id)
    ann_json = []
    for ann in announcement_list:
        ann_json.append({'title': ann.title,
                         'content': ann.content,
                         'author': session.query(User).
                        filter_by(id=ann.authorid).first().username})

    return jsonify({'announcement_list': ann_json})


@announcement.route('/announcement/local', methods=['GET'])
@jwt_required()
def get_local_list():
    username = get_jwt_identity()
    user = session.query(User).filter_by(username=username).first()

    announcement_list = session.query(Announcement).\
        join(Local, Local.announcementid == Announcement.id).\
        join(User, User.id == Announcement.authorid).\
        filter_by(city=user.city)
    ann_json = []
    for ann in announcement_list:
        ann_json.append({'title': ann.title,
                         'content': ann.content,
                         'author': session.query(User).
                        filter_by(id=ann.authorid).first().username})

    return jsonify({'announcement_list': ann_json})

@announcement.route('/announcement/<announementId>', methods=['GET'])
def get_announcement(announementId):

    public = session.query(Public).filter_by(announementid=announementId).first()
    if not public:
        return Response(status=404, response='No such public announcement')
    ann = session.query(Announcement).filter_by(id=public.announcementid).first()

    ann_json = {'title': ann.title,
                'content': ann.content,
                'author': session.query(User).
                    filter_by(id=ann.authorid).first().username}

    return jsonify({'announcement': ann_json})


@announcement.route('/announcement/local/<announementId>', methods=['GET'])
@jwt_required()
def get_local(announementId):
    username = get_jwt_identity()
    user = session.query(User).filter_by(username=username).first()

    local = session.query(Local).filter_by(announementid=announementId).first()
    if not local:
        return Response(status=404, response='No such local announcement')
    ann = session.query(Announcement).filter_by(id=local.announcementid).first()
    author = session.query(User).filter_by(id=ann.authorid).first()
    if author.city != user.city:
        return Response(status=404, response='You are not allowed')

    ann_json = {'title': ann.title,
                         'content': ann.content,
                         'author': session.query(User).
                        filter_by(id=ann.authorid).first().username}

    return jsonify({'announcement': ann_json})


@announcement.route('/announcement/<announementId>', methods=['PUT'])
@jwt_required()
def update_announcement(announementId):
    data = request.json
    try:
        announcement_schema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    username = get_jwt_identity()
    user = session.query(User).filter_by(username=username).first()

    announcement = session.query(Announcement).filter_by(id=announementId).first()
    if(announcement.authorid != user.id):
        return Response(status=404, response='You are not allowed to edit this announcement')

    local = session.query(Local).filter_by(announcementid=announementId).first()

    if 'title' in data.keys():
        announcement.title = data['title']
    if 'content' in data.keys():
        announcement.content = data['content']
    if 'isLocal' in data.keys():
        if data['isLocal'] and not local:
            session.delete(session.query(Public).filter_by(announcementid=announementId).first())
            session.add(Local(announcementid=announcement.id))
        else:
            session.delete(local)
            session.add(Public(announcementid=announcement.id))
    session.commit()
    session.close()
    return Response(response='Announcement was successfuly updated')


@announcement.route('/announcement/<announcementId>', methods=['DELETE'])
@jwt_required()
def delete_announcement(announcementId):

    username = get_jwt_identity()
    user = session.query(User).filter_by(username=username).first()

    announcement = session.query(Announcement).filter_by(id=announcementId).first()
    if (announcement.authorid != user.id):
        return Response(status=404, response='You are not allowed to delete this announcement')

    local = session.query(Local).filter_by(announcementid=announcementId).first()
    if not announcement:
        return Response(status=404, response="Announcement was not found")

    if local:
        session.delete(local)
    else:
        session.delete(session.query(Public).filter_by(announcementid=announcementId).first())
    session.delete(announcement)
    session.commit()
    session.close()
    return Response(response="Announcement was deleted")