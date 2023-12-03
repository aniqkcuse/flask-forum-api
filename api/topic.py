from serializers import TopicSchema
from flask_restful import Resource, reqparse
from models import Topic
from config_app import db

topic_schema = TopicSchema()

topic_parser = reqparse.RequestParser()
topic_parser.add_argument('name', required=True)

class TopicGeneralData(Resource):
    def get(self):
        topics = db.session.execute(db.select(Topic).order_by(Topic.name)).scalars()
        return [{"id":x.id, "name":x.name} for x in topics]

    def post(self):
        args = topic_parser.parse_args()
        topic = Topic(name=args["name"])
        db.session.add(topic)
        db.session.commit()
        return {"msg":"Post created"}

class TopicData(Resource):
    def get(self, pk):
        topic = db.session.get(Topic, pk)
        return topic_schema.dump(topic)

    def put(self, pk):
        args = topic_parser.parse_args()
        topic = db.session.get(Topic, pk)
        topic.name = args["name"]
        db.session.add(topic)
        db.session.commit()
        return {"msg":"Post updated"}

    def delete(self, pk):
        topic = db.session.get(Topic, pk)
        db.session.delete(topic)
        db.session.commit()
        return {"msg":"Post deleted"}
