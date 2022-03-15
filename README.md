A REST API using flask framework

Deployment:
Make sure you have pip, python3, python3 virtual environment, and sqlite3 installed:

    $ sudo apt update
    $ sudo apt upgrade
    $ python3 --version
    $ sqlite3 --version
    $ pip --version

Python-3.8.10, sqlite3-3.31.1 for this application, pip 9.0.1 (python 3.X) or similar
If need be, install or update python, sqlite, and python virtualenv.

    $ sudo apt install python3
    $ sudo apt install python3-venv
    $ sudo apt instell sqlite3

Create a new directory called flask-rest-api/ and move into it

    $ mkdir flask-rest-api/
    $ cd flask-rest-api/
    
Then Clone this git repository in the same directory:

    flask-rest-api/$ git clone git@github.com:rasmus842/flask-rest-api.git
    
There should be the following files in your folder now: requirements.txt, app.py, help.py, and test_app.py.

    flask-rest-api/$ ls -a

Next, create a new python virtual environment in that directory with a name such as .venv:

    flask-rest-api/$ python3 -m venv .venv

Activate venv:
(note: after actiavtin venv, python3 and pip3 may be run on commandline with python and pip respectively

    flask-rest-api/$ source .venv/bin/activate

The dependencies to run the application are located in requirements.txt
Install dependencies by running the following command in your command line:
(packages: Flask, flask-restful, Flask-SQLAlchemy, requests)

    (.venv) $ pip install -r requirements.txt

Check if installed dependencies match the contents of requirements.txt by running:

    (.venv) $ pip freeze

Now everything should be set for running the application.

At first we should create a new database with python CLI:

    (.venv) $ python
    (.venv) >>> from app import db
    (.venv) >>> db.create_all()
    (.venv) >>> exit()
    (.venv) $ 
    
To run flask application, run command:

    (.venv) $ python app.py

Or alternatively:

    (.venv) $ export FLASK_APP=app.py
    (.venv) $ flask run

You may ctrl+click the URL. The application is now running. To terminate, press ctrl+c.
In another terminal window, enter same diretory and activate venv:

    flask-rest-api/$ python3 -m venv .venv
    
Fill the database with some data by running help.py:

    (.venv) $ python help.py

You may view and manipulate the database with sqlite by running the following commands:

    (.venv) sqlite3 database.db
    (.venv) >>> .schema
    (.venv) >>> SELECT * FROM categories;
    (.venv) >>> SELECT * FROM products;
    (.venv) .exit

api end-points:

    base = "http://127.0.0.1:5000"
    get list of categories: base + "/categories"
    get list of products from category (<category_id>): base + "products/<category_id>"
    get/put/patch/delete category: base + "/category/<category_id>"
    get/put/patch/delte product: base + "/product/<product_id>"
    
To access api you may use curl from the command line:

    $ curl -i http://127.0.0.1:5000

You may also send http-requests to running api with python CLI (or any other tool for that matter, get-requests from browser with url aswell):
(note: you do not necessarily have to use venv for this, unless you want to avoid conflits with requests' package other versions)

    (.venv) $ python
    (.venv) >>> import requests
    (.venv) >>> response = requests.get("http://127.0.0.1:5000/category/2")
    (.venv) >>> response
    output: <Resonse status_code>
    (.venv) >>> response.json()
    output: <json-format code>
    (.venv) >>> response.headers
    output: <response headers>
    (.venv) .exit
    
other commands: requests.put(url, data), .patch(url, data), .delete(url, data)
    
To run unit tests:

    (.venv) python test_app.py

And finally, to exit virtual environment, run:

    (.venv) deactivate
    $
    
Delete unnecessary files manually:

    $ rm -Rf flask-rest-api
