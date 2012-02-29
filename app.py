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

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/salir")
def salir():
    flash("Hasta luego!")
    return redirect(url_for('homepage'))

@app.route("/estadisticas")
def estadisticas_listar():
    llamadas_y_rellamadas = "[['Con nombre asd', %d], ['Con otro nombre', %d]]" %(
        models.DatosBase.select().where(nombre="asd").count(),
        models.DatosBase.select().where(nombre__ne="asd").count())

    return render_template('estadisticas_listar.html', llamadas_y_rellamadas=llamadas_y_rellamadas)

@app.route("/llamada")
def llamada_listar():
    datosbase = models.DatosBase.select().order_by(('fecha', 'desc')).limit(10)
    return render_template('llamada_listar.html', lista_datosbase=datosbase)

@app.route("/llamada/crear", methods=['post', 'get'])
def llamada_crear():
    import forms

    if request.method == 'POST':
        form = forms.DatosBaseForm(request.form, csrf_enabled=False)

        if form.validate():
            datos = models.DatosBase()
            datos.cargar(form)
            flash("Se han creado los datos base para '%s'" %(datos.nombre), 'success')
            return redirect(url_for('agregar_llamada', id=datos.id))
    else:
        form = forms.DatosBaseForm(csrf_enabled=False)

    return render_template('llamada_crear.html', form=form)

@app.route("/llamada/ver/<int:id>")
def ver_datosbase(id):
    datosbase = models.DatosBase.get(id=id)
    return render_template('ver_datosbase.html', datosbase=datosbase)

@app.route("/llamada/crear/<int:id>", methods=['post', 'get'])
def agregar_llamada(id):
    import forms

    if request.method == 'POST':
        form = forms.LlamadaForm(request.form, csrf_enabled=False)

        if form.validate():
            datos = models.Llamada()
            datos.cargar(form)
            flash("Se han guardado la llamada correctamente", 'success')
            return redirect(url_for('llamada_listar'))
    else:
        form = forms.LlamadaForm(csrf_enabled=False)
        form.datosbase_id.data = id

    return render_template('llamada_agregar.html', form=form)

@app.template_filter('dateformat')
def dateformat(value, format):
    return value.strftime(format)

@app.context_processor
def helpers_personalizados():
    import flask

    def link_to(body, url, *k, **kv):
        return "<a href='%s'>%s</a>" %(url_for(url, *k, **kv), body)

    return {'link_to': link_to}

if __name__ == "__main__":
    app.run()
