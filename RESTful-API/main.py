from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice
from sqlalchemy.exc import NoResultFound

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {i.name: getattr(self, i.name, None) for i in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route("/random", methods=['GET'])
def random_cafe():
    cafe_random = choice(db.session.query(Cafe).all())
    return jsonify(cafe=cafe_random.to_dict())


@app.route('/all', methods=['GET'])
def all_cafe():
    return jsonify(cafes=[cafe.to_dict() for cafe in db.session.query(Cafe).all()])


@app.route('/search', methods=['GET'])
def search_cafe():
    loc = request.args.get('loc').title()
    cafes = db.session.query(Cafe).filter(Cafe.location == loc).all()
    if cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])
    else:
        return jsonify(error={'Not Found': "Sorry, we don't have a cafe at that location"})


## HTTP POST - Create Record

def str_to_boolean(arg_from_url: str):
    if arg_from_url in ['True', ' true', 'T', 't', 'Yes', 'yes', 'y', '1']:
        return True
    else:
        return False


@app.route('/add', methods=['POST'])
def add_cafe():
    cafe = Cafe(
        name=request.args.get("name"),
        map_url=request.args.get("map_url"),
        img_url=request.args.get("img_url"),
        location=request.args.get("location"),
        has_sockets=str_to_boolean(request.args.get("sockets")),
        has_toilet=str_to_boolean(request.args.get("toilet")),
        has_wifi=str_to_boolean(request.args.get("wifi")),
        can_take_calls=str_to_boolean(request.args.get("calls")),
        seats=request.args.get("seats"),
        coffee_price=request.args.get("coffee_price")
    )
    db.session.add(cafe)
    db.session.commit()
    return jsonify(response={'success': 'Successfully added the new cafe.'})


## HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id: int):
    try:
        cafe = db.session.query(Cafe).filter(Cafe.id == cafe_id).one()
    except NoResultFound:
        return jsonify(error={'Not Found': "Sorry a cafe with that id was not found in the database."}), 404
    else:
        cafe.coffee_price = request.args.get('new_price')
        db.session.commit()
        return jsonify(response={'success': 'Successfully update the price.'}), 200


## HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def report_closed(cafe_id):
    api_key = request.args.get('api-key')
    if api_key == 'TopSecretAPIKey':
        try:
            cafe = db.session.query(Cafe).filter(Cafe.id == cafe_id).one()
        except NoResultFound:
            return jsonify(error={'Not Found': "Sorry a cafe with that id was not found in the database."}), 404
        else:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
