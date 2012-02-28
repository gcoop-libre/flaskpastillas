from flaskext.wtf import *
import models
from wtfpeewee.fields import ModelSelectField


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

class DatosBaseForm(Form):
    nombre = TextField("Nombre")
    edad = DecimalField("Edad")
    #provincia = SelectField("Provincia", choices=[(1, 'asd'), (2, 'dasd')])
    provincia = ModelSelectField("Provincia", model=models.Provincia)

    #canciones = FieldList(FormField(CancionForm))
    #submit = SubmitField("Agregar")

