import re
import secrets
import string
import sys
import termios
import inquirer
import pyperclip

LONGITUD_MIN_CONTRASENA = 8


def obtener_longitud_contrasena():
    """
    Obtiene la longitud deseada para la contraseña.
    """
    while True:
        try:
            longitud = int(input("¿Cuántos caracteres deseas en tu contraseña? "))
            if longitud < 1:
                print("Debes ingresar un número mayor que 0.")
                continue
            return longitud
        except ValueError:
            print("Error: La longitud de la contraseña debe ser un número.")


def obtener_opciones_seleccionadas(conjuntos_caracteres):
    """
    Obtiene las opciones seleccionadas para la contraseña.
    """
    pregunta = [
        inquirer.Checkbox(
            "opciones",
            "Utiliza las teclas de flecha y la barra espaciadora para seleccionar los tipos de caracteres deseados para tu contraseña",
            conjuntos_caracteres.keys(),
            default=["Minúsculas"],
            carousel=True,
        )
    ]

    while True:
        try:
            seleccionadas = inquirer.prompt(pregunta)["opciones"]
        except termios.error:
            sys.exit(
                "Ocurrió un error en la consulta. ¿Estás ejecutando este script en una terminal? (Inquirer no funciona en entornos de desarrollo integrados)"
            )

        if seleccionadas:
            return seleccionadas

        print("Debes seleccionar al menos una opción.")


def generar_contrasena(seleccionadas, longitud, conjuntos_caracteres):
    """
    Genera una contraseña basada en las opciones seleccionadas.
    """
    caracteres = "".join([secrets.choice(conjuntos_caracteres[i]) for i in seleccionadas])
    restantes = "".join([conjuntos_caracteres[i] for i in seleccionadas])
    adicionales = [secrets.choice(restantes) for _ in range(longitud - len(seleccionadas))]

    generada = list(caracteres + "".join(adicionales))
    secrets.SystemRandom().shuffle(generada)
    contrasena = "".join(generada)

    return contrasena


def fortaleza_contrasena(contrasena):
    """
    Determina la fortaleza de una contraseña.
    """
    if len(contrasena) <= LONGITUD_MIN_CONTRASENA:
        return "Débil"
    if re.search(r"\d|[A-Z]", contrasena) and re.search(r"[\W_]", contrasena):
        return "Fuerte"
    return "Media"


def principal():
    """
    Función principal del programa.
    """
    print("¡Bienvenido al Generador de Contraseñas en Python!")

    longitud = obtener_longitud_contrasena()

    conjuntos_caracteres = {
        "Minúsculas": string.ascii_lowercase,
        "Mayúsculas": string.ascii_uppercase,
        "Números": string.digits,
        "Símbolos": string.punctuation,
    }

    seleccionadas = obtener_opciones_seleccionadas(conjuntos_caracteres)

    contrasena = generar_contrasena(seleccionadas, longitud, conjuntos_caracteres)

    print(f"Contraseña generada: {contrasena}")

    try:
        pyperclip.copy(contrasena)
    except pyperclip.PyperclipException as e:
        print(
            f"No se pudo copiar la contraseña al portapapeles: {e}. Por favor, cópiala manualmente."
        )

    print(f"Fuerza de la contraseña: {fortaleza_contrasena(contrasena)}")


if __name__ == "__main__":
    principal()
