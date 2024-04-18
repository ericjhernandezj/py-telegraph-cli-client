"""
Python Telegraph CLI Client
v1.0.4

Descripción
-----------
Cliente de consola escrito en Python para Telegraph (telegra.ph),
herramienta de Blogging minimalista desarrollada por Telegram.

Módulos
-------
- requests: Para hacer peticiones a la API de Telegra.ph (telegra.ph/api).
- os: Para usar el método system() y limpiar la consola.

Funcionalidades
---------------
- Crear cuenta: Permite crear una cuenta en Telegraph.
- Inicio de sesión: Permite iniciar sesión en una cuenta existente usando un
                    token de acceso.
    - Mostrar información de la cuenta
    - Editar información de la cuenta
    - Revocar acceso a navegadores y cerrar todas las sesiones generando un
      nuevo token de acceso

Estructura del código
---------------------
Este programa usa programación modular y un poco de programación orientada a
objetos

Funciones destacables:
- main: Código principal del programa, donde inician todos los procesos.
- createAccount: Permite la creación de cuentas.
- login: Permite el inicio de sesión en una cuenta existente. Una vez iniciada
         la sesión se pueden realizar acciones como editar datos básicos,
         cerrar sesiones, accerder a cuenta desde un navegador web.
- getAccountInfo: Permite ver información de una cuenta usando su token de
                  acceso.
- editAccountInfo: Permite editar información de una cuenta como nombre corto,
                   nombre de autor y URL de autor.
- revokeAccessToken: Cierra sesiones en navegadores web y genera un nuevo
                     token de acceso.

Uso
---
~$ git clone https://github.com/ericjhernandezj/py-telegraph-cli-client.git
~$ cd py-telegraph-cli-client/
~$ python3 src/main.py

Si este programa será ejecutado en Windows, ir a la función clear() y cambiar
system("clear") por system("cls").

Autor
-----
Eric Joel Hernandez Javier (@ericjhernandezj)
https://ericjhernandezj.com
ericjhernandezj@duck.com
"""

import os  # Para limpiar la pantalla

import requests  # Para realizar peticiones a la API de telegra.ph
import re # Para pseudo-verificar URLs


class StrStyle:
    """
    Clase para definir estilos de texto con colores ANSI.

    Attributes:
        IMPORTANT (str): Púrpura. Importante pero no crítico.
        INFO (str): Azul. Información no crítica.
        SUCCESS (str): Cian. Mensaje de éxito.
        SUCCESS_HIGHLIGHT (str): Verde. Mensaje de éxito importante.
        WARNING (str): Amarillo. Mensaje de advertencia.
        REGULAR (str): Color predeterminado. Mensajes normales.
        CONTEXT (str): Gris. Información contextual adicional.
        WARNING_HIGHLIGHT (str): Amarillo oscuro. Destaque de advertencia.
        FAIL (str): Rojo. Mensaje de error.
        BOLD (str): Estilo de texto en negrita.
        UNDERLINE (str): Estilo de texto subrayado.
        ENDC (str): Restablece el formato del texto al predeterminado.
    Example:
        >>> print(StrStyle.FAIL + "Esto es un mensaje de error" + StrStyle.ENDC)
    """
    IMPORTANT = '\033[95m'  # Purple. Important but not critical
    INFO = '\033[94m'  # Blue. Non-critical information
    SUCCESS = '\033[96m'  # Cyan. Success message
    SUCCESS_HIGHLIGHT = '\033[92m'  # Green. Important Success message
    WARNING = '\033[33m'  # Yellow. Warning message
    REGULAR = '\033[97m'  # Default color. Normal messages
    CONTEXT = '\033[90m'  # Grey. More contextual information
    WARNING_HIGHLIGHT = '\033[93m'  # Darker Yellow. Warning highlight message
    FAIL = '\033[91m'  # Red. Error message
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


