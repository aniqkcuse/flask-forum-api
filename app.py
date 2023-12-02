from models import User, Comments, Topic, Discussion, db
from serializers import UserSchema, CommentsSchema, TopicSchema, DiscussionSchema, ma
from config_app import app, api
from flask import request
from flask_restful import Resource, reqparse

#Testing data
with app.app_context():
    db.create_all()
    username_schema = UserSchema()
    topic_schema = TopicSchema()
    discussion_schema = DiscussionSchema()
    comment_schema = CommentsSchema()

    user_parser = reqparse.RequestParser()
    user_parser.add_argument('username', required=True)
    user_parser.add_argument('email', required=True)

    class UserAllData(Resource):
        def get(self):
            user = db.session.get(User, 3)
            return username_schema.dump(user)
        
        def post(self):
            args = user_parser.parse_args()
            user = User(username=args["username"], email=args["email"])
            db.session.add(user)
            db.session.commit()
            return {"msg":"User created"}

    class UserData(Resource):
        def get(self, pk):
            user = db.session.get(User, pk)
            return username_schema.dump(user)

        def put(self, pk):
            args = user_parser.parse_args()
            user = db.session.get(User, pk)
            user.username = args["username"]
            user.email = args["email"]
            db.session.add(user)
            db.session.commit()
            return {"msg":"User updated"}

        def delete(self, pk):
            user = db.session.get(User, pk)
            db.session.delete(user)
            db.session.commit()
            return {"msg":"User deleted"}

    api.add_resource(UserAllData, "/api/v1/user/")
    api.add_resource(UserData, "/api/v1/user/<int:pk>/")

    @app.get("/api/v1/topic/")
    def get_all_topic():
        topic = db.session.get(Topic, "TopicOne")
        return topic_schema.dump(topic)

    @app.get("/api/v1/discussion/")
    def get_all_discussion():
        discussion = db.session.get(Discussion, 1)
        return discussion_schema.dump(discussion)

    @app.get("/api/v1/comment/")
    def get_all_comment():
        comment = db.session.get(Comments, 1)
        return comment_schema.dump(comment)

