from datetime import datetime, timezone
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from models.models import TokenBlocklist, User
from utils.config_app import db, jwt
from passlib.hash import scrypt

args_parser = reqparse.RequestParser()

args_parser.add_argument("username", required=True)
args_parser.add_argument("password", required=True)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None

class Authentication(Resource):
    # Login
    def post(self):
        args = args_parser.parse_args()
        user = User.query.filter_by(username=args["username"]).first()
        if (scrypt.verify(args["password"], user.password)):
            access_token = create_access_token(identity=user.id)
            refrest_token = create_refresh_token(identity=user.id)
            return {"access_token":access_token, "refrest_token":refrest_token}
        else:
            return {"error": "Incorrect username or password"}, 401
    
    # Logout
    @jwt_required()
    def delete(self):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, type=ttype, user_id=get_jwt_identity(), created_at=now.isoformat()))
        db.session.commit()
        return {"message":"JWT revoked"}

class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return {"access_token": access_token}

