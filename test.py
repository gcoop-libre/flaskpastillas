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

    def test_puede_listar_llamadas(self):
        rv = self.app.get('/llamada')
        assert 'Llamada' in rv.data

class TestModelo(unittest.TestCase):

    def setUp(self):
        from models import DatosBase, Provincia
        DatosBase.drop_table()
        DatosBase.create_table()

    def test_guardar_datos_base(self):
        from models import DatosBase, Provincia

        datos = DatosBase(nombre='ejemplo')
        datos.provincia = Provincia.get(id=10)
        datos.save()
        assert datos.id
        assert DatosBase.select().where(nombre="ejemplo").count()

    def test_estan_las_provincias(self):
        from models import Provincia

        assert Provincia.select().where(nombre='BUENOS AIRES').count()

    def test_contar_llamadas_por_provincias(self):
        from models import Provincia, DatosBase

        for p in Provincia.select():
            assert p.llamadas.count() == 0

        datos = DatosBase(nombre='ejemplo')
        datos.provincia = Provincia.get(id=10)
        datos.save()

        p1 = Provincia.get(id=10)
        assert p1.llamadas.count() == 1





if __name__ == '__main__':
    deploy.crear_tablas()
    unittest.main()
