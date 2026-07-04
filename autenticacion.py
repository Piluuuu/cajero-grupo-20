# =============================================================================
# SIMULADOR DE CAJERO AUTOMÁTICO
# Materia: Algoritmos y Estructuras de Datos - UTN FRRe
# =============================================================================


# -----------------------------------------------------------------------------
# SECCIÓN 1: ESTRUCTURA DE DATOS DE USUARIOS
# -----------------------------------------------------------------------------

usuarios = {
    "48399733": {
        "pin":        "1234",
        "nombre":     "Pilar Verón Romero",
        "saldo":      150000.00,
        "intentos":   0,
        "bloqueado":  False,
        "operaciones": []
    },
    "87654321": {
        "pin":        "4321",
        "nombre":     "Mauro Benitez",
        "saldo":      75500.50,
        "intentos":   0,
        "bloqueado":  False,
        "operaciones": []
    },
    "11223344": {
        "pin":        "0000",
        "nombre":     "Ana Paula Verón",
        "saldo":      200000.00,
        "intentos":   0,
        "bloqueado":  False,
        "operaciones": []
    },
    "29032008": {
        "pin":        "5678",
        "nombre":     "Milena Sosa",
        "saldo":      3000.00,
        "intentos":   0,
        "bloqueado":  False,
        "operaciones": []
    }
}

MAX_INTENTOS       = 3
LIMITE_EXTRACCION  = 50000.00  # Límite máximo por operación de extracción


# =============================================================================
# INTEGRANTE 1 - LOGIN Y VALIDACIONES
# =============================================================================

def validar_dni(dni_ingresado):
    """
    Valida que el DNI ingresado tenga exactamente 8 dígitos y exista en el sistema.
    """
    if len(dni_ingresado) != 8 or not dni_ingresado.isdigit():
        print("  [!] El DNI debe tener exactamente 8 dígitos numéricos.")
        return False
    if dni_ingresado not in usuarios:
        print("  [!] DNI no encontrado en el sistema.")
        return False
    return True


def validar_pin(pin_ingresado):
    """
    Valida que el PIN tenga exactamente 4 dígitos numéricos.
    """
    if len(pin_ingresado) != 4 or not pin_ingresado.isdigit():
        print("  [!] El PIN debe tener exactamente 4 dígitos numéricos.")
        return False
    return True


def login():
    """
    Gestiona el inicio de sesión: solicita DNI y PIN, controla intentos y bloqueo.
    Retorna el DNI del usuario autenticado, o None si falló.
    """
    print("=" * 50)
    print("     BIENVENIDO AL CAJERO AUTOMÁTICO")
    print("=" * 50)

    # PASO 1: Solicitar y validar el DNI
    dni = ""
    dni_valido = False
    while not dni_valido:
        print("\nIngrese su DNI (8 dígitos) o escriba 'salir' para cancelar:")
        dni = input("  DNI: ").strip()
        if dni.lower() == "salir":
            print("\n  Operación cancelada. ¡Hasta luego!")
            return None
        dni_valido = validar_dni(dni)

    # PASO 2: Verificar si la cuenta está bloqueada
    if usuarios[dni]["bloqueado"]:
        print("\n  [X] La cuenta asociada al DNI ingresado está BLOQUEADA.")
        print("      Comuníquese con el banco para desbloquearla.")
        return None

    usuario_actual = usuarios[dni]

    # PASO 3: Bucle de verificación del PIN
    while usuario_actual["intentos"] < MAX_INTENTOS:
        intentos_restantes = MAX_INTENTOS - usuario_actual["intentos"]
        print(f"\n  Intentos restantes: {intentos_restantes}")
        print("  Ingrese su PIN de 4 dígitos:")
        pin_ingresado = input("  PIN: ").strip()

        if not validar_pin(pin_ingresado):
            continue

        if pin_ingresado == usuario_actual["pin"]:
            usuario_actual["intentos"] = 0
            print("\n" + "=" * 50)
            print(f"  ¡Bienvenido/a, {usuario_actual['nombre']}!")
            print("=" * 50)
            return dni
        else:
            usuario_actual["intentos"] += 1
            if usuario_actual["intentos"] < MAX_INTENTOS:
                print("  [!] PIN incorrecto. Verifique e intente nuevamente.")
            else:
                usuario_actual["bloqueado"] = True
                print("\n  [X] Ha superado el número máximo de intentos.")
                print("      Su cuenta ha sido BLOQUEADA por seguridad.")
                print("      Comuníquese con el banco para desbloquearla.")
                return None

    return None


def obtener_datos_usuario(dni):
    """Retorna el diccionario de datos del usuario dado su DNI."""
    if dni in usuarios:
        return usuarios[dni]
    return None


# =============================================================================
# INTEGRANTE 2 - TRANSACCIONES MONETARIAS
# =============================================================================

