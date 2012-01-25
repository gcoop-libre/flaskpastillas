from flask import Flask
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = Database(app)

auth = Auth(app, db)

from models import *

def admin_setup():
    admin = Admin(app, auth)
    admin.register(Note)

    admin.setup()

@app.route("/")
def homepage():
    return "<a href='/admin'>admin</a>"

if __name__ == "__main__":
    admin_setup()
    app.run()
