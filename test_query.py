import models

for x in models.DatosBase.select().group_by('provincia_id'):
    pass #print x

#print str([[x.nombre, x.datos_base.count()] for x in models.Provincia.select()])

# Edades de las personas que me llaman.
edades = [p.edad for p in models.DatosBase.select().group_by('edad')]
edades.sort()
print edades

for edad in edades:
    print edad, models.DatosBase.select().where(edad=edad).count()
