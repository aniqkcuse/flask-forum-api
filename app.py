from models import User, Comments, Topic, Discussion, db
from serializers import UserSchema, CommentsSchema, TopicSchema, DiscussionSchema, ma
from config_app import app, api
from flask_restful import Resource, reqparse

#Testing data
with app.app_context():
    db.create_all()
    username_schema = UserSchema()
    usernames_schema = UserSchema(many=True)

    topic_schema = TopicSchema()
    topics_schema = TopicSchema(many=True)

    discussion_schema = DiscussionSchema()
    discussions_schema = DiscussionSchema(many=True)

    comment_schema = CommentsSchema()
    comments_schema = CommentsSchema(many=True)

    user_parser = reqparse.RequestParser()
    user_parser.add_argument('username', required=True)
    user_parser.add_argument('email', required=True)

    topic_parser = reqparse.RequestParser()
    topic_parser.add_argument('name', required=True)
    
    discussion_parser = reqparse.RequestParser()
    discussion_parser.add_argument('topic')
    discussion_parser.add_argument('title', required=True)
    discussion_parser.add_argument('description', required=True)
    discussion_parser.add_argument('author')

    comment_parser = reqparse.RequestParser()
    comment_parser.add_argument('content', required=True)
    comment_parser.add_argument('author')
    comment_parser.add_argument('forum_id')

    class UserGeneralData(Resource):
        def get(self):
            users = db.session.execute(db.select(User).order_by(User.id)).scalars()
            return [{"id":x.id, "username":x.username, "email":x.email} for x in users]
        
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

    class CommentGeneralData(Resource):
        def get(self):
            comments = db.session.execute(db.select(Comments).order_by(Comments.id)).scalars()
            return [{"id":x.id, "content":x.content, "author":x.author, "forum_id":x.forum_id} for x in comments]

        def post(self):
            args = comment_parser.parse_args()
            author = db.session.get(User, args["author"])
            forum_id = db.session.get(Discussion, args["forum_id"])
            comment = Comments(content=args["content"], author=author.id, forum_id=forum_id.id)
            db.session.add(comment)
            db.session.commit()
            return {"msg":"Comment created"}
    
    class CommentData(Resource):
        def get(self, pk):
            comment = db.session.get(Comments, pk)
            return comment_schema.dump(comment)

        def put(self, pk):
            args = comment_parser.parse_args()
            comment = db.session.get(Comments, pk)
            comment.content = args["content"]
            db.session.add(comment)
            db.session.commit()
            return {"msg":"Comment update"}

        def delete(self, pk):
            comment = db.session.get(Comments, pk)
            db.session.delete(comment)
            db.session.commit()
            return {"msg":"Comment deleted"}

    api.add_resource(UserGeneralData, "/api/v1/user/")
    api.add_resource(UserData, "/api/v1/user/<int:pk>/")
    api.add_resource(TopicGeneralData, "/api/v1/topic/")
    api.add_resource(TopicData, "/api/v1/topic/<int:pk>/")
    api.add_resource(DiscussionGeneralData, "/api/v1/discussion/")
    api.add_resource(DiscussionData, "/api/v1/discussion/<int:pk>/")
    api.add_resource(CommentGeneralData, "/api/v1/comment/")
    api.add_resource(CommentData, "/api/v1/comment/<int:pk>/")

