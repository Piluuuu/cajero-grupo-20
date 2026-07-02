# =============================================================================
# SIMULADOR DE CAJERO AUTOMÁTICO
# Materia: Algoritmos y Estructuras de Datos - UTN FRRe
# =============================================================================


# -----------------------------------------------------------------------------
# SECCIÓN 1: ESTRUCTURA DE DATOS DE USUARIOS
# -----------------------------------------------------------------------------
# Se utiliza un diccionario de diccionarios. La clave principal es el DNI
# del usuario (string), y el valor es otro diccionario con sus datos.
#
# Campos de cada usuario:
#   - "pin"          : PIN de 4 dígitos (string, para conservar ceros iniciales)
#   - "nombre"       : Nombre completo del titular
#   - "saldo"        : Saldo disponible en pesos (float)
#   - "intentos"     : Contador de intentos fallidos consecutivos (int)
#   - "bloqueado"    : Estado de bloqueo de la cuenta (bool)
# -----------------------------------------------------------------------------

usuarios = {
    "48399733": {
        "pin":       "1234",
        "nombre":    "Pilar Verón Romero",
        "saldo":     150000.00,
        "intentos":  0,
        "bloqueado": False
    },
    "87654321": {
        "pin":       "4321",
        "nombre":    "Mauro Benitez",
        "saldo":     75500.50,
        "intentos":  0,
        "bloqueado": False
    },
    "11223344": {
        "pin":       "0000",
        "nombre":    "Ana Paula Verón",
        "saldo":     200000.00,
        "intentos":  0,
        "bloqueado": False
    },
    "29032008": {
        "pin":       "5678",
        "nombre":    "Milena Sosa",
        "saldo":     3000.00,
        "intentos":  0,
        "bloqueado": False
    }
}

# Constante: máximo de intentos permitidos antes del bloqueo
MAX_INTENTOS = 3


# -----------------------------------------------------------------------------
# SECCIÓN 2: FUNCIONES AUXILIARES DE VALIDACIÓN
# -----------------------------------------------------------------------------

def validar_dni(dni_ingresado):
    """
    Valida que el DNI ingresado cumpla el formato esperado:
      - Exactamente 8 caracteres.
      - Solo dígitos numéricos.
      - Que exista en la base de datos de usuarios.

    Parámetro:
        dni_ingresado (str): El DNI tal como lo escribió el usuario.

    Retorna:
        True  si el DNI es válido y existe en el sistema.
        False en cualquier otro caso.
    """
    # Verificamos longitud y que sean solo números
    if len(dni_ingresado) != 8 or not dni_ingresado.isdigit():
        print("  [!] El DNI debe tener exactamente 8 dígitos numéricos.")
        return False

    # Verificamos que el DNI esté registrado en el sistema
    if dni_ingresado not in usuarios:
        print("  [!] DNI no encontrado en el sistema.")
        return False

    return True


def validar_pin(pin_ingresado):
    """
    Valida el formato básico del PIN ingresado:
      - Exactamente 4 caracteres.
      - Solo dígitos numéricos.
    (La verificación de si el PIN es correcto se hace en la función de login.)

    Parámetro:
        pin_ingresado (str): El PIN tal como lo escribió el usuario.

    Retorna:
        True  si el formato es válido.
        False en cualquier otro caso.
    """
    if len(pin_ingresado) != 4 or not pin_ingresado.isdigit():
        print("  [!] El PIN debe tener exactamente 4 dígitos numéricos.")
        return False

    return True


# -----------------------------------------------------------------------------
# SECCIÓN 3: FUNCIÓN PRINCIPAL DE LOGIN
# -----------------------------------------------------------------------------

