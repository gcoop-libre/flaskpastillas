from flaskext.wtf import Form, TextField, DecimalField, TextField
from flaskext.wtf import FormField, FieldList, SubmitField


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

class DatosBaseForm(Form):
    nombre = TextField("Nombre")
    edad = DecimalField("Edad")
    #canciones = FieldList(FormField(CancionForm))
    #submit = SubmitField("Agregar")
