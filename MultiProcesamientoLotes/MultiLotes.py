import random
import time
import keyboard
from prettytable import PrettyTable


class Proceso:
    def __init__(self, id, tiempo_estimado, operacion, operandos):
        self.id = id
        self.tiempo_estimado = tiempo_estimado
        self.operacion = operacion
        self.operandos = operandos
        self.tiempo_transcurrido = 0
        self.finalizado = False
        self.error = False

    def ejecutar(self):
        try:
            if self.operacion == '+':
                resultado = self.operandos[0] + self.operandos[1]
            elif self.operacion == '-':
                resultado = self.operandos[0] - self.operandos[1]
            elif self.operacion == '*':
                resultado = self.operandos[0] * self.operandos[1]
            elif self.operacion == '/':
                resultado = self.operandos[0] / self.operandos[1] if self.operandos[
                                                                         1] != 0 else "Error: División por cero"
            elif self.operacion == '%':
                resultado = self.operandos[0] % self.operandos[1]
            return resultado
        except Exception as e:
            return f"Error: {str(e)}"


def generar_proceso(id):
    tiempo_estimado = random.randint(5, 20)
    operacion = random.choice(['+', '-', '*', '/', '%'])
    operandos = (random.randint(1, 10), random.randint(1, 10))
    return Proceso(id, tiempo_estimado, operacion, operandos)


def mostrar_estado(lotes_pendientes, proceso_en_ejecucion, trabajos_terminados, reloj, lote_actual, numero_lote):
    print(f"Lotes pendientes: {len(lotes_pendientes)}")
    print(f"Reloj: {reloj}")

    # Mostrar procesos en el lote actual
    print(f"\nLote en ejecución: {numero_lote}")
    print("\nProcesos en el lote actual:")
    if lote_actual:
        tabla_lote = PrettyTable()
        tabla_lote.field_names = ["ID", "Operación", "Operandos", "Tiempo Estimado", "Tiempo Transcurrido"]

        for proceso in lote_actual:
            tabla_lote.add_row([proceso.id, proceso.operacion, proceso.operandos, proceso.tiempo_estimado,
                                proceso.tiempo_transcurrido])

        print(tabla_lote)

    # Mostrar estado del proceso en ejecución
    if proceso_en_ejecucion:
        print(f"\nProceso en ejecución: ID: {proceso_en_ejecucion.id}, operación: {proceso_en_ejecucion.operacion}, "
              f"operandos: {proceso_en_ejecucion.operandos}, tiempo ejecutado: {proceso_en_ejecucion.tiempo_transcurrido}, "
              f"tiempo restante: {proceso_en_ejecucion.tiempo_estimado - proceso_en_ejecucion.tiempo_transcurrido}")

    # Mostrar trabajos terminados
    print("\nTrabajos terminados:")
    if trabajos_terminados:
        tabla_terminados = PrettyTable()
        tabla_terminados.field_names = ["ID", "Operación", "Resultado", "Error"]

        for trabajo in trabajos_terminados:
            resultado = "ERROR" if trabajo['error'] else trabajo['resultado']
            tabla_terminados.add_row([trabajo['id'], trabajo['operacion'], resultado, trabajo['error']])

        print(tabla_terminados)
    else:
        print("No hay trabajos terminados.")

    print("-" * 50)


# Variable para control de pausa e interrupciones
pausa = False
interrupcion = False
error = False


def manejar_teclas(event):
    global pausa, interrupcion, error

    if event.name == 'p' and not pausa:
        pausa = True
        print("Simulación pausada.")

    elif event.name == 'c' and pausa:
        pausa = False
        print("Simulación reanudada.")

    elif event.name == 'i' and not interrupcion:
        interrupcion = True
        print("Interrupción solicitada.")

    elif event.name == 'e' and not error:
        error = True
        print("Error solicitado.")




