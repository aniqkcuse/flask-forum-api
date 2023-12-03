from serializers import UserSchema
from flask_restful import reqparse, Resource
from config_app import db
from models import User

username_schema = UserSchema()

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True)
user_parser.add_argument('email', required=True)

class UserGeneralData(Resource):
    def get(self):
        users = db.session.execute(db.select(User).order_by(User.id)).scalars()
        return [{"id":x.id, "username":x.username, "email":x.email} for x in users]
        
    def post(self):
        args = user_parser.parse_args()
        if isinstance(args["username"], str) & isinstance(args["email"], str):
            user = User(username=args["username"], email=args["email"])
            db.session.add(user)
            db.session.commit()
            return {"msg":"User created"}
        else:
            return {"error":"The username and/or email should be string, not another type"}

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
