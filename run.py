from app.config_app import api, app
from api import user, topic, discussion, comment, auth
from doc import doc
import yaml

# Creation of different endpoint to the crud.
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

app.register_blueprint(doc.swagger_blueprint)

@app.route("/api/v1/swagger.yaml")
def swagger_yaml():
    with open('doc/openapi.yaml', 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

if __name__ == "__main__":
    app.run(debug=True)
