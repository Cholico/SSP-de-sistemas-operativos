import re
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

limpiar_pantalla()


def solicitar_numero():
    while True:
        try:
            # Pedir al usuario que ingrese un número
            numero = int(input("-> "))

            if numero <= 0:
                raise ValueError ("Ingresa un numero mayor a cero")
            else:
                return numero
        except ValueError as e:
            print(f"Entrada inválida: {e}. Por favor, intenta nuevamente. ")


def solicitar_cadena():
    while True:
        # Evitamos que la cadena tenga caracteres ectraños
        cadena = input("-> ")

        # Definir el patrón de caracteres válidos (letras, números y espacios)
        if re.match(r'^[a-zA-Z0-9\s]+$', cadena):
            return cadena
        else:
            print("Ingrese un nombre valido: ")


def solicitar_opernado():
    validos = ('+','*','-','/','%')

    while True:
        operando = input("-> ")

        if operando in validos:
            return operando

        else:
            print("Operación no válida, introduce una operación válida (+, -, *, /, %).")


def solicitar_digito(op=None):
    while True:
        try:
            # Pedir al usuario que ingrese un número
            numero = int(input("-> "))
            if (op == "/" or op == "%") and numero == 0:
                raise ZeroDivisionError("Ingrese un numero mayor a cero")

            return numero

        except ValueError as e:
            print(f"Entrada inválida: {e}. Por favor, intenta nuevamente.")
        except ZeroDivisionError as z:
            print(f"Entrada invalida: {z}. Ingrese nuevamente el segundo operando: ")





