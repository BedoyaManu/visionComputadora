import random

def adivina(intentos_max):

    numero_aleatorio = random.randint(0, 100)
    intentos_usados = 0
    while intentos_usados < intentos_max:
        try:
            numero_ingresado = int(input(f"Ingrese un número entre 0 y 100 (Intento {intentos_usados + 1}/{intentos_max}): "))
        except ValueError:
            print("Ingrese un número entero válido.")
            continue

        if numero_ingresado == numero_aleatorio:
            print("¡Felicidades! Adivinaste el número en", intentos_usados+1, "intentos.")
            break
        elif numero_ingresado < numero_aleatorio:
            print("El número ingresado es menor que el número secreto.")
        else:
            print("El número ingresado es mayor que el número secreto.")

        intentos_usados += 1

    if intentos_usados == intentos_max:
        print("No has podido adivinar el número! El número secreto era ", numero_aleatorio)

while True:
    salir = input("Desea salir del juego? (si/no): ").lower()
    if salir == "si":
        print("Saliendo...")
        break
    else:
        while True:
            try:
                intentos_max = int(input("Ingrese la cantidad máxima de intentos: "))
                if intentos_max > 0:
                    break
                else:
                    print("El número de intentos debe ser mayor que 0.")
            except ValueError:
                print("¡Error! Ingrese un número entero válido.")

        adivina(intentos_max)