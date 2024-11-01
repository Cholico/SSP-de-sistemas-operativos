# proceso.py

class Proceso:
    def __init__(self, id:int, tiempo_estimado, operacion, operandos):
        self.id = id
        self.tiempo_estimado = tiempo_estimado
        self.tiempo_transcurrido = 0
        self.estado = "Nuevo"
        self.operacion = operacion
        self.operandos = operandos
        self.resultado = None
        self.tiempo_llegada = None
        self.tiempo_finalizacion = None
        self.tiempo_respuesta = None
        self.tiempo_espera = 0
        self.tiempo_servicio = 0
        self.tiempo_retorno = 0
        self.hora_comienzo_ejecucion = None
        self.bloqueado_tiempo = 0
        self.contador = 0

    def ejecutar(self):
        try:
            if self.operacion == '+':
                resultado = self.operandos[0] + self.operandos[1]
            elif self.operacion == '-':
                resultado = self.operandos[0] - self.operandos[1]
            elif self.operacion == '*':
                resultado = self.operandos[0] * self.operandos[1]
            elif self.operacion == '/':
                resultado = round(self.operandos[0] / self.operandos[1], 2) if self.operandos[
                                                                         1] != 0 else "Error: División por cero"
            elif self.operacion == '%':
                resultado = round(self.operandos[0] % self.operandos[1], 2)
            return resultado
        except Exception as e:
            return f"Error: {str(e)}"

    def __repr__(self):
        return f"{self.id}"




