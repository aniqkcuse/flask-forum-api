from app.config_app import api, app
from api import user, topic, discussion, comment, auth
from flask import render_template

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

#Documentation of api
@app.route("/api/v1/doc/")
def documentation():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
