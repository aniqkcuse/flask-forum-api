from models.serializers import UserSchema
from flask_restful import reqparse, Resource
from utils.config_app import db
from models.models import User
from passlib.hash import scrypt

username_schema = UserSchema()

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True)
user_parser.add_argument('password', required=True)
user_parser.add_argument('email', required=True)

class UserGeneralData(Resource):
    def get(self):
        users = db.session.execute(db.select(User).order_by(User.id)).scalars()
        return [{"id":x.id, "username":x.username, "password":x.password, "email":x.email} for x in users]
        
    def post(self):
        args = user_parser.parse_args()
        password = scrypt.hash(args["password"])
        user = User(username=args["username"], password=password, email=args["email"])
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
        user.password = scrypt.hash(args["password"])
        user.email = args["email"]
        db.session.add(user)
        db.session.commit()
        return {"msg":"User updated"}

    def delete(self, pk):
        user = db.session.get(User, pk)
        db.session.delete(user)
        db.session.commit()
        return {"msg":"User deleted"}
