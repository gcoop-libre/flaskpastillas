import unittest
import os
import app
import unittest
import tempfile
import config

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
        


if __name__ == '__main__':
    unittest.main()
