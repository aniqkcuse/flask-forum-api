from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(20), nullable=False)

class Comments(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    author: Mapped[int] = mapped_column(ForeignKey("user.id"))

class Topic(db.Model):
    name: Mapped[str] = mapped_column(String(20), primary_key=True, nullable=False)

class Discussion(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic: Mapped[str] = mapped_column(ForeignKey("topic.name"))
    title: Mapped[str] = mapped_column(String(40), nullable=False)
    answer: Mapped[int] = mapped_column(ForeignKey("comments.id"))
    author: Mapped[int] = mapped_column(ForeignKey("user.id"))
