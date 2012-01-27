from flask import Flask
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from flask import render_template, flash, redirect, request, url_for
from wtfpeewee.orm import model_form


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = Database(app)

auth = Auth(app, db)

from models import *

def admin_setup():
    admin = Admin(app, auth)
    #admin.register(Note)

    admin.setup()

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/estadisticas")
def estadisticas_listar():
    return render_template('estadisticas_listar.html')

@app.route("/llamada/crear", methods=['post', 'get'])
def llamada_crear():
    LlamadaForm = model_form(Llamada)

    if request.method == 'POST':
        form = LlamadaForm(request.form)

        if form.validate():
            llamada = Llamada()
            form.populate_obj(llamada)
            llamada.save()
            flash("Se ha creado la llamada con identificador: %s" %(llamada.id))
            return redirect(url_for('homepage'))
    else:
        form = LlamadaForm()

    return render_template('llamada_crear.html', form=form)

if __name__ == "__main__":
    admin_setup()
    app.run()
