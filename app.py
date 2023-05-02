"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, serialize, Cupcake
from secret import SECRET_KEY

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///sb_cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

connect_db(app)


################################################## HTML routes ##################################################
@app.route("/")
def show_cupcakes():
    """ 
    This should return an HTML page (via render_template). This page should be entirely static (the route should just render the template, without providing any information on cupcakes in the database). It should show simply have an empty list where cupcakes should appear and a form where new cupcakes can be added.
    """
    return render_template("show-cupcakes.html", cupcakes=Cupcake.query.all())


@app.route("/cupcakes/<int:id>")
def show_cupcake(id):
    return render_template("show-cupcake.html", cupcake=Cupcake.query.get(id))


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
    flavor = request.json.get("flavor", None)
    size = request.json.get("size", None)
    rating = int(request.json.get("rating", None))
    image = request.json.get("image", None)

    if flavor and size and rating:
        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

        db.session.add(new_cupcake)
        db.session.commit()

        json = jsonify(cupcake=serialize(new_cupcake))

        return (json, 201)
    else:
        invalid_inputs = []

        if not flavor:
            invalid_inputs.append("flavor")
        elif not size:
            invalid_inputs.append("size")
        elif not rating:
            invalid_inputs.append("rating")
            
        json = jsonify(message="ERROR: Invalid form submission", invalid_inputs=invalid_inputs)
        return (json, 400)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """
    Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request.
    You can always assume that the entire cupcake object will be passed to the backend.
    """
    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = int(request.json.get("rating", cupcake.rating))
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()

    return jsonify(cupcake=serialize(cupcake))


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message="deleted")