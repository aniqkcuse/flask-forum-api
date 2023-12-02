from config_app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.ForeignKey("user.id"))
    forum_id = db.Column(db.ForeignKey("discussion.id"))

class Topic(db.Model):
    name = db.Column(db.String(20), primary_key=True, nullable=False)

class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20), db.ForeignKey("topic.name"))
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    answer = db.relationship('Comments', backref='answer')
    author = db.Column(db.ForeignKey("user.id"))
