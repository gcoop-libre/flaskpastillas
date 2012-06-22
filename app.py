# -*- encoding: utf-8 -*-
import os
import random
import redis
import time

from flask import Flask
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from peewee import Q
from flask_peewee.admin import Admin
from flask import render_template, flash, redirect, send_from_directory
from flask import request, url_for, jsonify, g
from functools import wraps
from werkzeug import secure_filename
from flask.ext.celery import Celery
from flask_debugtoolbar import DebugToolbarExtension
from celery import exceptions

from utils import Progreso


app = Flask(__name__)
app.config.from_pyfile('config.py')


db = Database(app)
auth = Auth(app, db)
adm = Admin(app, auth)
celery = Celery(app)
#toolbar = DebugToolbarExtension(app)

import models


@app.route("/")
@auth.login_required
def homepage():
    return redirect(url_for('llamada_listar'))

@app.route("/llamada")
@auth.login_required
def llamada_listar():
    return render_template('llamada_listar.html')

@app.route("/obtener_llamadas")
def obtener_llamadas():
    """Retorna un objeto json con llamadas para construir una tabla usando datatables.

    La cantidad de llamadas depende de varios parametros opcionales, cómo
    la página a mostrar y el nombre de la persona.
    """
    query = models.DatosBase.select()
    total = models.DatosBase.select().count()

    search = request.args.get('sSearch')
    limite = int(request.args.get('iDisplayLength'))
    desde = int(request.args.get('iDisplayStart'))

    datosbase = query.order_by(('fecha', 'desc')).paginate(desde/limite, limite)
    datosbase = datosbase.where(Q(nombre__icontains=search))

    # Extrae los datos en formato de tabla y los retorna convertidos en json.
    datos = [convertir_en_formato_de_tabla(d) for d in datosbase]

    return jsonify({'aaData': datos, 'iTotalDisplayRecords': datosbase.count(), 'iTotalRecords': total})

def convertir_en_formato_de_tabla(datosbase):
    "Convierte un registro de datos base en una lista de celdas para una tabla."
    name = link_to(datosbase.nombre, 'ver_datosbase', id=datosbase.id)
    localidad = datosbase.localidad
    cantidad = datosbase.cantidad_llamadas()
    edad = datosbase.edad
    tel = datosbase.telefono
    fecha = datosbase.fecha.strftime('%d/%m/%Y')
    acciones = "<a href='%s'>Agregar</a>" %(url_for('agregar_llamada', id=datosbase.id))
    return [name, localidad, cantidad, edad, tel, fecha, acciones]

@app.route("/salir")
def salir():
    auth.logout()
    return redirect("/")

@app.route("/estadisticas")
@auth.login_required
def estadisticas_listar():
    # Obtiene cantidad de personas de dos grupos: los que tienen manual y los que no.
    tienen_manual = "[['Tiene manual', %d], ['No tiene manual', %d]]" %(
        models.Llamada.select().where(tiene_manual=True).count(),
        models.Llamada.select().where(tiene_manual=False).count())

    # Obtiene una lista de provincias y la cantidad de personas que han llamado
    # de cada una (se suprimen las provincias de las que no se ha llamado
    # nunca).
    provincias = [[str(x.nombre), x.datos_base.count()] for x in models.Provincia.select()
                                                        if x.datos_base.count() > 0]

    return render_template('estadisticas_listar.html', tienen_manual=tienen_manual, provincias=str(provincias))


@app.route("/llamada/crear", methods=['post', 'get'])
@auth.login_required
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
@auth.login_required
def ver_datosbase(id):
    datosbase = models.DatosBase.get(id=id)
    llamadas = enumerate(datosbase.llamadas)
    return render_template('ver_datosbase.html', datosbase=datosbase, llamadas=llamadas)

@app.route("/llamada/crear/<int:id>", methods=['post', 'get'])
@auth.login_required
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

def link_to(body, url, *k, **kv):
    return "<a href='%s'>%s</a>" %(url_for(url, *k, **kv), body)

def helper_javascript(url, basepath='/static/js/', *k, **kv):
    return "<script src='{basepath}{url}' type='text/javascript'></script>".format(url=url, basepath=basepath)

def create_random_id(prefix):
    "Genera un nombre aleatorio con prefijo."
    aleatorio = random.randint(1000, 2000)
    return "%s_%d" %(prefix, aleatorio)

def helper_pie(values, title="untitled", size=100):
    id = create_random_id("pie")
    size = int((400 / 100.0) * size)
    return render_template('pie.html', id=id, size=size, title=title, values=values)

