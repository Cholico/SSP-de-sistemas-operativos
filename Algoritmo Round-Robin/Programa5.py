import random
import time
import keyboard
from prettytable import PrettyTable
from proceso import Proceso


class Simulador():
    def __init__(self, num_procesos, quantum):
        self.pausa = False
        self.interrupcion = False
        self.error = False
        self.nuevos = []
        self.listos = []
        self.bloqueados = []
        self.terminados = []
        self.num_procesos = num_procesos
        self.reloj = 0
        self.proceso_en_ejecucion = None
        self.quantum = quantum


    def mostrar_estado(self):
        print(f"Procesos en estado Nuevo: {len(self.nuevos)}")
        print(f'Quantum {self.quantum}')

        # Mostrar cola de listos
        print("\nCola de Listos:")
        if self.listos:
            tabla_listos = PrettyTable()
            tabla_listos.field_names = ["ID", "Tiempo Máximo Estimado", "Tiempo Transcurrido"]
            for proceso in self.listos:
                tabla_listos.add_row([proceso.id, proceso.tiempo_estimado, proceso.tiempo_transcurrido])
            print(tabla_listos)
        else:
            print("No hay procesos en la cola de listos.")

        # Mostrar proceso en ejecución
        if self.proceso_en_ejecucion:
            print(
                f"\nProceso en Ejecución: ID: {self.proceso_en_ejecucion.id}, Operación: {self.proceso_en_ejecucion.operacion}, "
                f"Operandos: {self.proceso_en_ejecucion.operandos}, Tiempo Transcurrido: {self.proceso_en_ejecucion.tiempo_transcurrido}, "
                f"Tiempo Restante: {self.proceso_en_ejecucion.tiempo_estimado - self.proceso_en_ejecucion.tiempo_transcurrido}")
        else:
            print("No hay proceso en ejecución.")

        # Mostrar cola de bloqueados
        print("\nCola de Bloqueados:")
        if self.bloqueados:
            tabla_bloqueados = PrettyTable()
            tabla_bloqueados.field_names = ["ID", "Tiempo Transcurrido en Bloqueado"]
            for proceso in self.bloqueados:
                tabla_bloqueados.add_row([proceso.id, proceso.bloqueado_tiempo])
            print(tabla_bloqueados)
        else:
            print("No hay procesos en la cola de bloqueados.")

        # Mostrar trabajos terminados
        print("\nTrabajos Terminados:")
        if self.terminados:
            tabla_terminados = PrettyTable()
            tabla_terminados.field_names = ["ID", "Operación", "Resultado"]
            for trabajo in self.terminados:
                resultado = "ERROR" if trabajo['error'] else trabajo['resultado']
                tabla_terminados.add_row([trabajo['proceso'].id, trabajo['operacion'], resultado])
            print(tabla_terminados)
        else:
            print("No hay trabajos terminados.")

        print(f"Reloj: {self.reloj}")
        print("-" * 50)

    def mostrar_tabla_bcp(self):
        # Crear tabla de estado detallado de cada proceso
        tabla = PrettyTable()
        tabla.field_names = [
            "ID", "Estado", "Operación", "Resultado", "Tiempo Llegada", "Tiempo Finalización",
            "Tiempo Retorno", "Tiempo Espera", "Tiempo Servicio", "Tiempo Restante CPU", "Tiempo Respuesta"
        ]

        # Función para formatear campos nulos
        def formatear_campo(valor):
            return valor if valor is not None else "N/A"

        # Procesos en estado "Nuevo"
        for proceso in self.nuevos:
            tabla.add_row([
                proceso.id, "Nuevo", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"
            ])

        # Procesos en estado "Listo"
        for proceso in self.listos:
            tabla.add_row([
                proceso.id, "Listo",
                f"{proceso.operandos[0]} {proceso.operacion} {proceso.operandos[1]}",
                "N/A", formatear_campo(proceso.tiempo_llegada), "N/A", "N/A",
                proceso.tiempo_espera, proceso.tiempo_transcurrido,
                "N/A", formatear_campo(proceso.tiempo_respuesta)
            ])

        # Proceso en estado "En Ejecución"
        if self.proceso_en_ejecucion:
            tiempo_restante = self.proceso_en_ejecucion.tiempo_estimado - self.proceso_en_ejecucion.tiempo_transcurrido
            tabla.add_row([
                self.proceso_en_ejecucion.id, "En Ejecución",
                f"{self.proceso_en_ejecucion.operandos[0]} {self.proceso_en_ejecucion.operacion} {self.proceso_en_ejecucion.operandos[1]}",
                "En Progreso", formatear_campo(self.proceso_en_ejecucion.tiempo_llegada),
                "N/A", "N/A", self.proceso_en_ejecucion.tiempo_espera,
                self.proceso_en_ejecucion.tiempo_transcurrido, tiempo_restante,
                formatear_campo(self.proceso_en_ejecucion.tiempo_respuesta)
            ])

        # Procesos en estado "Bloqueado"
        for proceso in self.bloqueados:
            tiempo_restante_bloqueado = 7 - proceso.bloqueado_tiempo  # Tiempo restante en el estado de bloqueado
            tabla.add_row([
                proceso.id, "Bloqueado",
                f"{proceso.operandos[0]} {proceso.operacion} {proceso.operandos[1]}",
                "N/A", formatear_campo(proceso.tiempo_llegada), "N/A", "N/A",
                proceso.tiempo_espera, proceso.tiempo_transcurrido,
                tiempo_restante_bloqueado, formatear_campo(proceso.tiempo_respuesta)
            ])

        # Procesos en estado "Terminado"
        for proceso in self.terminados:
            p = proceso['proceso']
            tabla.add_row([
                p.id, p.estado,
                p.operacion, proceso["resultado"],
                formatear_campo(p.tiempo_llegada),
                formatear_campo(p.tiempo_finalizacion),
                formatear_campo(p.tiempo_retorno),
                formatear_campo(p.tiempo_espera),
                formatear_campo(p.tiempo_servicio),
                "N/A", formatear_campo(p.tiempo_respuesta)
            ])

        # Mostrar la tabla en consola
        print(tabla)


    def generar_procesos(self, num) -> Proceso:
        tiempo_estimado = random.randint(5, 20)
        operacion = random.choice(['+', '-', '*', '/', '%'])
        operandos = (random.randint(1, 10), random.randint(1, 10))
        return Proceso(num, tiempo_estimado, operacion, operandos)

    def administar_nuevos(self):
        self.nuevos = [self.generar_procesos(n) for n in range(1, self.num_procesos + 1)]

    def manejar_teclas(self, event):
        if event.name == 'p' and not self.pausa:
            self.pausa = True
            print("Simulación pausada.")
        elif event.name == 'c' and self.pausa:
            self.pausa = False
            print("Simulación reanudada.")
        elif event.name == 'i' and not self.interrupcion:
            self.interrupcion = True
            print("Interrupción solicitada.")
        elif event.name == 'e' and not self.error:
            self.error = True
            print("Error solicitado.")
        elif event.name == "n":
            self.num_procesos += 1
            self.nuevos.append(self.generar_procesos(self.num_procesos))
            print(f"Se agrego el proceso numero: {self.num_procesos}")
        elif event.name == 'b':
            self.pausa = True
            print("Mostrando tabla de estado de procesos (BCP)...")
            self.mostrar_tabla_bcp()

    def administrar_memoria(self):
        while len(self.nuevos) > 0 and len(self.listos) + len(self.bloqueados) < 4:
            proceso = self.nuevos.pop(0)
            proceso.estado = 'Listo'
            proceso.tiempo_llegada = self.reloj  # Capturar el tiempo de llegada
            self.listos.append(proceso)

    def ejecucion(self):
        self.administar_nuevos()
        keyboard.on_press(self.manejar_teclas)


        while self.listos or self.bloqueados or self.proceso_en_ejecucion or self.nuevos:
            self.administrar_memoria()

            time.sleep(1)
            self.reloj += 1

            if not self.proceso_en_ejecucion and self.listos:
                self.proceso_en_ejecucion = self.listos.pop(0)
                self.proceso_en_ejecucion.estado = 'Ejecución'

                # Capturar el tiempo de respuesta
                if self.proceso_en_ejecucion.hora_comienzo_ejecucion is None:
                    self.proceso_en_ejecucion.hora_comienzo_ejecucion = self.reloj
                    self.proceso_en_ejecucion.tiempo_respuesta = self.reloj - self.proceso_en_ejecucion.tiempo_llegada


            if not self.pausa:
                self.mostrar_estado()

                if self.proceso_en_ejecucion is None:
                    pass
                else:
                    self.proceso_en_ejecucion.contador += 1

                if self.proceso_en_ejecucion:
                    self.proceso_en_ejecucion.tiempo_transcurrido += 1


                    if self.proceso_en_ejecucion.contador >= self.quantum:
                        self.proceso_en_ejecucion.contador = 0
                        self.proceso_en_ejecucion.estado = "Listo"
                        self.listos.append(self.proceso_en_ejecucion)
                        self.proceso_en_ejecucion = self.listos.pop(0)
                        self.proceso_en_ejecucion.estado = 'Ejecución'


                        if self.proceso_en_ejecucion.hora_comienzo_ejecucion is None:
                            self.proceso_en_ejecucion.hora_comienzo_ejecucion = self.reloj
                            self.proceso_en_ejecucion.tiempo_respuesta = self.reloj - self.proceso_en_ejecucion.tiempo_llegada

                    # Verificar si el proceso ha terminado
                    if self.proceso_en_ejecucion.tiempo_transcurrido >= self.proceso_en_ejecucion.tiempo_estimado:
                        try:
                            resultado_operacion = eval(
                                f"{self.proceso_en_ejecucion.operandos[0]} {self.proceso_en_ejecucion.operacion} {self.proceso_en_ejecucion.operandos[1]}")
                            error_ocurrido = False
                        except Exception as e:
                            resultado_operacion = str(e)
                            error_ocurrido = True

                        self.proceso_en_ejecucion.tiempo_finalizacion = self.reloj
                        self.proceso_en_ejecucion.tiempo_retorno = self.proceso_en_ejecucion.tiempo_finalizacion - self.proceso_en_ejecucion.tiempo_llegada
                        self.proceso_en_ejecucion.tiempo_servicio = self.proceso_en_ejecucion.tiempo_transcurrido
                        self.proceso_en_ejecucion.tiempo_espera = self.proceso_en_ejecucion.tiempo_retorno - self.proceso_en_ejecucion.tiempo_servicio  # Puede ser negativo si hay un error.
                        self.proceso_en_ejecucion.estado = "Terminado"
                        resultado = {
                            'proceso': self.proceso_en_ejecucion,  # Siempre almacenamos el objeto completo
                            'operacion': f"{self.proceso_en_ejecucion.operandos[0]} {self.proceso_en_ejecucion.operacion} {self.proceso_en_ejecucion.operandos[1]}",
                            'resultado': resultado_operacion,
                            'error': error_ocurrido
                        }

                        self.terminados.append(resultado)
                        self.proceso_en_ejecucion = None

                # Manejo de interrupciones
                if self.interrupcion and self.proceso_en_ejecucion:
                    self.proceso_en_ejecucion.estado = 'Bloqueado'
                    self.bloqueados.append(self.proceso_en_ejecucion)
                    self.proceso_en_ejecucion = None
                    self.interrupcion = False
                    print("Proceso interrumpido y agregado a la cola de bloqueados.")

                # Manejo de errores
                if self.error and self.proceso_en_ejecucion:
                    self.proceso_en_ejecucion.tiempo_finalizacion = self.reloj
                    self.proceso_en_ejecucion.tiempo_retorno = self.proceso_en_ejecucion.tiempo_finalizacion - self.proceso_en_ejecucion.tiempo_llegada
                    self.proceso_en_ejecucion.tiempo_servicio = self.proceso_en_ejecucion.tiempo_transcurrido
                    self.proceso_en_ejecucion.tiempo_espera = self.proceso_en_ejecucion.tiempo_retorno - self.proceso_en_ejecucion.tiempo_servicio  # Puede ser negativo si hay un error.
                    self.proceso_en_ejecucion.estado = "Terminado"
                    resultado = {
                        'proceso': self.proceso_en_ejecucion,
                        'operacion': f"{self.proceso_en_ejecucion.operandos[0]} {self.proceso_en_ejecucion.operacion} {self.proceso_en_ejecucion.operandos[1]}",
                        'resultado': "ERROR",
                        'error': True
                    }
                    self.terminados.append(resultado)
                    self.proceso_en_ejecucion = None
                    self.error = False
                    print("Proceso finalizado con ERROR.")

                # Incrementar el tiempo de bloqueo de los procesos bloqueados
                for proceso in self.bloqueados:
                    proceso.bloqueado_tiempo += 1
                    if proceso.bloqueado_tiempo >= 7:  # Tiempo de desbloqueo
                        proceso.estado = 'Listo'
                        proceso.tiempo_retorno += 7
                        proceso.bloqueado_tiempo = 0
                        self.listos.append(proceso)
                self.bloqueados = [p for p in self.bloqueados if p.estado == 'Bloqueado']

        # Mostrar la tabla final con los tiempos de cada proceso
        print(f"\nSimulación finalizada. Reloj:{self.reloj} | Resultados:")
        print("-" * 50)

        tabla_resultados = PrettyTable()
        tabla_resultados.field_names = ["ID", "Tiempo Llegada", "Tiempo Finalización", "Tiempo Retorno",
                                        "Tiempo Respuesta", "Tiempo Espera", "Tiempo Servicio"]

        for trabajo in self.terminados:
            proceso = trabajo.get('proceso')  # Accede con get para evitar KeyError
            if proceso:  # Verifica que el objeto proceso existe
                tabla_resultados.add_row([
                    proceso.id,
                    proceso.tiempo_llegada,
                    proceso.tiempo_finalizacion,
                    proceso.tiempo_retorno,
                    proceso.tiempo_respuesta,
                    proceso.tiempo_espera,
                    proceso.tiempo_servicio
                ])
        print(tabla_resultados)


def main():
    try:
        num_trabajos = int(input("Ingrese el número de procesos inicial (N): "))
        quantum = int(input("Defina el quantum: "))
        while num_trabajos <= 0:
            print("Ingrese el número de procesos inicial (N):")
            num_trabajos = int(input("Ingrese el número de procesos inicial (N): "))
            quantum = int(input("Defina el quantum: "))
            print("Define el Quantum: ")

        s = Simulador(num_trabajos, quantum)
        s.ejecucion()
    except ValueError:
        print("\nTe equivocaste al ingresar el daato")


if __name__ == '__main__':
    main()
