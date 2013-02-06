# -*- encoding: utf-8 -*-
import datetime
from peewee import *
from app import db

from peewee import SelectQuery

class Modelo(db.Model):
    """Representa un modelo que se puede cargar desde un formulario.

    Este método va a tratar de usar la intefaz del modelo para
    asociar los campos. Así que si tu formulario es complejo
    y tiene que tratar los datos antes de procesarlos, podría
    utilizar properties.
    """

    def cargar(self, form):
        datos = form.data

        for (clave, valor) in datos.items():
            setattr(self, clave, valor)

        self.save()
        self.guardar_relaciones()

    def cantidad_llamadas(self):
        return self.llamadas.count()

    def guardar_relaciones(self):
        pass


class Provincia(db.Model):
    codigo = IntegerField()
    nombre = CharField()

    def __unicode__(self):
        return "%s (%s)" %(self.nombre, self.codigo)

    @staticmethod
    def obtener_por_codigo(self, codigo):
        import pdb
        pdb.set_trace()
        pass

class DatosBase(Modelo):
    numero_de_ficha = IntegerField()
    fecha = DateTimeField(default=datetime.datetime.now)
    telefono = CharField()
    nombre = CharField()
    edad = IntegerField(null=True)
    provincia = ForeignKeyField(Provincia, related_name='datos_base')
    barrio = IntegerField()
    nacionalidad = CharField()
    localidad = CharField()

    def __unicode__(self):
        return self.nombre

class Llamada(Modelo):
    datosbase = ForeignKeyField(DatosBase, related_name='llamadas')
    fecha = DateTimeField(default=datetime.datetime.now)
    motivo = IntegerField()
    reconfirmo_embarazo = IntegerField()
    metodo_comprobacion = IntegerField()
    fum = DateTimeField()
    edad_gestacional = IntegerField()
    motivo_mas_de_10_semanas = IntegerField()
    semana_entero = IntegerField()
    cantidad_de_hijos = IntegerField()

    fue_al_medico = IntegerField()
    frases_buenas_malas_practicas = CharField()

    tipo_de_servicio = IntegerField()
    obra_social = IntegerField()
    compania = IntegerField()

    entero_medio = IntegerField()
    tiene_manual = BooleanField()

    derivacion = CharField()
    motivo_derivacion = IntegerField()
    observaciones = CharField()

    mac = IntegerField()
    ahe = IntegerField()

    def set_datosbase_id(self, valor):
        self.datosbase = DatosBase.get(id=valor)

    datosbase_id = property(fset=set_datosbase_id)

    def save(self):
        # Repara el bug del manejo de fechas.
        if type(self.fum) == datetime.date:
            self.fum = datetime.datetime(self.fum.year, self.fum.month, self.fum.day)

        Modelo.save(self)

    def guardar_relaciones(self):
        for x in self.lista_aborto_anterior + self.lista_intento_de_aborto + self.lista_informacion_incorrecta:
            x.llamada = self
            x.save()

    def set_aborto_anterior(self, value):
        self.lista_aborto_anterior = []
        for item in value:
            aborto_anterior = AbortoAnterior()
            aborto_anterior.observaciones = item['observaciones']
            aborto_anterior.aborto_anterior = item['aborto_anterior']
            self.lista_aborto_anterior.append(aborto_anterior)

    def set_intento_de_aborto(self, value):
        self.lista_intento_de_aborto = []

        for item in value:
            ia = IntentoDeAborto()
            ia.metodo = item['metodo']
            ia.hace_cuantos_dias = item['hace_cuantos_dias']
            ia.miso = item['miso']
            ia.cantidad_de_pastillas = item['cantidad_de_pastillas']
            ia.precio = item['precio']
            ia.costo_si_no_es_miso = item['costo_si_no_es_miso']
            ia.sangrado = item['sangrado']
            ia.sangrado_actual = item['sangrado_actual']
            ia.signos_de_infeccion = item['signos_de_infeccion']

            self.lista_intento_de_aborto.append(ia)

    def set_informacion_incorrecta(self, value):
        self.lista_informacion_incorrecta = []

        for item in value:
            ii = InformacionIncorrecta()
            ii.medio = item['medio']
            ii.detalle = item['detalle']
            self.lista_informacion_incorrecta.append(ii)

    aborto_anterior = property(fset=set_aborto_anterior)
    intento_de_aborto = property(fset=set_intento_de_aborto)
    informacion_incorrecta = property(fset=set_informacion_incorrecta)

    def __unicode__(self):
        return "Llamada de %s (el %s)" %(self.datosbase.nombre, self.fecha)


class AbortoAnterior(Modelo):
    llamada = ForeignKeyField(Llamada, related_name='lista_aborto_anterior')
    aborto_anterior = IntegerField()
    observaciones = CharField()

class InformacionIncorrecta(Modelo):
    llamada = ForeignKeyField(Llamada, related_name='lista_informacion_incorrecta')
    medio = IntegerField()
    detalle = CharField()

class IntentoDeAborto(Modelo):
    llamada = ForeignKeyField(Llamada, related_name='lista_intento_de_aborto')
    metodo = IntegerField()
    hace_cuantos_dias = IntegerField()
    miso = IntegerField()
    cantidad_de_pastillas = IntegerField()
    precio = IntegerField()
    costo_si_no_es_miso = IntegerField()
    sangrado = IntegerField()
    sangrado_actual = IntegerField()
    signos_de_infeccion = BooleanField()
