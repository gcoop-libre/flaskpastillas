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
