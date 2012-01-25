
import datetime
from peewee import *

from app import db

class Note(db.Model):
    message = TextField()
    created = DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.message
