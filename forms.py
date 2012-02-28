# -*- encoding: utf-8 -*-
from flaskext.wtf import *
import models
from wtfpeewee.fields import ModelSelectField
import data

class Separador(TextField):

    def __init__(self, *k, **kv):
        self.titulo = kv.pop('titulo')
        TextField.__init__(self, *k, **kv)

    def __call__(self):
        return "<strong>%s</strong>" %(self.titulo)

class DatosBaseForm(Form):
    nombre = TextField("Nombre")
    edad = DecimalField("Edad")
    telefono = TextField("Telefono")
    nacionalidad = TextField("Nacionalidad")

    separador = Separador("", titulo=u"Dirección")
    provincia = ModelSelectField("Provincia", model=models.Provincia)
    localidad = TextField("Localidad")
    barrio = SelectField("Barrio", choices=data.BARRIOS, coerce=int)



    #fum = DateField("Fum", format='%d/%m/%Y')

    #canciones = FieldList(FormField(CancionForm))
    #submit = SubmitField("Agregar")

class LlamadaForm(Form):
    s = Separador("", titulo="Semanas Gestacionales")
    
    motivo = SelectField("Motivo", choices=data.MOTIVO, coerce=int)
    reconfirmo_embarazo = SelectField(u"Reconfirmó embarazo", choices=data.RECONFIRMO, coerce=int)
    fum = DateField("FUM", format='%d/%m/%Y')
    edad_gestacional = IntegerField("Edad gestacional")
    semana_entero = IntegerField(u"En qué semana se enteró")
    motivo_mas_de_10_semanas = SelectField(u"Más de 10 semanas",
                                           choices=data.MOTIVO_MAS_DE_10_SEMANAS, coerce=int)
    cantidad_de_hijos = IntegerField()

    datosbase_id = HiddenField("")