class Account:
    """
    Clase para representar una cuenta de usuario.

    Attributes:
        ok (bool): Indica si la cuenta se creó de forma correcta.
        short_name (str): Nombre corto.
        author_name (str): Nombre del autor.
        author_url (str): URL del autor.
        page_count (int): Cantidad de páginas.
        auth_url (str): URL de inicio de sesión para navegadores web.
        access_token (str): Token de acceso.
    """

    def __init__(self, ok, short_name, author_name, author_url, page_count,
                 auth_url, access_token):
        """
        Inicializa una nueva cuenta de usuario.

        Args:
            ok (bool): Indica si la cuenta se creó de forma correcta.
            short_name (str): Nombre corto.
            author_name (str): Nombre del autor.
            author_url (str): URL del autor.
            page_count (int): Cantidad de páginas.
            auth_url (str): URL de inicio de sesión para navegadores web.
            access_token (str): Token de acceso.
        """
        self.ok: bool = ok
        self.short_name: str = short_name
        self.author_name: str = author_name
        self.author_url: str = author_url
        self.page_count: int = page_count
        self.auth_url: str = auth_url
        self.access_token: str = access_token

    def printInfo(self, target="default"):
        """
        Imprime información del usuario según el 'target'.

        Args:
            target (str): Define qué información mostrar:
                - 'default': Muestra la información pública/segura del usuario.
                - 'all': Muestra toda la información del usuario, incluyendo
                         información sensible.
                - 'ok', 'short_name', 'author_name', 'author_url',
                  'page_count', 'auth_url', 'access_token': Muestra información
                                                            específica.

        Si 'target' no coincide con ninguna opción, imprime un mensaje de
        error.

        Example:
            >>> account.printInfo("short_name")
            "Nombre corto: Eric Hernandez"
        """
        if target == "default":
            print("--- Información Pública del Usuario ---")
            print(f"Nombre: {self.short_name}")
            print(f"Autor: {self.author_name}")
            print(f"URL: {self.author_url}")
            print(f"Páginas: {self.page_count}")
        elif target == "all":
            print("--- Información (pública y privada) del Usuario ---")
            print(f"Nombre: {self.short_name}")
            print(f"Autor: {self.author_name}")
            print(f"URL: {self.author_url}")
            print(f"Páginas: {self.page_count}")
            print(f"URL de login para navegador web: {self.auth_url}")
            print(f"Token de acceso: {self.access_token}")
        elif target == "ok":
            print(f"OK: {self.ok}")
        elif target == "short_name":
            print(f"Nombre corto: {self.short_name}")
        elif target == "author_name":
            print(f"Autor: {self.author_name}")
        elif target == "author_url":
            print(f"URL de autor: {self.author_url}")
        elif target == "page_count":
            print(f"Páginas: {self.page_count}")
        elif target == "auth_url":
            print(f"Iniciar sesión en navegado web: {self.auth_url}")
        elif target == "access_token":
            print(f"Token de acceso: {self.access_token}")
        else:
            print("Error con pase de argumentos")


def clear():
    """
    Limpia la consola (no los datos).

    Example:
        >>> clear()
    """
    os.system('cls' if os.name == 'nt' else 'clear') # Detecta si el sistema es Windows o no


def createAccount(short_name: str, author_name: str, author_url: str):
    """
    Creación de Cuenta en Telegra.ph.

    Args:
        short_name (str): Nombre corto para identificar la cuenta.
                          Este dato no será visible públicamente.
        author_name (str): Nombre del autor de los futuros artículos.
        author_url (str): Website al que el lector es enviado si toca el
                          nombre del autor en el artículo.
    Returns:
        Account: Si la cuenta se crea con éxito, se devuelve un objeto Account
                 que contiene los datos recibidos. En caso de error,
                 retorna un string indicando el problema.
    Example:
        >>> account = createAccount("Cuenta de Prueba", "Eric Hernandez",
                                    "https://example.com")
        >>> account.short_name
        "Cuenta de Prueba"
        >>> account.page_count
        0
    """
    response = requests.get(
        f"https://api.telegra.ph/createAccount?"
        f"short_name={short_name}&author_name={author_name}&"
        f"author_url={author_url}", timeout=5)

    if response.status_code == 200:
        data = response.json()
        token = data["result"]["access_token"]

        response = requests.get(
            f'https://api.telegra.ph/getAccountInfo?access_token={token}&'
            f'fields=["short_name", "author_name", "author_url", '
            f'"page_count","auth_url"]', timeout=5)
        data = response.json()

        return Account(True, data["result"]["short_name"],
                       data["result"]["author_name"],
                       data["result"]["author_url"],
                       data["result"]["page_count"],
                       data["result"]["auth_url"], token)
    else:
        return Account(False, "", "", "", "", "", "")


