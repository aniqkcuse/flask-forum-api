from config_app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    forum_id = db.Column(db.Integer, db.ForeignKey("discussion.id"))

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Integer, db.ForeignKey("topic.id"))
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    answer = db.relationship('Comments', backref='answer')
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
