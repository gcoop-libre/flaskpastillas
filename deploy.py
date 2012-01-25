import os

import app
from models import Note
from config import DATABASE

auth = app.auth
if os.path.exists(DATABASE['name']):
    os.remove(DATABASE['name'])

#Crear tablas
auth.User.create_table(fail_silently=True)
Note.create_table(fail_silently=True)

#Crear usuario admin
admin = auth.User(username='admin', admin=True, active=True)
admin.set_password('admin')
admin.save()
