from models.serializers import CommentsSchema
from flask_restful import Resource, reqparse
from models.models import Comments, User, Discussion
from utils.config_app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

comment_schema = CommentsSchema()
    
comment_parser = reqparse.RequestParser()
comment_parser.add_argument('content', required=True)
comment_parser.add_argument('forum_id')

class CommentGeneralData(Resource):

    @jwt_required()
    def get(self):
        comments = db.session.execute(db.select(Comments).order_by(Comments.id)).scalars()
        return [{"id":x.id, "content":x.content} for x in comments]

    @jwt_required()
    def post(self):
        args = comment_parser.parse_args()
        author = db.session.get(User, get_jwt_identity())
        forum_id = db.session.get(Discussion, args["forum_id"])
        comment = Comments(content=args["content"], author=author.id, forum_id=forum_id.id)
        db.session.add(comment)
        db.session.commit()
        return {"msg":"Comment created", "comment": {"id":comment.id, "content":comment.content, 'forum_id':comment.forum_id}}
    
class CommentData(Resource):
    @jwt_required()
    def get(self, pk):
        comment = db.session.get(Comments, pk)
        if comment.author == get_jwt_identity():
            return comment_schema.dump(comment)
        else:
            return {"error":"Can't get comment of another user"}, 401

    @jwt_required()
    def put(self, pk):
        args = comment_parser.parse_args()
        comment = db.session.get(Comments, pk)
        if comment.author == get_jwt_identity():
            comment.content = args["content"]
            db.session.add(comment)
            db.session.commit()
            return {"msg":"Comment update", "comment": {"id": comment.id, "content": comment.content, "forum_id": comment.forum_id}}
        else:
            return {"error":"Can't update comment of another user"}, 401

    @jwt_required()
    def delete(self, pk):
        comment = db.session.get(Comments, pk)
        if comment.author == get_jwt_identity():
            db.session.delete(comment)
            db.session.commit()
            return {"msg":"Comment deleted"}
        else:
            return {"error":"Can't delete comment of another user"}, 401
