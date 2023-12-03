from serializers import CommentsSchema
from flask_restful import Resource, reqparse
from models import Comments, User, Discussion
from config_app import db

comment_schema = CommentsSchema()
    
comment_parser = reqparse.RequestParser()
comment_parser.add_argument('content', required=True)
comment_parser.add_argument('author')
comment_parser.add_argument('forum_id')

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
