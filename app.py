from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

# instantiate a new Flask application and wrap the app within an api
app = Flask(__name__)
api = Api(app)

# create a new db with sqlalchemy and sqlite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Create 2 tables for product categories and products
# Table for categories
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "Product category: {}".format(self.name)
        
# Create argument parsers to edit categories database
# primary key not required, other arguments NOT NULL
category_crud_args = reqparse.RequestParser()
category_crud_args.add_argument("id", type=int, help="Id of category", required=True)
category_crud_args.add_argument("name", type=str, help="Name of category", required=True)

# Table for products
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)

    def __init__(self, id, name, price, stock, category_id):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.category_id = category_id

    def __repr__(self):
        return "Product: {}, price: {}, product category_id: {}".format(self.name, self.price, self.category_id)

# Create argument parsers to edit product database
# primary key not required, other arguments NOT NULL
product_crud_args = reqparse.RequestParser()
product_crud_args.add_argument("id", type=int, help="Product id", required=True)
product_crud_args.add_argument("name", type=str, help="Name of product", required=True)
product_crud_args.add_argument("price", type=float, help="Price of product", required=True)
product_crud_args.add_argument("stock", type=int, help="Product stock", required=True)
product_crud_args.add_argument("category_id", type=int, help="Product category id", required=True)


# define objects for api: Category and Product. inherits from Resource

# Define product category resource to perform CRUD
class Category(Resource):
    def get(self, category_id):
        r = Categories.query.filter_by(id=category_id).first()
        if not r:
            return {"message": "Category doesn't exist..."}, 404

        output = {
            "id": r.id,
            "name": r.name
        }
        return {"category": output}, 200

    def put(self, category_id):
        # no duplicates - i.e. cannot have same id and cannot have same name
        # return the created object
        args = category_crud_args.parse_args()
        r = Categories.query.filter_by(id=category_id).first()
        if r:
            return {"message": "Category id taken..."}, 409

        c = Categories(id=category_id, name=args["name"])
        db.session.add(c)
        db.session.commit()

        output = {
            "id": args["id"],
            "name": args["name"]
        }
        return {"category added": output}, 201

    def patch(self, category_id):
        # if the entry doesn't exist, then return 404, raise 404 or smth

        args = category_crud_args.parse_args()
        r = Categories.query.filter_by(id=category_id).first()
        if not r:
            return {"message": "This category doesn't exist..."}, 404
        
        r.name = args["name"]
        db.session.commit()

        output = {
            "id": r.id,
            "name": r.name
        }
        return {"category updated": output}, 200

    def delete(self, category_id):
        # if already doesn't exist, then raise exception or return whatever code

        r = Categories.query.filter_by(id=category_id).first()
        if not r:
            return {"message": "This category already doesn't exist..."}, 404
                
        output = {
            "id": r.id,
            "name": r.name
        }
        db.session.delete(r)
        db.session.commit()

        return {"category deleted": output}, 200

# crud for products
class Product(Resource):
    def get(self, product_id):
        r = Products.query.filter_by(id=product_id).first()
        if not r:
            return {"message": "Product doesn't exist..."}, 404

        output = {
            "id": r.id,
            "name": r.name,
            "price": r.price,
            "stock": r.stock,
            "category_id": r.category_id
        }
        return {"product": output}, 200

    def put(self, product_id):
        # no duplicates - i.e. cannot have same id and cannot have same name
        # return the created object
        args = product_crud_args.parse_args()
        r = Products.query.filter_by(id=product_id).first()
        if r:
            return {"message": "Product id taken..."}, 409
        
        p = Products(id=product_id, name=args["name"], price=args["price"], stock=args["stock"], category_id=args["category_id"])
        db.session.add(p)
        db.session.commit()

        output = {
            "id": args["id"],
            "name": args["name"],
            "price": args["price"],
            "stock": args["stock"],
            "category_id": args["category_id"]
        }
        return {"product added": output}, 201

    def patch(self, product_id):
        args = product_crud_args.parse_args()
        r = Products.query.filter_by(id=product_id).first()
        if not r:
            return {"message": "This product doesn't exit"}, 204
        
        r.name = args["name"]
        r.price = args["price"]
        r.stock = args["stock"]
        r.category_id = args["category_id"]
        db.session.commit()

        output = {
            "id": r.id,
            "name": r.name,
            "price": r.price,
            "stock": r.stock,
            "category_id": r.category_id
        }
        return {"product updated": output}, 200

    def delete(self, product_id):

        r = Products.query.filter_by(id=product_id).first()
        if not r:
            return {"message": "This product already doesn't exist..."}, 204

        output = {
            "id": r.id,
            "name": r.name,
            "price": r.price,
            "stock": r.stock,
            "category_id": r.category_id
        }
        db.session.delete(r)
        db.session.commit()

        return {"product deleted": output}, 200

# add category and product resouces to api
api.add_resource(Category, "/category/<int:category_id>")
api.add_resource(Product, "/product/<int:product_id>")

# query for all categories, returns categories as a list of dictionaries
@app.route("/categories")
def get_categories():
    result = Categories.query.all()
    if not result:
        return {"message": "No categories found"}, 404
    output = []
    for r in result:
        c = {
            "id": r.id,
            "name": r.name
        }
        output.append(c)
    return {"categories": output}, 200

# query for all products of a given category by category_id, returns as a list of dictionaries
@app.route("/products/<int:category_id>")
def get_products(category_id):
    c = Categories.query.filter_by(id=category_id).first()
    if not c:
        return {"message": "No such category"}, 404

    result = Products.query.filter_by(category_id=category_id).all()

    output = []
    for r in result:
        p = {
            "id": r.id,
            "name": r.name,
            "price": r.price,
            "stock": r.stock,
            "category_id": r.category_id
        }
        output.append(p)
    return {c.name: output}, 200

@app.route("/")
def index():
    return {"message": "flask-rest-api by Rasmus Zalite!"}, 200

if __name__ == "__main__":
    app.run(debug=True)