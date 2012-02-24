import unittest
import os
import app
import unittest
import tempfile
import config
import deploy

from pyquery import PyQuery as pq


class TestAcceso(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_exite_primer_opcion_en_el_menu(self):
        rv = self.app.get('/')
        d = pq(rv.data)
        assert 'Principal' in d(".tabs li:first").html()

    def test_puede_crear_llamada(self):
        rv = self.app.get('/llamada/crear')
        d = pq(rv.data)
        assert 'Cargar una llamada' in rv.data
       


class TestModelo(unittest.TestCase):

    def test_guardar_datos_base(self):
        from models import DatosBase

        datos = DatosBase(nombre='ejemplo')
        datos.save()
        assert datos.id
        assert DatosBase.select().where(nombre="ejemplo").count()

if __name__ == '__main__':
    deploy.crear_tablas()
    unittest.main()
