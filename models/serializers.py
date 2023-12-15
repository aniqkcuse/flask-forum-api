from app.config_app import ma
from .models import User, Comments, Topic, Discussion, TokenBlocklist

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class CommentsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comments
        include_fk = True

class TopicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Topic
        include_fk = True

class DiscussionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Discussion
        include_fk = True

class TokenBlocklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TokenBlocklist
        include_fk = True
