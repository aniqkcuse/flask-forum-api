from sqlalchemy.orm import identity
from models.serializers import UserSchema
from flask_restful import reqparse, Resource
from utils.config_app import db
from models.models import User
from passlib.hash import scrypt
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

username_schema = UserSchema()

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True)
user_parser.add_argument('password', required=True)
user_parser.add_argument('email', required=True)

class UserGeneralData(Resource):
    @jwt_required()
    def get(self):
        users = db.session.execute(db.select(User).order_by(User.id)).scalars()
        return [{"id":x.id, "username":x.username} for x in users]
        
    def post(self):
        args = user_parser.parse_args()
        password = scrypt.hash(args["password"])
        user = User(username=args["username"], password=password, email=args["email"])
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return {"msg":"User created", "access_token":access_token, "refresh_token":refresh_token}

class UserData(Resource):
    @jwt_required()
    def get(self, pk):
        if pk == get_jwt_identity():
            user = db.session.get(User, pk)
            return username_schema.dump(user)
        else:
            return {"error":"Can't have permission to check another user"}, 401

    @jwt_required()
    def put(self, pk):
        if pk == get_jwt_identity():
            args = user_parser.parse_args()
            user = db.session.get(User, pk)
            user.username = args["username"]
            user.password = scrypt.hash(args["password"])
            user.email = args["email"]
            db.session.add(user)
            db.session.commit()
            return {"msg":"User updated"}
        else:
            return {"error":"Can't update another user"}, 401

    @jwt_required()
    def delete(self, pk):
        if pk == get_jwt_identity():
            user = db.session.get(User, pk)
            db.session.delete(user)
            db.session.commit()
            return {"msg":"User deleted"}
        else:
            return {"error":"Can't delete another user"}, 401
