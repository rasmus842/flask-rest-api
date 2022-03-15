import unittest, requests, json, pickle
from app import Categories, Products, Category, Product
from flask import Flask

class TestAPI(unittest.TestCase):
    BASE = "http://127.0.0.1:5000"
    categories = [
        {"id":0, "category_name":"toys"},
        {"id":1, "category_name":"books"},
        {"id":2, "category_name":"clothing"},  # category where there are no products
    ]
    products = [
        {"id":0, "product_name":"Teddy-Bear", "price":9.99, "stock":5, "category_id":0},
        {"id":1, "product_name":"Yo-Yo", "price":1.50, "stock":80, "category_id":0},
        {"id":2, "product_name":"The Hobbit", "price":11.00, "stock":15, "category_id":1},
        {"id":3, "product_name":"A Storm of Swords", "price":7.99, "stock":2, "category_id":1},
        {"id":4, "product_name":"Apple", "price":1.59, "stock":10, "category_id":3}, # product which doesn't belong to a category
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
            new_cat = Categories(id=c["id"], category_name=c["category_name"])
            self.assertEqual(c["id"], new_cat.id)
            self.assertEqual(c["category_name"], new_cat.category_name)

    # test Product database model constructor
    def test_product_model(self):
        for p in self.products:
            new_prod = Products(id=p["id"], product_name=p["product_name"], price=p["price"], stock=p["stock"], category_id=p["category_id"])
            self.assertEqual(p["id"], new_prod.id)
            self.assertEqual(p["product_name"], new_prod.product_name)
            self.assertEqual(p["price"], new_prod.price)
            self.assertEqual(p["stock"], new_prod.stock)
            self.assertEqual(p["category_id"], new_prod.category_id)

    # test routes - get_categories(), get_products(), index(), exit(), and shop()
    # test get_categories()
    # status_code, response is json-serializable, content correct
    def test_get_categories(self):
        r = self.tester.get("/categories")
        sc = r.status_code
        if sc == 200:
            self.assertEqual(r.headers["Content-Type"], "application/json")
            self.assertTrue("category_name" in json.dumps(r.json()))

    # test route get_products()
    # status_code, response is json-serializable, content correct
    def test_get_products(self):
        for p in self.products:
            r = self.tester.post("/products", data=p)
            sc = r.status_code
            if sc == 200:
                self.assertEqual(r.headers["Content-Type"], "application/json")
                self.assertTrue("product_name" in json.dumps(r.json()))
    
    # test route index()
    # status_code, content matches  (compare bytes), use pickle.dumps for text/html
    # !!!content has list of categories -- have not implemented mock-database for this
    # !!! app.py has to run while running test_app.py. This test will fail if not since using requests and not test_client
    def test_index(self):
        #for c in categories:
        r = requests.get(self.BASE + "/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(b"<select class" in pickle.dumps(r))

    # test route shop()
    # status_code, content match (compare bytes), use pickle.dumps for text/html
    # !!!can also check for when category isn't found. check for product list aswell
    # !!! app.py has to run while running test_app.py. This test will fail if not since using requests and not test_client
    def test_shop(self):
        for c in self.categories:
            r = requests.post(self.BASE + "/shop", data=c)
            self.assertEqual(r.status_code, 200)
            r_bytes = pickle.dumps(r)
            if c["category_name"] == "Select category":
                self.assertTrue(b"Please return to main page!" in r_bytes)
            elif b"Category not found!" in r_bytes:
                self.assertTrue(b"<form action" in r_bytes)
            else:
                self.assertTrue(b"<thead class" in r_bytes)

    # test route admin()
    # !!!not yet implemented!
    #def test_admin(self):


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
        pass

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
        pass

if __name__ == "__main__":
    unittest.main()