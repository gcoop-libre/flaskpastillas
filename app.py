from flask import Flask
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from flask import render_template


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
    return render_template('homepage.html')

@app.route("/estadisticas")
def estadisticas_listar():
    return render_template('estadisticas_listar.html')

@app.route("/llamada/crear")
def llamada_crear():
    return render_template('llamada_crear.html')

if __name__ == "__main__":
    admin_setup()
    app.run()
