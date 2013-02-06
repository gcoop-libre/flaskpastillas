# -*- encoding: utf-8 -*-
import xlrd
import xlwt
import models
import datetime
import time

class ArchivoErrores:
    """
    Representa un achivo Excel con los datos erroneos detectados
    en la importación de datos.
    """

    def __init__(self, ruta):
        self.fila = 3
        self.ruta = ruta
        self.archivo = xlwt.Workbook()
        self.hoja = self.archivo.add_sheet('sheet1', cell_overwrite_ok=True)

    def guardar(self, elementos):
        "Guarda una fila completa de datos y avanza el puntero de escritura."
        for i, v in enumerate(elementos):
            self.hoja.write(self.fila, i, v)

        self.fila += 1

    def cerrar(self):
        "Cierra el archivo y vuelca los datos en el disco."
        self.archivo.save(self.ruta)

class Importador:
    """
    Representa la tarea de importación de registros.

    El objeto importador se inicializa con la ruta del archivo excel que
    tiene que procesar y opcionalmente recibe un parámetro para simular
    una demora en la importación. Esta demora es útil para realizar pruebas
    solamente.

    Una vez inicializado el importador, se tiene que llamar al método
    ``procesar_registro`` y este procesa la fila actual. Cada vez que
    se usa al importador, el puntero que señala la fila actual avanza. Así
    que se puede pensar en el importador cómo usa suerte de iterador.
    """

    def __init__(self, archivo_a_procesar, ruta_archivo_errores, demora=0):
        try:
            self.documento = xlrd.open_workbook(archivo_a_procesar)
        except xlrd.biffh.XLRDError:
            raise Exception("Solo se admiten archivos xls con formato excel 2000/XP/2003")

        # Obtienen la hora principal del documento.
        self.hoja = self.documento.sheet_by_index(0)
        # Define la primer fila a procesar. Las primeras filas son cabeceras.
        self.numero_de_fila = 3
        self.total = self._contar_filas() - self.numero_de_fila
        self.fecha_anterior = None
        self.demora = demora
        self.errores = 0

        self.archivo_errores = ArchivoErrores(ruta_archivo_errores)


    def _contar_filas(self):
        "Retorna la cantidad de filas utilizandas dentro del archivo excel."
        i = 0

        while True:
            fila = self.hoja.row_values(i)
            if not fila[0]:
                return i
            i += 1

    def obtener_fila_actual(self):
        "Retorna una tupla con todos los valores en la fila actual."
        return self.hoja.row_values(self.numero_de_fila)

    def _procesar(self):
        """
        Procesa todas las celdas de una sola fila del archivo excel.

        La fila que se va a procesar depende del atributo ``numero_de_fila``, y
        este atributo no se increamenta aquí.
        """

        fila = self.obtener_fila_actual()

        datos_base = models.DatosBase()
        datos_base.numero_de_ficha = self.numero(fila[0])

        # En caso de que no exista la descripcion de la fecha, se asume que
        # la fecha es la misma de la llamada anterior.
        if fila[2]:
            datos_base.fecha = self.fecha(fila[2])
            self.fecha_anterior = datos_base.fecha
        else:
            datos_base.fecha = self.fecha_anterior

        datos_base.telefono = self.numero(fila[3])
        datos_base.nombre = fila[4]
        datos_base.edad = self.numero(fila[5])
        datos_base.localidad = self.cadena_ascii(fila[6])

        codigo_provincia = self.numero(fila[7], 99)
        datos_base.provincia_id = models.Provincia.get(codigo=codigo_provincia).id

        datos_base.barrio = str(fila[8])
        datos_base.nacionalidad = str(fila[9])

        datos_base.save()

        # Primer Llamado
        # --------------
        llamada = models.Llamada()
        llamada.datosbase_id = datos_base.id

        # En caso de que no exista la descripcion de la fecha, se asume que
        # la fecha es la misma de la llamada anterior.
        if fila[2]:
            llamada.fecha = self.fecha(fila[2])
        else:
            llamada.fecha = self.fecha_anterior


        # Semanas gestacionales
        llamada.motivo = self.numero(fila[10])
        llamada.reconfirmo_embarazo = self.numero(fila[11], 0)
        llamada.metodo_comprobacion = self.numero(fila[12])
        llamada.fum = self.fecha(fila[13], default=datetime.datetime.now())
        llamada.edad_gestacional = self.numero(fila[14])
        llamada.motivo_mas_de_10_semanas = self.numero(fila[15])
        llamada.semana_entero = self.numero(fila[16])

        # Cantidad de hijos
        llamada.cantidad_de_hijos = self.numero(fila[17])

        # Atención médica
        llamada.fue_al_medico = self.numero(fila[18])
        llamada.frases_buenas_malas_practicas = self.cadena_ascii(fila[20])
        llamada.tipo_de_servicio = self.numero(fila[21])
        llamada.obra_social = self.numero(fila[22])

        # Compania
        llamada.compania = self.numero(fila[23])

        # Se guarda la llamada para vincularla con los registros de aborto
        # anterior que siguen.
        llamada.save()

        # Aborto anterior 1
        if fila[24]:
            self.crear_aborto_anterior(fila, 24, llamada)

        # Aborto anterior 2
        if fila[26]:
            self.crear_aborto_anterior(fila, 26, llamada)

        # Aborto anterior 3
        if fila[28]:
            self.crear_aborto_anterior(fila, 28, llamada)

        # Aborto anterior 4
        if fila[30]:
            self.crear_aborto_anterior(fila, 30, llamada)


        # MAC y AHE (Método Anticonceptivo)
        llamada.mac = self.numero(fila[32])
        llamada.ahe = self.numero(fila[33])

        # Cómo se entero de la linea
        llamada.entero_medio = self.numero(fila[34])

        # Información incorrecta: 1
        if fila[37]:
            self.crear_informacion_incorrecta(llamada, fila, 37)

        # Información incorrecta: 2
        if fila[38]:
            self.crear_informacion_incorrecta(llamada, fila, 39)

        # TODO: col 42
        # TODO: col 43
        # TODO: col 44
        # TODO: col 45

        # Si tiene el manual
        llamada.tiene_manual = self.numero(fila[41])

        # Primer intento de aborto
        if fila[46]:
            self.crear_intento_de_aborto(llamada, fila, 46)

        # Segundo intento de aborto
        if fila[57]:
            self.crear_intento_de_aborto(llamada, fila, 57)

        # Tercer intento de aborto
        if fila[68]:
            self.crear_intento_de_aborto(llamada, fila, 68)

        # Cuarto intento de aborto
        if fila[79]:
            self.crear_intento_de_aborto(llamada, fila, 79)

        # TODO: col 90 (gasto total en posaborto).

        # Derivación (con motivo)
        llamada.derivacion = self.cadena(fila[91])
        llamada.motivo_derivacion = self.numero(fila[92], 99)

        llamada.save()

        # Observaciones de la llamada.
        llamada.observaciones = self.cadena_ascii(fila[234])
        llamada.save()

        # Genera las llamadas desde la segunda a la sexta (inclusive).
        self.crear_llamada_reducida(fila, datos_base, 94, 2)
        self.crear_llamada_reducida(fila, datos_base, 94, 3)
        self.crear_llamada_reducida(fila, datos_base, 94, 4)
        self.crear_llamada_reducida(fila, datos_base, 94, 5)
        self.crear_llamada_reducida(fila, datos_base, 94, 6)

    def crear_llamada_reducida(self, fila, datos_base, i, numero_llamada):
        llamada = models.Llamada()
        llamada.datosbase_id = datos_base.id

        if fila[i]:
            llamada.fecha = self.fecha(fila[i])

        # TODO: Esta columna falta en la segunda,tercera, cuarta, quita y sexta llamada...
        llamada.fum = self.fecha(fila[13], default=datetime.datetime.now())

        llamada.edad_gestacional = self.numero(fila[i+1])
        llamada.motivo = self.numero(fila[i+2])
        llamada.reconfirmo_embarazo = self.numero(fila[i+3], 0)

        # Atención médica (segundo llamada)
        llamada.fue_al_medico = self.numero(fila[i+4])
        llamada.frases_buenas_malas_practicas = self.cadena_ascii(fila[i+6])
        llamada.tipo_de_servicio = self.numero(fila[i+7])

        # TODO: falta la columna de obra social de la segunda llamada!

        # Se guarda la segunda llamada para procesar los intentos de aborto.
        llamada.save()

        # Primer intento de aborto (segunda llamada)
        if fila[i+13]:
            self.crear_intento_de_aborto(llamada, fila, i+13)

        # Segundo intento de aborto (segunda llamada)
        if fila[i+24]:
            self.crear_intento_de_aborto(llamada, fila, i+24)

        # Derivación (con motivo, de la segunda llamada)
        llamada.derivacion = self.cadena(fila[i+34])
        llamada.motivo_derivacion = self.numero(fila[i+35], 99)

        # Fin de la segunda llamada
        llamada.save()

    def __deprecated(self):
        # Segunda llamada
        # ---------------
        llamada = models.Llamada()
        llamada.datosbase_id = datos_base.id

        if fila[94]:
            llamada.fecha = self.fecha(fila[94])

        # TODO: Esta columna falta en la segunda llamada...
        llamada.fum = self.fecha(fila[13], default=datetime.datetime.now())

        llamada.edad_gestacional = self.numero(fila[95])
        llamada.motivo = self.numero(fila[96])
        llamada.reconfirmo_embarazo = self.numero(fila[97], 0)

        # Atención médica (segundo llamada)
        llamada.fue_al_medico = self.numero(fila[98])
        llamada.frases_buenas_malas_practicas = self.cadena_ascii(fila[100])
        llamada.tipo_de_servicio = self.numero(fila[101])

        # TODO: falta la columna de obra social de la segunda llamada!

        # Se guarda la segunda llamada para procesar los intentos de aborto.
        llamada.save()

        # Primer intento de aborto (segunda llamada)
        if fila[107]:
            self.crear_intento_de_aborto(llamada, fila, 107)

        # Segundo intento de aborto (segunda llamada)
        if fila[118]:
            self.crear_intento_de_aborto(llamada, fila, 118)

        # Derivación (con motivo, de la segunda llamada)
        llamada.derivacion = self.cadena(fila[128])
        llamada.motivo_derivacion = self.numero(fila[129], 99)

        # Fin de la segunda llamada
        llamada.save()

        # Tercer llamada
        # ---------------
        llamada = models.Llamada()
        llamada.datosbase_id = datos_base.id

        if fila[131]:
            llamada.fecha = self.fecha(fila[131])

        # TODO: Esta columna falta en la segunda llamada...
        llamada.fum = self.fecha(fila[13], default=datetime.datetime.now())

        llamada.edad_gestacional = self.numero(fila[132])
        llamada.motivo = self.numero(fila[133])
        llamada.reconfirmo_embarazo = self.numero(fila[134], 0)

        # Atención médica (segundo llamada)
        llamada.fue_al_medico = self.numero(fila[135])
        llamada.frases_buenas_malas_practicas = self.cadena_ascii(fila[136])
        llamada.tipo_de_servicio = self.numero(fila[137])

        # TODO: falta la columna de obra social de la segunda llamada!

        # Se guarda la segunda llamada para procesar los intentos de aborto.
        llamada.save()

        # Primer intento de aborto (segunda llamada)
        if fila[143]:
            self.crear_intento_de_aborto(llamada, fila, 143)

        # Segundo intento de aborto (segunda llamada)
        if fila[156]:
            self.crear_intento_de_aborto(llamada, fila, 156)

        # Derivación (con motivo, de la segunda llamada)
        llamada.derivacion = self.cadena(fila[154])
        llamada.motivo_derivacion = self.numero(fila[155], 99)

        # Fin de la segunda llamada
        llamada.save()


    def crear_aborto_anterior(self, fila, indice, llamada):
        ab = models.AbortoAnterior()
        ab.llamada = llamada
        ab.medio = self.numero(fila[indice])
        ab.observaciones = self.cadena_ascii(fila[indice + 1])
        ab.save()

    def crear_informacion_incorrecta(self, llamada, fila, inicial):
        info1 = models.InformacionIncorrecta()
        info1.llamada = llamada
        info1.medio = fila[inicial]
        info1.detalle = fila[inicial + 1]
        info1.save()

    def crear_intento_de_aborto(self, llamada, fila, indice):
        r = models.IntentoDeAborto()
        r.llamada = llamada
        r.metodo = fila[indice + 1]
        r.hace_cuantos_dias = fila[indice + 2]
        r.miso = fila[indice + 3]
        r.precio = fila[indice + 4]
        r.cantidad_de_pastillas = fila[indice + 5]

        r.costo_si_no_es_miso = fila[indice + 7]
        r.sangrado = fila[indice + 8]
        r.sangrado_actual = fila[indice + 9]
        r.signos_de_infeccion = fila[indice + 10]

        r.save()

    def procesar_registro(self, progreso):
        """Procesa la fila de actual del archivo excel y avanza el puntero de lectura.

        Este método representa una iteración del importador. En una
        ejecución normal, este método se tiene que llamar tantas veces
        cómo cantidad de filas se quieran procesar.
        """
        try:
            self._procesar()
            progreso.correctos += 1
        except Exception as e:
            print e
            print self.obtener_fila_actual()
            self.archivo_errores.guardar(self.obtener_fila_actual())
            progreso.incorrectos += 1

        self.numero_de_fila += 1

        if self.demora:
            time.sleep(self.demora)


    def numero(self, valor, default=0):
        "Convierte un valor de tipo cadena en un numero base 10."
        if not valor:
            return default

        return str(int(valor))

    def cadena(self, valor):
        return str(valor)

    def cadena_ascii(self, valor):
        return str(repr(valor)).replace("u'", "").replace("'", "")

    def cadena_utf(self, valor):
        return valor

    def fecha(self, valor, datemode=0, default=None):
        "Convierte un campo de tipo cadena en una fecha."
        # datemode: 0 for 1900-based, 1 for 1904-based
        try:
            return (datetime.datetime(1899, 12, 30) + datetime.timedelta(days=valor + 1462 * datemode))
        except TypeError as e:
            if default is not None:
                return default
            else:
                raise e


    def guardar_archivo_de_errores(self):
        self.archivo_errores.cerrar()

if __name__ == '__main__':
    import deploy
    deploy.crear_tablas()
    importador = Importador('test/data/ENERO_original.xls', '/tmp/123')

    for x in range(importador.total):
        importador._procesar()
        importador.numero_de_fila += 1
