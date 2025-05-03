import random

def elegir_palabra():
    palabras = ['python', 'programacion', 'ahorcado', 'desarrollo', 'inteligencia', 'artificial']
    return random.choice(palabras)

def mostrar_estado(palabra, letras_adivinadas):
    estado = ''.join([letra if letra in letras_adivinadas else '_' for letra in palabra])
    return estado

def jugar():
    palabra_secreta = elegir_palabra()
    letras_adivinadas = set()
    intentos_restantes = 6

    print("¡Bienvenido al juego del ahorcado!")

    while intentos_restantes > 0:
        print(f"\nPalabra: {mostrar_estado(palabra_secreta, letras_adivinadas)}")
        print(f"Letras adivinadas: {', '.join(sorted(letras_adivinadas))}")
        print(f"Intentos restantes: {intentos_restantes}")

        letra = input("Adivina una letra: ").lower()

        if letra in letras_adivinadas:
            print("Ya has adivinado esa letra. Intenta con otra.")
            continue

        letras_adivinadas.add(letra)

        if letra in palabra_secreta:
            print("¡Bien hecho! La letra está en la palabra.")
        else:
            intentos_restantes -= 1
            print("Letra incorrecta. Pierdes un intento.")

        if all(letra in letras_adivinadas for letra in palabra_secreta):
            print(f"\n¡Felicidades! Has adivinado la palabra: {palabra_secreta}")
            break
    else:
        print(f"\n¡Has perdido! La palabra era: {palabra_secreta}")

if __name__ == "__main__":
    jugar()
