from flaskext.wtf import *
import models
from wtfpeewee.fields import ModelSelectField
import data

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


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

    separador = Separador("", titulo="Direccion")
    provincia = ModelSelectField("Provincia", model=models.Provincia)
    localidad = TextField("Localidad")
    barrio = SelectField("Barrio", choices=data.BARRIOS, coerce=int)
    #fum = DateField("Fum", format='%d/%m/%Y')

    #canciones = FieldList(FormField(CancionForm))
    #submit = SubmitField("Agregar")

