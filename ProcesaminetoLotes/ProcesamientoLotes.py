from validaciones import *
from prettytable import PrettyTable
import time


class Proceso:
    def __init__(self, id_programa, nombre_programador, operacion, operandos, tiempo_estimado, numero_lote):
        self.id_programa = id_programa
        self.nombre_programador = nombre_programador
        self.operacion = operacion
        self.operandos = operandos
        self.tiempo_estimado = tiempo_estimado
        self.tiempo_transcurrido = 0
        self.resultado = None
        self.numero_lote = numero_lote  # Añadido para almacenar el número de lote

    def ejecutar(self):
        if self.operacion == '+':
            self.resultado = self.operandos[0] + self.operandos[1]
        elif self.operacion == '-':
            self.resultado = self.operandos[0] - self.operandos[1]
        elif self.operacion == '*':
            self.resultado = self.operandos[0] * self.operandos[1]
        elif self.operacion == '/':
            if self.operandos[1] != 0:
                self.resultado = self.operandos[0] / self.operandos[1]
            else:
                self.resultado = 'Error: División entre 0'
        elif self.operacion == '%':
            self.resultado = self.operandos[0] % self.operandos[1]

    def __str__(self):
        return f"ID Programa: {self.id_programa}, Programador: {self.nombre_programador}, Operación: {self.operacion} {self.operandos[0]}, {self.operandos[1]}, Tiempo Estimado: {self.tiempo_estimado}"


class Lote:
    def __init__(self, procesos, numero_lote):
        self.procesos = procesos
        self.numero_lote = numero_lote

    def __str__(self):
        return "\n".join(str(p) for p in self.procesos)


def crear_lotes(procesos, capacidad=5):
    lotes = []
    for i in range(0, len(procesos), capacidad):
        lotes.append(Lote(procesos[i:i + capacidad], len(lotes) + 1))
    return lotes


def ejecutar_procesos(lotes):
    global_clock = 0
    lotes_pendientes = len(lotes)
    procesos_terminados = []

    # Crear tabla para procesos en ejecución
    tabla_ejecucion = PrettyTable()
    tabla_ejecucion.field_names = ["Número de Lote", "ID Programa", "Programador", "Operación", "Tiempo Estimado",
                                   "Tiempo Transcurrido"]

    while lotes:
        lote_actual = lotes.pop(0)
        print(f"\nLote en ejecución: {lote_actual.numero_lote}")
        print(f"Lotes pendientes: {lotes_pendientes - 1}")

        for proceso in lote_actual.procesos:
            print(f"\nProceso en ejecución: {proceso}")

            for t in range(proceso.tiempo_estimado):
                proceso.tiempo_transcurrido += 1
                global_clock += 1
                time.sleep(1)  # Simula el tiempo transcurrido
                print(f"Tiempo transcurrido: {proceso.tiempo_transcurrido} / {proceso.tiempo_estimado}")

                # Actualizar tabla de ejecución
                tabla_ejecucion.clear_rows()
                for p in lote_actual.procesos:
                    tabla_ejecucion.add_row(
                        [lote_actual.numero_lote, p.id_programa, p.nombre_programador, p.operacion, p.tiempo_estimado,
                         p.tiempo_transcurrido])

                # Mostrar tabla de procesos en ejecución actualizada
                print(tabla_ejecucion)

            proceso.ejecutar()
            procesos_terminados.append(proceso)  # Almacenar el proceso terminado
            print(f"Proceso terminado. Resultado: {proceso.resultado}")

        lotes_pendientes -= 1
        print("\nFin de lote.")


    # Mostrar tabla de procesos terminados
    tabla_terminados = PrettyTable()
    tabla_terminados.field_names = ["Número de Lote", "ID Programa", "Programador", "Operación", "Resultado"]

    for p in procesos_terminados:
        tabla_terminados.add_row(
            [p.numero_lote, p.id_programa, p.nombre_programador, f"{p.operacion} {p.operandos[0]}, {p.operandos[1]}",
             p.resultado])

    print("\nTabla de procesos terminados:")
    print(tabla_terminados)

    print(f"\nSimulación terminada. Tiempo global: {global_clock} segundos.")
    input("Presiona Enter para cerrar...")
7

def capturar_procesos():
    procesos = []
    print("Introduce el número de procesos: ")
    num_procesos = solicitar_numero()
    ids = set()
    limpiar_pantalla()

    for i in range(num_procesos):
        print(f"Introduce el ID del programa {i + 1}: ")
        id_programa = solicitar_numero()
        while id_programa in ids:
            print("ID duplicado, por favor introduce un ID único.")
            print(f"Introduce el ID del programa {i + 1}: ")
            id_programa = solicitar_numero()
        ids.add(id_programa)

        print("Introduce el nombre del programador: ")
        nombre_programador = solicitar_cadena()

        print("Introduce la operación (+, -, *, /, %): ")
        operacion = solicitar_opernado()

        print("Introduce el primer operando: ")
        op1 = solicitar_digito()
        print("Introduce el segundo operando: ")
        op2 = solicitar_digito(operacion)
        operandos = [op1, op2]

        print("Introduce el tiempo máximo estimado (mayor a 0): ")
        tiempo_estimado = solicitar_numero()

        # Crear el proceso, pasando el número de lote (temporariamente se pasará None, será asignado luego)
        proceso = Proceso(id_programa, nombre_programador, operacion, operandos, tiempo_estimado, None)
        procesos.append(proceso)

        limpiar_pantalla()

    return procesos


def main():
    procesos = capturar_procesos()
    lotes = crear_lotes(procesos)
    # Asignar el número de lote a cada proceso
    for numero_lote, lote in enumerate(lotes, start=1):
        for proceso in lote.procesos:
            proceso.numero_lote = numero_lote  # Asignar número de lote al proceso

    ejecutar_procesos(lotes)


if __name__ == "__main__":
    main()