def registrar_operacion(dni, tipo, monto):
    """
    Agrega una entrada al historial de operaciones del usuario.

    Parámetros:
        dni   (str)  : DNI del usuario activo.
        tipo  (str)  : Descripción de la operación ("Extracción", "Depósito", etc.)
        monto (float): Monto de la operación (negativo para débitos).
    """
    registro = {
        "tipo":              tipo,
        "monto":             monto,
        "saldo_resultante":  usuarios[dni]["saldo"]
    }
    usuarios[dni]["operaciones"].append(registro)


def consultar_saldo(dni):
    """Muestra el saldo actual del usuario activo."""
    print("\n" + "-" * 40)
    print("          CONSULTA DE SALDO")
    print("-" * 40)
    print(f"  Titular : {usuarios[dni]['nombre']}")
    print(f"  Saldo   : $ {usuarios[dni]['saldo']:,.2f}")
    print("-" * 40)


def extraer(dni):
    """
    Solicita un monto y lo descuenta del saldo del usuario.
    Validaciones:
      - Formato numérico.
      - Mayor a cero.
      - No supera el límite máximo por operación (LIMITE_EXTRACCION).
      - No supera el saldo disponible (control de saldo insuficiente).
    Retorna True si la operación fue exitosa, False si fue cancelada.
    """
    print("\n" + "-" * 40)
    print("             EXTRACCIÓN")
    print("-" * 40)
    print(f"  Saldo disponible        : $ {usuarios[dni]['saldo']:,.2f}")
    print(f"  Límite máximo operación : $ {LIMITE_EXTRACCION:,.2f}")

    while True:
        entrada = input("\n  Monto a extraer (0 para cancelar): $ ").strip()

        # Validar formato numérico
        try:
            monto = float(entrada)
        except ValueError:
            print("  [!] Error: ingrese un valor numérico válido.")
            continue

        # Cancelar
        if monto == 0:
            print("  Operación cancelada.")
            return False

        # Validar positivo
        if monto < 0:
            print("  [!] Error: el monto debe ser mayor a cero.")
            continue

        # Validar límite máximo
        if monto > LIMITE_EXTRACCION:
            print(f"  [!] Error: supera el límite máximo de $ {LIMITE_EXTRACCION:,.2f} por operación.")
            continue

        # Validar saldo suficiente
        if monto > usuarios[dni]["saldo"]:
            print(f"  [!] Error: saldo insuficiente. Su saldo es $ {usuarios[dni]['saldo']:,.2f}.")
            continue

        # Ejecutar extracción
        usuarios[dni]["saldo"] -= monto
        registrar_operacion(dni, "Extracción", -monto)
        print(f"\n  ✔ Extracción exitosa de $ {monto:,.2f}")
        print(f"  Nuevo saldo: $ {usuarios[dni]['saldo']:,.2f}")
        return True


def depositar(dni):
    """
    Solicita un monto y lo acredita al saldo del usuario.
    Validaciones:
      - Formato numérico.
      - Mayor a cero.
    Retorna True si la operación fue exitosa, False si fue cancelada.
    """
    print("\n" + "-" * 40)
    print("              DEPÓSITO")
    print("-" * 40)
    print(f"  Saldo actual: $ {usuarios[dni]['saldo']:,.2f}")

    while True:
        entrada = input("\n  Monto a depositar (0 para cancelar): $ ").strip()

        # Validar formato numérico
        try:
            monto = float(entrada)
        except ValueError:
            print("  [!] Error: ingrese un valor numérico válido.")
            continue

        # Cancelar
        if monto == 0:
            print("  Operación cancelada.")
            return False

        # Validar positivo
        if monto < 0:
            print("  [!] Error: el monto debe ser mayor a cero.")
            continue

        # Ejecutar depósito
        usuarios[dni]["saldo"] += monto
        registrar_operacion(dni, "Depósito", +monto)
        print(f"\n  ✔ Depósito exitoso de $ {monto:,.2f}")
        print(f"  Nuevo saldo: $ {usuarios[dni]['saldo']:,.2f}")
        return True


# =============================================================================
# MENÚ PRINCIPAL (une ambas partes)
# =============================================================================

def menu(dni):
    """
    Muestra el menú de operaciones y deriva a cada función.
    Se ejecuta en bucle hasta que el usuario elige salir.
    """
    salir = False
    while not salir:
        print("\n" + "=" * 40)
        print("           MENÚ PRINCIPAL")
        print("=" * 40)
        print("  1 - Consultar saldo")
        print("  2 - Extraer dinero")
        print("  3 - Depositar dinero")
        print("  4 - Cerrar sesión")
        print("=" * 40)

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            consultar_saldo(dni)
        elif opcion == "2":
            extraer(dni)
        elif opcion == "3":
            depositar(dni)
        elif opcion == "4":
            print(f"\n  Sesión cerrada. ¡Hasta luego, {usuarios[dni]['nombre']}!")
            salir = True
        else:
            print("  [!] Opción inválida. Ingrese un número del 1 al 4.")


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    dni_activo = login()

    if dni_activo is not None:
        menu(dni_activo)
    else:
        print("\n  [Sistema] No se pudo iniciar sesión. Programa finalizado.")
