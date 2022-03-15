import unittest, requests, json
from app import Categories, Products, Category, Product
from flask import Flask

# using Python unittest, requests, and flask test_client to perform unit-tests

class TestAPI(unittest.TestCase):
    BASE = "http://127.0.0.1:5000"
    categories = [
        {"id":0, "name":"toys"},
        {"id":1, "name":"books"},
        {"id":2, "name":"clothing"},  # category where there are no products
    ]
    products = [
        {"id":0, "name":"Teddy-Bear", "price":9.99, "stock":5, "category_id":0},
        {"id":1, "name":"Yo-Yo", "price":1.50, "stock":80, "category_id":0},
        {"id":2, "name":"The Hobbit", "price":11.00, "stock":15, "category_id":1},
        {"id":3, "name":"A Storm of Swords", "price":7.99, "stock":2, "category_id":1},
        {"id":4, "name":"Apple", "price":1.59, "stock":10, "category_id":3}, # product which doesn't belong to a category
    ]
    
    # setup: create a new test_client, use a temporary database to test models
    # !!!temporary database not set up
    # !!! unit tests with main database at this moment
    def setUp(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        self.tester = app.test_client()
        #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        #self.temp_db = SQLAlchemy(tester)
        # how to add create tables for temp_db ??
        #self.temp_db.create_all()
    
    # teardown: 
    #def tearDown(self):
        #self.temp_db.drop_all()
        #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    # test Category database model constructor
    def test_category_model(self):
        for c in self.categories:
            new_cat = Categories(id=c["id"], name=c["name"])
            self.assertEqual(c["id"], new_cat.id)
            self.assertEqual(c["name"], new_cat.name)

    # test Product database model constructor
    def test_product_model(self):
        for p in self.products:
            new_prod = Products(id=p["id"], name=p["name"], price=p["price"], stock=p["stock"], category_id=p["category_id"])
            self.assertEqual(p["id"], new_prod.id)
            self.assertEqual(p["name"], new_prod.name)
            self.assertEqual(p["price"], new_prod.price)
            self.assertEqual(p["stock"], new_prod.stock)
            self.assertEqual(p["category_id"], new_prod.category_id)

    # test routes - get_categories(), get_products()
    # test get_categories()
    # status_code, response is json-serializable, content correct
    def test_get_categories(self):
        r = self.tester.get("/categories")
        sc = r.status_code
        if sc == 200:
            self.assertEqual(r.headers["Content-Type"], "application/json")
            self.assertTrue("name" in json.dumps(r.json()))

    # test route get_products()
    # status_code, response is json-serializable, content correct
    def test_get_products(self):
        for p in self.products:
            r = self.tester.post("/products", data=p)
            sc = r.status_code
            if sc == 200:
                self.assertEqual(r.headers["Content-Type"], "application/json")
                self.assertTrue("name" in json.dumps(r.json()))
    

    # test Category(Resource) and its get, put, patch, and delete methods
    # get method
    # status_code, is content json-serializable, and content itself
    def test_category_get(self):
        for c in self.categories:
            r = self.tester.get("/category/" + str(c["id"]))
            if r.status_code == 200:
                self.assertEqual(r.headers["Content-Type"], "application/json")
                self.assertTrue("category" in json.dumps(r.json()))

    # put method
    # status_code, is content json-serializable, and content itself
    def test_category_put(self):
        for c in self.categories:
            r = self.tester.put("/category/" + str(c["id"]))
            if r.status_code == 201:
                self.assertEqual(r.headers["Content-Type"], "application/json")
                self.assertTrue("category added" in json.dumps(r.json()))

    # patch method
    # status_code, is content json-serializable, and content itself
    def test_category_patch(self):
        for c in self.categories:
            r = self.tester.patch("/category/" + str(c["id"]))
            if r.status_code == 200:
                self.assertEqual(r.headers["Content-Type"], "application/json")
                self.assertTrue("category updated" in json.dumps(r.json()))

    # delete method
    # status_code, is content json-serializable, and content itself
    def test_category_delete(self):
        for c in self.categories:
            r = self.tester.delete("/category/" + str(c["id"]))
            if r.status_code == 200:
                self.assertEqual(r.headers["Content-Type"], "application/json")
                self.assertTrue("category deleted" in json.dumps(r.json()))

    # test Product(Resource) and its get,put,patch, and delete methods
    # get method
    # status_code, is content json-serializable, and content itself
    def test_product_get(self):
        for p in self.products:
            r = self.tester.get("/product/" + str(p["id"]))
            if r.status_code == 200:
                self.assertEqual(r.headers["Content-Type"], "application/json")
                self.assertTrue("product" in json.dumps(r.json()))

    # put method
    # status_code, is content json-serializable, and content itself
    def test_product_put(self):
        for p in self.products:
            r = self.tester.put("/product/" + str(p["id"]))
            if r.status_code == 201:
                self.assertEqual(r.headers["Content-Type"], "application/json")
                self.assertTrue("product updated" in json.dumps(r.json()))

    # patch method
    # status_code, is content json-serializable, and content itself
    def test_product_patch(self):
        for p in self.products:
            r = self.tester.patch("/product/" + str(p["id"]))
            if r.status_code == 200:
                self.assertEqual(r.headers["Content-Type"], "application/json")
                self.assertTrue("product deleted" in json.dumps(r.json()))

    # delete method
    # status_code, is content json-serializable, and content itself
    def test_product_delete(self):
        for p in self.products:
            r = self.tester.delete("/product/" + str(p["id"]))
            if r.status_code == 200:
                self.assertEqual(r.status_code, 200)
                self.assertEqual(r.headers["Content-Type"], "application/json")
                self.assertTrue("product deleted" in json.dumps(r.json()))

if __name__ == "__main__":
    unittest.main()
