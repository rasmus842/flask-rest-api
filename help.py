import app, requests, json, pickle
from flask import Flask, Response

BASE = "http://127.0.0.1:5000"

categories = [
    {"id":0, "category_name":"toys"},
    {"id":1, "category_name":"books"},
    {"id":2, "category_name":"clothing"},  # category where there are no products
]

new_cat = {"id":3, "category_name":"children's section"}

products = [
{"id":0, "product_name":"Teddy-Bear", "price":9.99, "stock":5, "category_id":0},
    {"id":1, "product_name":"Yo-Yo", "price":1.50, "stock":80, "category_id":0},
    {"id":2, "product_name":"The Hobbit", "price":11.00, "stock":15, "category_id":1},
    {"id":3, "product_name":"A Storm of Swords", "price":7.99, "stock":2, "category_id":1},
    {"id":4, "product_name":"Apple", "price":1.59, "stock":10, "category_id":3}, # product with an invalid category_id
]

# May use requests.get / .put / .post / .patch / .delete to test app here
# pickle.dumps(response) for text/html, response.json() for json-serializable objects

"""
response = requests.get(BASE + "/shop")
print(response)
print(pickle.dumps(response))
print(response.headers["Content-Type"])
"""

for c in categories:
    response = requests.put(BASE + "/category/" + str(c["id"]), c)
    print(response.json())
    print(response)

for p in products:
    response = requests.put(BASE + "/product/" + str(p["id"]), p)
    print(response.json())
    print(response)


"""
for p in products:
    response = requests.post(BASE + "/products", data=p)
    print(response.json())
    print(response)

for c in categories:
    response = requests.delete(BASE + "/category/" + str(c["id"]))
    print(response.json())
    print(response)

for c in categories:
    response = requests.patch(BASE + "/category/" + str(c["id"]), c)
    print(response.json())
    print(response)

for p in products:
    response = requests.patch(BASE + "/product/" + str(p["id"]), p)
    print(response.json())
    print(response)

for p in products:
    response = requests.delete(BASE + "/product/" + str(p["id"]))
    print(response.json())
    print(response)    


for p in products:
    response = requests.get(BASE + "/product/" + str(p["id"]))
    print(response.json())
    print(response)

for c in categories:
    response = requests.get(BASE + "/category/" + str(c["id"]))
    print(response.json())
    print(response)


response = requests.get(BASE + "/categories")
print(response.json())
print(response)

for p in products:
    response = requests.post(BASE + "/products", data=p)
    print(response.json())
    print(response)

"""
