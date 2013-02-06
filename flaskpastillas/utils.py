
class Progreso:
    "Representa el progreso de una tarea de celery."

    def __init__(self, total):
        self.correctos = 0
        self.incorrectos = 0
        self.total =  total

    def como_diccionario(self):
        return {"procesados": self.procesados(),
                "correctos": self.correctos,
                "incorrectos": self.incorrectos,
                "total": self.total}

    def procesados(self):
        return self.correctos + self.incorrectos
