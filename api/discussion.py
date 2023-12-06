from models.serializers import DiscussionSchema
from flask_restful import Resource, reqparse
from models.models import Discussion, Topic, User
from utils.config_app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

discussion_schema = DiscussionSchema()

discussion_parser = reqparse.RequestParser()
discussion_parser.add_argument('topic', required=True)
discussion_parser.add_argument('title', required=True)
discussion_parser.add_argument('description', required=True)

class DiscussionGeneralData(Resource):
    @jwt_required()
    def get(self):
        discussions = db.session.execute(db.select(Discussion).order_by(Discussion.id)).scalars()
        return [{"id":x.id, "title":x.title} for x in discussions]

    @jwt_required()
    def post(self):
        args = discussion_parser.parse_args()
        topic = Topic.query.filter_by(name=args["topic"]).first()
        author = db.session.get(User, get_jwt_identity())
        discussion = Discussion(topic=topic.id, title=args["title"], description=args["description"], author=author.id)
        db.session.add(discussion)
        db.session.commit()
        return {"msg":"Discussion created"}

class DiscussionData(Resource):
    @jwt_required()
    def get(self, pk):
        discussion = db.session.get(Discussion, pk)
        if discussion.author == get_jwt_identity():
            return {"id":discussion.id, "topic":discussion.topic, "author":discussion.author, "title":discussion.title, "description":discussion.description, "comments": [y.content for y in discussion.answer]}
        else:
            return {"error":"Can't get discussion for another user"}, 401

    @jwt_required()
    def put(self, pk):
        args = discussion_parser.parse_args()
        discussion = db.session.get(Discussion, pk)
        if discussion.author == get_jwt_identity():
            discussion.title = args["title"]
            discussion.description = args["description"]
            db.session.add(discussion)
            db.session.commit()
            return {"msg":"Discussion updated"}
        else:
            return {"error":"Can't update discussion for another user"}, 401

    @jwt_required()
    def delete(self, pk):
        discussion = db.session.get(Discussion, pk)
        if discussion.author == get_jwt_identity():
            db.session.delete(discussion)
            db.session.commit()
            return {"msg":"Discussion deleted"}
        else:
            return {"error", "Can't delete discussion for another user"}, 401


