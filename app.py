from utils.config_app import api, app, db
from api import user, topic, discussion, comment, auth
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api.add_resource(user.UserGeneralData, "/api/v1/user/")
api.add_resource(user.UserData, "/api/v1/user/<int:pk>/")
api.add_resource(topic.TopicGeneralData, "/api/v1/topic/")
api.add_resource(topic.TopicData, "/api/v1/topic/<int:pk>/")
api.add_resource(discussion.DiscussionGeneralData, "/api/v1/discussion/")
api.add_resource(discussion.DiscussionData, "/api/v1/discussion/<int:pk>/")
api.add_resource(comment.CommentGeneralData, "/api/v1/comment/")
api.add_resource(comment.CommentData, "/api/v1/comment/<int:pk>/")
api.add_resource(auth.Authentication, "/api/v1/auth/")
api.add_resource(auth.Refresh, "/api/v1/refresh/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
