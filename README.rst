Instalación
-----------

Para realizar la instalación necesitamos crear un entorno e instalar
todas las bibliotecas para flask.

::

    mkvirtualenv flaskpastillas
    workon flaskpastillas
    pip install -r requirements.txt


Es una *muy* buena idea usar ipython adentro del virtualenv. Este link explica
cómo hacerlo:

    http://www.ahmedsoliman.com/2011/09/27/use-virtualenv-with-ipython-0-11/

Ejecutar la aplicación
----------------------

Primero hay que entrar en el entorno, y luego
lanzar del servidor de prueba::

    workon flaskpastillas
    python app.py
