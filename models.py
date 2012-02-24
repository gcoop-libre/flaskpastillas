import datetime
from peewee import *

from app import db

class DatosBase(db.Model):
    fecha = DateTimeField(default=datetime.datetime.now)
    telefono = CharField()
    nombre = CharField()
    edad = IntegerField()

    def __unicode__(self):
        return self.nombre

    def cargar(self, form):
        datos = form.data
        self.nombre = datos['nombre']
        self.edad = datos['edad']
        self.save()

class AbortoAnterior(db.Model):
    tipo = CharField()
    observaciones = TextField()
