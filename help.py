import requests
from flask import Response

BASE = "http://127.0.0.1:5000"

categories = [
    {"id":0, "name":"toys"},
    {"id":1, "name":"books"},
    {"id":2, "name":"clothing"},  
    {"id":3, "name":"fruits"}
]

products = [
{"id":0, "name":"Teddy-Bear", "price":9.99, "stock":5, "category_id":0},
    {"id":1, "name":"Yo-Yo", "price":1.50, "stock":80, "category_id":0},
    {"id":2, "name":"The Hobbit", "price":11.00, "stock":15, "category_id":1},
    {"id":3, "name":"A Storm of Swords", "price":7.99, "stock":2, "category_id":1},
    {"id":4, "name":"Apple", "price":1.59, "stock":10, "category_id":3}, 
]

for c in categories:
    response = requests.put(BASE + "/category/" + str(c["id"]), c)
    print(response.json())

for p in products:
    response = requests.put(BASE + "/product/" + str(p["id"]), p)
    print(response.json())