def login():
    """
    Gestiona el proceso completo de inicio de sesión del usuario.

    Flujo general:
        1. Solicita el DNI y lo valida (formato y existencia).
        2. Verifica si la cuenta está bloqueada.
        3. Entra en un bucle de hasta MAX_INTENTOS intentos de PIN.
        4. Si el PIN es correcto → retorna el DNI del usuario autenticado.
        5. Si se superan los intentos → bloquea la cuenta y retorna None.

    Retorna:
        str  : El DNI del usuario que inició sesión exitosamente.
        None : Si el login falló (bloqueo o cancelación).
    """

    print("=" * 50)
    print("     BIENVENIDO AL CAJERO AUTOMÁTICO")
    print("=" * 50)

    # ------------------------------------------------------------------
    # PASO 1: Solicitar y validar el DNI
    # Usamos un bucle para no avanzar hasta tener un DNI con formato correcto.
    # ------------------------------------------------------------------
    dni = ""
    dni_valido = False

    while not dni_valido:
        print("\nIngrese su DNI (8 dígitos) o escriba 'salir' para cancelar:")
        dni = input("  DNI: ").strip()

        # Permitimos al usuario salir del proceso de login
        if dni.lower() == "salir":
            print("\n  Operación cancelada. ¡Hasta luego!")
            return None

        # Usamos nuestra función auxiliar para validar formato y existencia
        dni_valido = validar_dni(dni)

    # ------------------------------------------------------------------
    # PASO 2: Verificar si la cuenta está bloqueada
    # Antes de pedir el PIN, chequeamos el estado de la cuenta.
    # ------------------------------------------------------------------
    if usuarios[dni]["bloqueado"]:
        print("\n  [X] La cuenta asociada al DNI ingresado está BLOQUEADA.")
        print("      Comuníquese con el banco para desbloquearla.")
        return None

    # Guardamos una referencia al diccionario del usuario para mayor legibilidad
    usuario_actual = usuarios[dni]

    # ------------------------------------------------------------------
    # PASO 3: Bucle de verificación del PIN
    #
    # Este bucle se ejecuta mientras:
    #   a) No se hayan agotado los intentos (contador < MAX_INTENTOS), Y
    #   b) La cuenta no esté bloqueada.
    #
    # En cada iteración:
    #   - Informamos cuántos intentos quedan.
    #   - Pedimos el PIN.
    #   - Validamos su formato.
    #   - Comparamos con el PIN almacenado.
    # ------------------------------------------------------------------
    while usuario_actual["intentos"] < MAX_INTENTOS:

        # Calculamos y mostramos los intentos restantes
        intentos_restantes = MAX_INTENTOS - usuario_actual["intentos"]
        print(f"\n  Intentos restantes: {intentos_restantes}")
        print("  Ingrese su PIN de 4 dígitos:")
        pin_ingresado = input("  PIN: ").strip()

        # Validación de formato del PIN (si el formato es malo, reintentamos
        # sin consumir un intento, es un aviso amigable al usuario)
        if not validar_pin(pin_ingresado):
            continue  # Volvemos al inicio del while sin sumar intento

        # ------------------------------------------------------------------
        # VERIFICACIÓN: ¿El PIN ingresado coincide con el PIN almacenado?
        # ------------------------------------------------------------------
        if pin_ingresado == usuario_actual["pin"]:
            # ✅ PIN CORRECTO: login exitoso
            usuario_actual["intentos"] = 0  # Reseteamos el contador de intentos
            print("\n" + "=" * 50)
            print(f"  ¡Bienvenido/a, {usuario_actual['nombre']}!")
            print("=" * 50)
            return dni  # <-- Retornamos el DNI para que lo usen los demás módulos

        else:
            # ❌ PIN INCORRECTO: sumamos un intento fallido
            usuario_actual["intentos"] += 1  # Acumulador de intentos fallidos

            if usuario_actual["intentos"] < MAX_INTENTOS:
                # Todavía hay intentos disponibles
                print(f"  [!] PIN incorrecto. Verifique e intente nuevamente.")
            else:
                # Se agotaron los intentos → bloqueamos la cuenta
                usuario_actual["bloqueado"] = True
                print("\n  [X] Ha superado el número máximo de intentos.")
                print("      Su cuenta ha sido BLOQUEADA por seguridad.")
                print("      Comuníquese con el banco para desbloquearla.")
                return None  # Login fallido

    # Si por alguna razón se sale del while sin retornar, retornamos None
    return None


# -----------------------------------------------------------------------------
# SECCIÓN 4: FUNCIÓN AUXILIAR PARA OTROS MÓDULOS
# -----------------------------------------------------------------------------

def obtener_datos_usuario(dni):
    """
    Función utilitaria para que los demás módulos (menú, transferencias,
    extracciones) puedan acceder a los datos del usuario autenticado.

    Parámetro:
        dni (str): DNI del usuario cuya sesión está activa.

    Retorna:
        dict : Diccionario con todos los datos del usuario.
        None : Si el DNI no existe (no debería ocurrir si se usa tras el login).
    """
    if dni in usuarios:
        return usuarios[dni]
    return None


# -----------------------------------------------------------------------------
# SECCIÓN 5: PUNTO DE ENTRADA - BLOQUE PRINCIPAL
# -----------------------------------------------------------------------------
# Este bloque solo se ejecuta si corremos este archivo directamente.
# Cuando los compañeros importen este módulo, este bloque NO se ejecuta.
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # Llamamos a la función de login y guardamos el resultado
    dni_activo = login()

    # Verificamos si el login fue exitoso
    if dni_activo is not None:
        # Login exitoso: mostramos confirmación y el DNI activo
        # (Los demás módulos recibirán este dni_activo para operar)
        datos = obtener_datos_usuario(dni_activo)
        print(f"\n  [Sistema] Sesión iniciada para DNI: {dni_activo}")
        print(f"  [Sistema] Saldo actual: $ {datos['saldo']:,.2f}")
    else:
        # Login fallido o cancelado
        print("\n  [Sistema] No se pudo iniciar sesión. Programa finalizado.")