def helper_chart(values, title="untitled", size=100):
    id = create_random_id("chart")
    size = int((400 / 100.0) * size)
    return render_template('chart.html', id=id, size=size, title=title, values=values)

@app.context_processor
def helpers_personalizados():
    import flask
    return {'link_to': link_to, 'javascript': helper_javascript, 'pie': helper_pie, 'chart': helper_chart}

@app.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        if es_usuario_valido(request.form['nombre'], request.form['password']):
            g.user = request.form['nombre']
            return redirect('/')
        else:
            flash("El nombre de usuario o la clave son incorrectas", 'warning')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/importar")
@auth.login_required
def comenzar_a_importar():
    return render_template('importar.html')

def es_archivo_permitido(archivo):
    "Retorna True si el archivo indicado se puede subir al servidor."
    return '.' in archivo and archivo.endswith('xls')

@app.route("/importar/subir", methods=['POST'])
@auth.login_required
def importar_subir_archivo():
    if request.method == 'POST':
        file = request.files['archivo']
        if file and es_archivo_permitido(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('importacion_procesando', filename=filename))
        else:
            flash("El archivo %s no es un archivo excel 2003/XP/2000 valido" %(file.filename), "error")
            return redirect(url_for('importar'))

    return render_template('importar.html')

@app.route("/importar/procesando/<filename>")
@auth.login_required
def importacion_procesando(filename):
    ruta_al_archivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    ruta_al_archivo_errores = obtener_ruta_archivo_errores(ruta_al_archivo)

    try:
        res = importar.apply_async((ruta_al_archivo,))
        id_tarea = res.task_id
    except redis.exceptions.ConnectionError as e:
        flash("Error de conexion con redis: %s" %(e), 'error')
        return redirect(url_for('comenzar_a_importar'))

    return render_template("importar_procesando.html", nombre=filename, ruta_al_archivo_errores=ruta_al_archivo_errores.replace("/tmp/", ""), ruta_al_archivo=ruta_al_archivo, id_tarea=id_tarea)

@app.route("/importar/descargar/<filename>")
@auth.login_required
def descargar_archivo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@celery.task(name="app.sumar")
def sumar(a, b):
    time.sleep(1)
    return a + b


@celery.task(name="app.importar")
def importar(ruta):
    "Representa la tarea de importar registros desde archivos .xls"
    from importador import Importador

    importador = Importador(ruta, obtener_ruta_archivo_errores(ruta), 0.20)
    progreso = Progreso(importador.total)

    for fila in range(importador.total):
        importador.procesar_registro(progreso)
        importar.update_state(state="PROGRESS", meta=progreso.como_diccionario())

    importador.guardar_archivo_de_errores()

    importar.update_state(state="PROGRESS", meta=progreso.como_diccionario())
    return progreso.como_diccionario()

@app.route("/importar/obtener_estado/<tarea_id>")
@auth.login_required
def obtener_estado(tarea_id):
    "Informa el estado de una tarea en formato json."
    resultado = importar.AsyncResult(tarea_id)

    if resultado.ready():
        return jsonify({'resultado': resultado.info})
    else:
        if resultado.status == 'PROGRESS':
            return jsonify(resultado.info)
        else:
            return jsonify({'status': resultado.status})

def tareas_activas():
    "Retorna una lista de las tareas activas."
    tareas = celery.control.inspect()
    tareas_como_lista = tareas.active().values()[0]
    return [t["id"] for t in tareas_como_lista]

@app.route("/importar/cancelar")
@auth.login_required
def cancelar():
    flash("Se ha cancelado la importacion de registros", 'warning')
    return redirect(url_for('llamada_listar'))

@app.route("/importar/confirmar")
@auth.login_required
def confirmar():
    flash("Se han incorporado nuevos registros al sistema", 'info')
    return redirect(url_for('llamada_listar'))

def obtener_ruta_archivo_errores(archivo_a_procesar):
    return archivo_a_procesar.replace('.xls', '_errores.xls')

def generar_administrador(adm):
    adm.register(models.Provincia)
    adm.register(models.DatosBase)
    adm.register(models.Llamada)
    adm.register(models.AbortoAnterior)
    adm.register(models.InformacionIncorrecta)
    adm.register(models.IntentoDeAborto)
    adm.register(auth.User)
    adm.setup()



if __name__ == "__main__":
    generar_administrador(adm)
    app.run()
