from dataclasses import dataclass
import requests
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint

# creating flask app
from producer import publish

app = Flask(__name__)
# adding sql config <mysql://[username]:[password]@[host name or service name]/[db name]>
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'

# adding cors to the app
CORS(app)

# getting db object
db = SQLAlchemy(app=app)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    # autoincrement is set to 'False' because this app
    # will not be creating products objects
    # this app is only supposed to retrieve product objects
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(length=200))
    image = db.Column(db.String(length=500))


@dataclass()
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route("/api/products")
def index():
    products = Product.query.all()
    return jsonify(products)


@app.route("/api/products/<int:id>/like", methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json_data = req.json()

    try:
        productUser = ProductUser(user_id=json_data['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
    except:
        abort(400, "You've already liked this product.")

    return jsonify({
        'message': 'success'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
