Instalación
-----------

Para realizar la instalación necesitamos crear un entorno e instalar
todas las bibliotecas para flask.

::

    mkdir flaskpastillas
    cd flaskpastillas
    mkvirtualenv flaskpastillas
    workon flaskpastillas
    pip install -r requirements.txt


Es una *muy* buena idea usar ipython adentro del virtualenv. Sobretodo
si estás depurando cosas o investigando.

Este link explica cómo hacerlo:

- http://www.ahmedsoliman.com/2011/09/27/use-virtualenv-with-ipython-0-11/

Ejecutar la aplicación en modo desarrollo
-----------------------------------------

Primero hay que entrar en el entorno, y luego
lanzar del servidor de prueba::

    workon flaskpastillas
    python app.py


Iniciar Redis y Celery
----------------------

El sistema de importación de registros en el sistema se realizó
usando Celery, así que si quieres usar esa funcionalidad hay
unos pasos mas...

Primero es conveniente iniciar Redis (backend de datos/comunicación), y
luego iniciar Celery desde el entorno virtual de python.

Abre un terminal y ejecuta el servidor de redis::

    redis-server

Luego, desde otro terminal podrías ingresar en el entorno
virtual y lanzar Celery::

    workon flaskpastillas
    python manage.py celeryd


Ejecutar la aplicación en modo producción
-----------------------------------------

Hay que ingresar en el entorno y luego abrir
greenunicorn::

    workon flaskpastillas
    ~/.virtualenvs/flaskpastillas/bin/gunicorn app:app -b 0.0.0.0:8000

Ten en cuenta que existe un parámetro ``-D`` para correr este
comando como ``daemon``, y luego hay otro comando llamado
``gunicorn-console`` para monitorizar los procesos.

Por ejemplo::
    
    ~/.virtualenvs/flaskpastillas/bin/gunicorn app:app -b 0.0.0.0:8000
    ~/.virtualenvs/flaskpastillas/bin/gunicorn-console

