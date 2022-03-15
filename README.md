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
    
Next, create a new python virtual environment in that directory with a name such as .venv:

    flask-rest-api/$ python3 -m venv .venv

Activate venv:

    flask-rest-api/$ source .venv3/bin/activate

There should be the following files in your folder now: requirements.txt, app.py, help.py, test_app.py. 
And also folders containing .html-files in templates/ (and static/ which is empty at this time).

The dependencies to run the application are located in requirements.txt
Install dependencies by running the following command in your command line:

    (.venv) pip install -r requirements.txt

Check if installed dependencies match the contents of requirements.txt by running:

    (.venv) pip freeze

Now everything should be set for running the application.
To run flask application, run command:

    (.venv) python app.py

Or alternatively:

    (.venv) export FLASK_APP=app.py
    (.venv) flask run

The api should now be running and can be opened by pressing the URL with ctrl+click or by typing "http://127.0.0.1:5000" into browser.
To exit api press ctrl+c in terminal window.
The home page is where you may search for products.
Choose a category and click submit. After that a table with all products within that categorie will be displayed.
If the category is empty there will be simply be no products in the table.
If the category itself doesn't exist or if something went wrong, you will be directed to an error page, and click submit to redirect to home page.

There shouldn't be any products or categories displayed on the pages because the database is not yet created.
Create the database by running the following commands in the terminal:

    (.venv) python
    (.venv) from app import db
    (.venv) db.create_all()
    (.venv) exit()

Fill the database by running help.py:

    (.venv) python help.py

You may view the database with sqlite by running the following commands:

    (.venv) sqlite3 database.db
    (.venv) .schema
    
    (.venv) SELECT * FROM categories;
    (.venv) SELECT * FROM products;

    (.venv) .exit

To run unit tests:
(important to note app.py should be running while tests are run, otherwise failure will occur)

    (.venv) python test_app.py

And finally, to exit virtual environment, run:

    (.venv) deactivate
    $
