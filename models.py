import datetime
from peewee import *

from app import db

class Llamada(db.Model):
    nombre_persona = CharField()
    rellamada = BooleanField()
    observacion = TextField()
    fecha = DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.nombre_persona

class DatosBase(db.Model):
    fecha = DateTimeField(default=datetime.datetime.now)
    telefono = CharField()
    nombre = CharField()
    edad = IntegerField()

    def __unicode__(self):
        return self.nombre

class AbortoAnterior(db.Model):
    tipo = CharField()
    observaciones = TextField()
