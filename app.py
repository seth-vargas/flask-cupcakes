"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, serialize, Cupcake
from secret import SECRET_KEY

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///sb_cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

connect_db(app)


################################################## API routes ##################################################
@app.route("/api/cupcakes")
def get_cupcakes():
    """ Responds with JSON for all cupcakes """
    cupcakes = [serialize(cupcake) for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """ Get data about a single cupcake. """
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=serialize(cupcake))


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """ Create a cupcake with flavor, size, rating and image data from the body of the request. """
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    json = jsonify(cupcake=serialize(new_cupcake))

    return (json, 201)