def login(access_token: str):
    """
    Inicio de sesión en cuenta existente.

    Args:
        access_token (str): Token de acceso a una cuenta existente.
    Returns:
        bool: Retorna False cuando se termina el inicio de sesión.
    Example:
        >>> login(
            "f1c7cc248f2d3e1fea44c28a0b93148e4dea0e7a24b7cfe791a993a13413"
            )
        False
    """
    while True:
        account = getAccountInfo(access_token)

        if account.ok:
            print("\nEsta es una sesión temporal")
            print(f"Hola, {account.short_name} ({account.author_name})")
            print()
            print("1. Mostrar información")
            print("2. Editar Información")
            print("3. Crear nuevo token de acceso")
            print("0. Salir")
            user_input = input("> ")

            if user_input == "1":
                print("1. Mostrar Información Pública")
                print("2. Mostrar Información Pública y Privada")
                print("0. Regresar")
                user_input = input("> ")

                if user_input == "1":
                    clear()
                    account.printInfo("default")
                elif user_input == "2":
                    clear()
                    account.printInfo("all")
                elif user_input == "0":
                    clear()
                else:
                    clear()
                    print("Entrada no válida. Regresando al menú principal")
            elif user_input == "2":
                print("1. Cambiar nombre corto")
                print("2. Cambiar autor")
                print("3. Cambiar URL de autor")
                print("0. Regresar")
                user_input = input("> ")

                if user_input == "1":
                    clear()
                    print("Ingresar nuevo nombre corto")
                    new_short_name = input("> ")

                    editAccountInfo(access_token, "short_name", new_short_name)
                elif user_input == "2":
                    clear()
                    print("Ingresar nuevo autor")
                    new_author_name = input("> ")

                    editAccountInfo(access_token, "author_name",
                                    new_author_name)
                elif user_input == "3":
                    clear()
                    print("Ingresar nueva URL")
                    new_author_url = input("> https://")
                    new_author_url = f"https://{new_author_url}"

                    editAccountInfo(access_token, "author_url", new_author_url)
                elif user_input == "0":
                    clear()
                else:
                    clear()
                    print("Entrada no válida. Regresando al menú principal")
            elif user_input == "3":
                clear()
                print("Ingresar 'OK' si deseas cerrar todas las sesiones, "
                      "generar nuevo token de acceso y generar nueva URL "
                      "para navegadores web\n"
                      "Después de ingresar 'OK' se te proporcionará un nuevo "
                      "token y nueva URL para navegadores web. Guardar el "
                      "nuevo token ya que es la unica forma de acceder "
                      "a la cuenta\n"
                      "Una vez generado el nuevo token de acceso, el token "
                      "anterior quedará inutilizable")
                user_input = input("> ")

                if user_input == "OK":
                    revokeAccessToken(access_token)

                    while True:
                        print(
                            "Si ya has guardado tu nuevo token de acceso, "
                            "ingresa 'EXIT' para cerrar del programa"
                        )
                        user_input = input("> ")

                        if user_input == "EXIT":
                            print("Cerrando programa")

                            return False
                else:
                    print("Acción cancelada")
            elif user_input == "0":
                print("Saliendo...")

                return False
            else:
                print("Entrada no válida")
        else:
            print("La cuenta no existe.")
            print(f'Token "{account.access_token}" no válido')

            return False


def getAccountInfo(access_token):
    """
    Obtiene información de una cuenta usando su token de acceso.

    Args:
        access_token (str): Token de acceso a una cuenta existente.
    Returns:
        Account: Devuelve un objeto Account que contiene los datos
        recibidos desde el API.
    Example:
        >>> account = getAccountInfo(
            "f1c7cc248f2d3e1fea44c28a0b93148e4dea0e7a24b7cfe791a993a13413"
            )
        >>> account.short_name
        "Cuenta de Prueba"
        >>> account.page_count
        0
    """
    response = requests.get(
        f'https://api.telegra.ph/getAccountInfo?access_token={access_token}&'
        f'fields=["short_name", "author_name", "author_url", "auth_url",'
        f'"page_count"]', timeout=5)
    data = response.json()

    if data["ok"]:
        return Account(True, data["result"]["short_name"],
                   data["result"]["author_name"], data["result"]["author_url"],
                   data["result"]["page_count"], data["result"]["auth_url"],
                   access_token)
    else:
        return Account(False, "", "", "", "", "", access_token)


