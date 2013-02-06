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
        return "<h5>%s</h5>" %(self.titulo)

class Agregar(TextField):

    def __init__(self, *k, **kv):
        TextField.__init__(self, *k, **kv)

    def __call__(self):
        return "<button id='%s' class='agregar btn' type='submit'>+</button>" %(self.id)

class AbortoAnterior(Form):
    aborto_anterior = SelectField(u"Aborto anterior", choices=data.ABORTO_ANTERIOR, coerce=int)
    observaciones = TextField(u"Observaciones")

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(AbortoAnterior, self).__init__(*args, **kwargs)

class InformacionIncorrecta(Form):
    medio = SelectField(u"Medio", choices=data.MEDIO_INFORMACION_INCORRECTA, coerce=int)
    detalle = TextField(u"Detalle")

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(InformacionIncorrecta, self).__init__(*args, **kwargs)

class IntentoDeAborto(Form):
    metodo = SelectField(u"Metodo", choices=data.METODO_INTENTO_DE_ABORTO, coerce=int)
    hace_cuantos_dias = TextField(u"¿Hace cuantos días?")
    miso = SelectField(u"Misoprostol", choices=data.MOTIVO_MAS_DE_10_SEMANAS, coerce=int)
    cantidad_de_pastillas = TextField(u"Cantidad de pastillas")
    precio = TextField("Edad gestacional")
    costo_si_no_es_miso = TextField(u"Costo total si no es misoprostol")
    sangrado = SelectField(u"Sangrado", choices=data.SANGRADO_INTENTO_ABORTO, coerce=int)
    sangrado_actual = SelectField(u"Sangrado actual", choices=data.SANGRADO_INTENTO_ABORTO, coerce=int)
    signos_de_infeccion = BooleanField(u"Signos de infección")

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(IntentoDeAborto, self).__init__(*args, **kwargs)

class DatosBaseForm(Form):
    nombre = TextField("Nombre")
    edad = DecimalField("Edad")
    telefono = TextField("Telefono")
    nacionalidad = TextField("Nacionalidad")

    separador = Separador("", titulo=u"Dirección")
    provincia = ModelSelectField("Provincia", model=models.Provincia)
    localidad = TextField("Localidad")
    barrio = SelectField("Barrio", choices=data.BARRIOS, coerce=int)

class LlamadaForm(Form):
    s1 = Separador("", titulo="Semanas Gestacionales")

    motivo = SelectField("Motivo", choices=data.MOTIVO, coerce=int)
    reconfirmo_embarazo = SelectField(u"Reconfirmó embarazo", choices=data.RECONFIRMO, coerce=int)
    fum = DateField("FUM", format='%d/%m/%Y')
    edad_gestacional = IntegerField("Edad gestacional")
    semana_entero = IntegerField(u"En qué semana se enteró")
    motivo_mas_de_10_semanas = SelectField(u"Más de 10 semanas",
                                           choices=data.MOTIVO_MAS_DE_10_SEMANAS, coerce=int)
    cantidad_de_hijos = IntegerField()

    datosbase_id = HiddenField("")

    # CAMPOS NUEVOS
    s2 = Separador("", titulo=u"Atención médica")
    fue_al_medico = SelectField(u"Fué al médico", choices=data.FUE_AL_MEDICO, coerce=int)
    frases_buenas_malas_practicas = TextField(u"Frases buenas, malas prácticas")
    tipo_de_servicio = SelectField(u"Tipo de servicio", choices=data.TIPO_DE_SERVICIO, coerce=int)
    obra_social = SelectField(u"Obra social", choices=data.OBRA_SOCIAL, coerce=int)
    compania = SelectField(u"Compañia", choices=data.COMPANIA, coerce=int)

    mac = SelectField(u"Método anticonceptivo", choices=data.METODO_ANTICONCEPTIVO, coerce=int)
    ahe = SelectField(u"AHE", choices=data.AHE, coerce=int)

    s3 = Separador("", titulo=u"¿Cómo se enteró de la linea?")

    # FALTA CORREGIR CHOICES
    entero_medio = SelectField(u"Medio", choices=data.MEDIO_COMO_SE_ENTERO, coerce=int)
    tiene_manual = BooleanField(u"¿Tiene el manual?")


    s4 = Separador("", titulo=u"Abortos anteriores")
    aborto_anterior = FieldList(FormField(AbortoAnterior), min_entries=1)
    submit = Agregar("", id='agregar_aborto_anterior')

    s5 = Separador("", titulo=u"Información incorrecta")
    informacion_incorrecta = FieldList(FormField(InformacionIncorrecta), min_entries=1)
    submit2 = Agregar("", id='agregar_informacion_incorrecta')

    s6 = Separador("", titulo=u"Intentos de aborto")
    intento_de_aborto = FieldList(FormField(IntentoDeAborto), min_entries=1)
    submit3 = Agregar("", id='agregar_intento_de_aborto')

    s7 = Separador("", titulo=u"Derivación")
    derivacion = TextField(u"Derivación")
    motivo_derivacion = SelectField(u"Motivo de la derivación", choices=data.MOTIVO_DERIVACION, coerce=int)
    observaciones = TextField(u"Observaciones")
