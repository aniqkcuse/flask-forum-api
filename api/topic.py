from models.serializers import TopicSchema
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Topic, User
from utils.config_app import db

topic_schema = TopicSchema()

topic_parser = reqparse.RequestParser()
topic_parser.add_argument('name', required=True)

class TopicGeneralData(Resource):
    @jwt_required()
    def get(self):
        topics = db.session.execute(db.select(Topic).order_by(Topic.name)).scalars()
        return [{"id":x.id, "name":x.name} for x in topics]

    @jwt_required()
    def post(self):
        args = topic_parser.parse_args()
        identity = get_jwt_identity()
        author = db.session.get(User, identity)
        topic = Topic(name=args["name"], author=author.id)
        db.session.add(topic)
        db.session.commit()
        return {"msg":"Post created"}

class TopicData(Resource):
    @jwt_required()
    def get(self, pk):
        topic = db.session.get(Topic, pk)
        if topic.author == get_jwt_identity():
            return topic_schema.dump(topic)
        else:
            return {"error":"Can't check topic created by another user"}, 401

    @jwt_required()
    def put(self, pk):
        topic = db.session.get(Topic, pk)
        if topic.author == get_jwt_identity():
            args = topic_parser.parse_args()
            topic.name = args["name"]
            db.session.add(topic)
            db.session.commit()
            return {"msg":"Post updated"}
        else:
            return {"error":"Can't update topic created by another user"}, 401

    @jwt_required()
    def delete(self, pk):
        topic = db.session.get(Topic, pk)
        if topic.author == get_jwt_identity():
            db.session.delete(topic)
            db.session.commit()
            return {"msg":"Post deleted"}
        else:
            return {"error","Can't delete topic created by another user"}, 401