def editAccountInfo(access_token: str, target: str, new_value: str):
    """
    Permite editar dato a la vez de la cuenta enlazada al token de acceso.

    Args:
        access_toke (str): Token de acceso a una cuenta existente.
        target (str): Clave del dato que se quiere editar.
        new_value (str): Nuevo valor que se sobrescribirá sobre el
                         argumentos 'target'
    Example:
        >>> editAccountInfo(
            "f1c7cc248f2d3e1fea44c28a0b93148e4dea0e7a24b7cfe791a993a13413",
            "author_name", "Eric Joel Hernandez")
        "Cambio hecho con éxito"
    """
    response = requests.get(
        f"https://api.telegra.ph/editAccountInfo?access_token={access_token}&"
        f"{target}={new_value}", timeout=5)
    data = response.json()

    if data["ok"]:
        print("Cambio hecho con éxito")
    else:
        print("Error. ok not True")


def revokeAccessToken(access_token: str):
    """
    Cierra todas las sesiones generando un nuevo token de acceso.

    Args:
        access_token (str): Token de acceso a una cuenta existente.
    Example:
        >>> revokeAccessToken(
            "f1c7cc248f2d3e1fea44c28a0b93148e4dea0e7a24b7cfe791a993a13413"
            )
        "Sesiones cerradas. Nuevo token generado. Nuevo auth url generado"
        "Nuevo token de acceso:
        h6c0cb248f1d3e1fea45c28a0b93148e4dea0e5z24v7cde781a903abv2s1"
        "Nuevo Auth URL:
        https://edit.telegra.ph/auth/71oM2k1Js5FUKuUfNEYkqtr7GhpFtVtyThlTClC20i"
    """
    response = requests.get(
        f"https://api.telegra.ph/revokeAccessToken?access_token={access_token}", timeout=5)
    data = response.json()

    if data["ok"]:
        print(
            "Sesiones cerradas. Nuevo token generado. Nuevo auth_url generado")
        print(f"Nuevo token de acceso: {data['result']['access_token']}")
        print(f"Nuevo auth_url: {data['result']['auth_url']}")
    else:
        print("Error. ok not True")


def main():
    """Función principal del programa."""
    clear()

    print("Cliente de Consola escrito en Python para Telegra.ph")
    print()
    print("1. Crear cuenta")
    print("2. Acceder a cuenta")
    user_input = input("> ")

    if user_input == "1":
        clear()

        print("(Obligatorio)\n"
              "Ingresar nombre corto para La Cuenta\n"
              "Este nombre será usado para ayudar a identificar cuentas "
              "en caso de tener muchas")

        while True:
            short_name = input("> ")

            if len(short_name) < 1:
                print('Nombre corto muy corto. Intente de nuevo.')
            elif len(short_name) > 32:
                print('Nombre corto muy largo. Intente de nuevo.')
            else:
                break


        print("(Obligatorio)\n"
          "Ingresar nombre del autor de los articulos\n"
          "Este nombre aparecerá como autor en futuros articulos")

        while True:
            author_name = input("> ")

            if len(author_name) < 0:
                print('Nombre de autor muy corto. Intente de nuevo.')
            elif len(author_name) > 128:
                print('Nombre de autor muy largo. Intente de nuevo.')
            else:
                break

        print("(Obligatorio)\n"
              "Ingresar URL de autor\n"
              "Cuando el lector presione el nombre del autor, "
              "será enviado a esta URL")

        while True:
            author_url = input("> https://")

            if not author_url:
                break

            url_pattern = re.compile(
                r'(?:www\.)?'
                r'([a-zA-Z0-9-]{1,63}\.){1,}'
                r'[a-zA-Z]{2,}(?:/[a-zA-Z0-9-]+)*')

            if url_pattern.match(author_url):
                author_url = f'https://{author_url}'
                if len(author_url) > 512:
                    print('URL válida pero muy larga.')
                else:
                    break
            else:
                print('Formato de URL invalido')


        account = createAccount(short_name, author_name, author_url)


        if account.ok:
            print("Cuenta creada con éxito")
            account.printInfo("all")
        else:
            print("Error al crear cuenta")
            print(account.printInfo("ok"))
    elif user_input == "2":
        clear()

        print("Ingresar token de acceso")
        token = input("> ")

        clear()

        login(token)
    else:
        print("Error")


if __name__ == "__main__":
    main()
