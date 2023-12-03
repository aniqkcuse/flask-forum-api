from serializers import DiscussionSchema
from flask_restful import Resource, reqparse
from models import Discussion, Topic, User
from config_app import db

discussion_schema = DiscussionSchema()

discussion_parser = reqparse.RequestParser()
discussion_parser.add_argument('topic')
discussion_parser.add_argument('title', required=True)
discussion_parser.add_argument('description', required=True)
discussion_parser.add_argument('author')

class DiscussionGeneralData(Resource):
    def get(self):
        discussions = db.session.execute(db.select(Discussion).order_by(Discussion.id)).scalars()
        return [{"id":x.id, "topic":x.topic, "title":x.title, "description":x.description, "answer":[y.content for y in x.answer], "author":x.author} for x in discussions]

    def post(self):
        args = discussion_parser.parse_args()
        topic = db.session.get(Topic, args["topic"])
        author = db.session.get(User, args["author"])
        discussion = Discussion(topic=topic.id, title=args["title"], description=args["description"], author=author.id)
        db.session.add(discussion)
        db.session.commit()
        return {"msg":"Discussion created"}

class DiscussionData(Resource):
    def get(self, pk):
        discussion = db.session.get(Discussion, pk)
        return discussion_schema.dump(discussion)

    def put(self, pk):
        args = discussion_parser.parse_args()
        discussion = db.session.get(Discussion, pk)
        discussion.title = args["title"]
        discussion.description = args["description"]
        db.session.add(discussion)
        db.session.commit()
        return {"msg":"Discussion updated"}

    def delete(self, pk):
        discussion = db.session.get(Discussion, pk)
        db.session.delete(discussion)
        db.session.commit()
        return {"msg":"Discussion deleted"}


