from flaskext.wtf import *
import models
from wtfpeewee.fields import ModelSelectField
import data

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

class DatosBaseForm(Form):
    nombre = TextField("Nombre")
    edad = DecimalField("Edad")
    telefono = TextField("Telefono")

    provincia = ModelSelectField("Provincia", model=models.Provincia)
    localidad = TextField("Localidad")

    barrio = SelectField("Barrio", choices=data.BARRIOS)
    nacionalidad = TextField("Nacionalidad")


    #canciones = FieldList(FormField(CancionForm))
    #submit = SubmitField("Agregar")

