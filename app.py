from flask import Flask
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from flask import render_template, flash, redirect, request, url_for, jsonify
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
    llamadas_y_rellamadas = "[['Llamadas por primera vez', %d], ['Re-llamadas', %d]]" %(
        Llamada.select().where(rellamada=False).count(),
        Llamada.select().where(rellamada=True).count())

    return render_template('estadisticas_listar.html', llamadas_y_rellamadas=llamadas_y_rellamadas)

@app.route("/llamada")
def llamada_listar():
    llamadas = Llamada.select().order_by(('fecha', 'desc')).limit(5)
    return render_template('llamada_listar.html', llamadas=llamadas)

@app.route("/llamada/crear", methods=['post', 'get'])
def llamada_crear():
    LlamadaForm = model_form(Llamada)

    if request.method == 'POST':
        form = LlamadaForm(request.form)

        if form.validate():
            llamada = Llamada()
            form.populate_obj(llamada)
            llamada.save()
            return redirect("/llamada?resaltar")
    else:
        form = LlamadaForm()

    return render_template('llamada_crear.html', form=form)

if __name__ == "__main__":
    admin_setup()
    app.run()
