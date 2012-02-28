# -*- encoding: utf-8 -*-
import datetime
from peewee import *

from app import db

class Modelo(db.Model):
    """Representa un modelo que se puede cargar desde un formulario.
    
    Este método va a tratar de usar la intefaz del modelo para
    asociar los campos. Así que si tu formulario es complejo
    y tiene que tratar los datos antes de procesarlos, podría
    utilizar properties.

    Por ejemplo, si el formulario tiene un campo llamado 'csrf' podemos
    interceptarlo con la siguiente property::

        class MiModelo(Modelo):

            def get_csrf(self):
                pass

            def set_csrf(self, valor):
                print "Se quiere asignar el valor:", valor
                pass

            csrf = property(get_csrf, set_csrf)
    
    
    """

    def cargar(self, form):
        datos = form.data

        for (clave, valor) in datos.items():
            setattr(self, clave, valor)

        self.save()

class Provincia(db.Model):
    codigo = IntegerField()
    nombre = CharField()

    def __unicode__(self):
        return "%s (%s)" %(self.nombre, self.codigo)

class DatosBase(Modelo):
    fecha = DateTimeField(default=datetime.datetime.now)
    telefono = CharField()
    nombre = CharField()
    edad = IntegerField()
    provincia = ForeignKeyField(Provincia, related_name='llamadas')
    barrio = IntegerField()
    nacionalidad = CharField()
    localidad = CharField()

    def __unicode__(self):
        return self.nombre

class Llamada(Modelo):
    fecha = DateTimeField(default=datetime.datetime.now)
    motivo = IntegerField()
    reconfirmo_embarazo = IntegerField()
    metodo_comprobacion = IntegerField()
    fum = DateTimeField()
    edad_gestacional = IntegerField()
    semana_entero = IntegerField()
    motivo_mas_de_10_semanas = IntegerField()
    cantidad_de_hijos = IntegerField()
