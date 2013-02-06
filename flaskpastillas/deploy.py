import os
import inspect
from colorama import init
from colorama import Fore, Back, Style

import app
import models
from config import DATABASE

def crear_tablas():
    init(autoreset=True)

    auth = app.auth
    if os.path.exists(DATABASE['name']):
        print Fore.GREEN  + 'Creando el archivo ' + DATABASE['name']
        os.remove(DATABASE['name'])

    # Crear tablas
    auth.User.create_table(fail_silently=True)

    def es_un_modelo(clase):
        return inspect.isclass(c) and issubclass(c, models.db.Model)

    for nombre, clase in [(n, c) for n, c in inspect.getmembers(models) if es_un_modelo(c)]:
        clase.create_table(fail_silently=True)
        print Fore.GREEN  + 'Creando tabla para ' + nombre

    #Crear usuario admin
    admin = auth.User(username='admin', admin=True, active=True)
    admin.set_password('admin')
    admin.save()
    print Fore.GREEN + "Creando usuario admin"

    cargar_provincias()


def cargar_provincias():
    from data import PROVINCIAS

    print Fore.GREEN + "Cargando la informacion de provincias"
    for provincia, codigo in PROVINCIAS:
        p = models.Provincia(nombre=provincia, codigo=codigo)
        p.save()

if __name__ == '__main__':
    crear_tablas()
