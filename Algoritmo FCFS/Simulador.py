import random
import time
import keyboard
from prettytable import PrettyTable
from proceso import Proceso


class Simulador():
    def __init__(self, num_procesos):
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

    def mostrar_estado(self):
        print(f"Procesos en estado Nuevo: {len(self.nuevos)}")

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

                if self.proceso_en_ejecucion:
                    self.proceso_en_ejecucion.tiempo_transcurrido += 1


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
        while num_trabajos <= 0:
            print("El número de procesos debe ser mayor que 0.")
            num_trabajos = int(input("Ingrese el número de procesos inicial (N): "))

        s = Simulador(num_trabajos)
        s.ejecucion()
    except KeyboardInterrupt:
        print("\nSimulación interrumpida por el usuario.")


if __name__ == '__main__':
    main()