def ejecutar_simulacion(num_trabajos):
    global pausa, interrupcion, error
    lotes_pendientes = []
    trabajos_terminados = []
    reloj = 0
    lote_actual = []
    total_procesos = num_trabajos

    # Generación de trabajos y lotes
    for i in range(1, num_trabajos + 1):
        proceso = generar_proceso(i)
        lote_actual.append(proceso)
        if len(lote_actual) == 5 or i == num_trabajos:
            lotes_pendientes.append(lote_actual)
            lote_actual = []

    proceso_en_ejecucion = None
    numero_lote = 1  # Contador para los lotes

    # Configurar el listener para las teclas
    keyboard.on_press(manejar_teclas)

    while lotes_pendientes or proceso_en_ejecucion:
        if not proceso_en_ejecucion and lotes_pendientes:
            lote_actual = lotes_pendientes.pop(0)
            proceso_en_ejecucion = lote_actual.pop(0)

        # Mostrar estado
        mostrar_estado(lotes_pendientes, proceso_en_ejecucion, trabajos_terminados, reloj, lote_actual, numero_lote)

        # Esperar mientras la simulación esté en pausa
        while pausa:
            time.sleep(0.1)  # Breve pausa para evitar uso excesivo de CPU

        # Simulación de ejecución del proceso actual
        time.sleep(1)

        # Solo incrementar el tiempo y reloj si no hay error
        if not error:
            proceso_en_ejecucion.tiempo_transcurrido += 1
            reloj += 1

            if proceso_en_ejecucion.tiempo_transcurrido >= proceso_en_ejecucion.tiempo_estimado:
                resultado = proceso_en_ejecucion.ejecutar()
                trabajos_terminados.append({
                    'id': proceso_en_ejecucion.id,
                    'operacion': f"{proceso_en_ejecucion.operandos[0]} {proceso_en_ejecucion.operacion} {proceso_en_ejecucion.operandos[1]}",
                    'resultado': resultado,
                    'error': False
                })
                if lote_actual:
                    proceso_en_ejecucion = lote_actual.pop(0)
                else:
                    proceso_en_ejecucion = None
                    numero_lote += 1  # Incrementar el número de lote solo si se han terminado todos los procesos en el lote

        # Si se solicitó un error
        if error and proceso_en_ejecucion:
            trabajos_terminados.append({
                'id': proceso_en_ejecucion.id,
                'operacion': f"{proceso_en_ejecucion.operandos[0]} {proceso_en_ejecucion.operacion} {proceso_en_ejecucion.operandos[1]}",
                'resultado': 'ERROR',
                'error': True
            })
            proceso_en_ejecucion = None
            proceso_en_ejecucion = lote_actual.pop(0) if lote_actual else None
            error = False
            print("Proceso finalizado por error.")

        # Si se solicitó una interrupción
        if interrupcion:
            lote_actual.append(proceso_en_ejecucion)  # Mover el proceso interrumpido al final del lote actual
            proceso_en_ejecucion = lote_actual.pop(0) if lote_actual else None  # Ejecutar el siguiente proceso en el lote
            interrupcion = False
            print("Proceso interrumpido y agregado al final del lote actual.")

    # Al finalizar la simulación, mostrar todos los trabajos terminados
    print(f"\nSimulación finalizada. | Reloj:{reloj}")
    print("\nTrabajos terminados:")
    for trabajo in trabajos_terminados:
        if trabajo['error']:
            print(f"ID: {trabajo['id']}, operación: {trabajo['operacion']}, resultado: ERROR")
        else:
            print(f"ID: {trabajo['id']}, operación: {trabajo['operacion']}, resultado: {trabajo['resultado']}")

    # Mostrar cuántos procesos no se ejecutaron (si es que quedaron pendientes)
    procesos_restantes = sum(len(lote) for lote in lotes_pendientes)
    if procesos_restantes > 0:
        print(f"\nProcesos pendientes sin ejecutar: {procesos_restantes} de {total_procesos} procesos totales.")
    else:
        print("\nTodos los procesos fueron ejecutados.")

    input("Enter para continuar....")

# Iniciar simulación
num_trabajos = int(input("Ingresa el número de trabajos: "))
ejecutar_simulacion(num_trabajos)
