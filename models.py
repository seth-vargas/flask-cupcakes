"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


def serialize(cupcake):
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": int(cupcake.rating),
        "image": cupcake.image
    }


class Cupcake(db.Model):
    """ Cupcake model """

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False, default="https://tinyurl.com/demo-cupcake")
