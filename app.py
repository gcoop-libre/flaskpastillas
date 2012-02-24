from flask import Flask
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from flask import render_template, flash, redirect
from flask import request, url_for, jsonify

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = Database(app)

auth = Auth(app, db)

import models
import forms

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/salir")
def salir():
    flash("Hasta luego!")
    return redirect(url_for('homepage'))

@app.route("/estadisticas")
def estadisticas_listar():
    llamadas_y_rellamadas = "[['Llamadas por primera vez', %d], ['Re-llamadas', %d]]" %(
        Llamada.select().where(rellamada=False).count(),
        Llamada.select().where(rellamada=True).count())

    return render_template('estadisticas_listar.html', llamadas_y_rellamadas=llamadas_y_rellamadas)

@app.route("/llamada")
def llamada_listar():
    llamadas = models.DatosBase.select().order_by(('fecha', 'desc')).limit(5)
    return render_template('llamada_listar.html', llamadas=llamadas)

@app.route("/llamada/crear", methods=['post', 'get'])
def llamada_crear():

    if request.method == 'POST':
        form = forms.DatosBaseForm(request.form, csrf_enabled=True)
        print form

        if form.validate():
            datos = models.DatosBase()
            datos.cargar(form)
            return redirect(url_for('llamada_listar'))
    else:
        form = forms.DatosBaseForm(csrf_enabled=True)

    return render_template('llamada_crear.html', form=form)

if __name__ == "__main__":
    app.run()
