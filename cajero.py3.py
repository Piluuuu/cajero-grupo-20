# =============================================================================
# SIMULADOR DE CAJERO AUTOMÁTICO
# Materia: Algoritmos y Estructuras de Datos - UTN FRRe
#
# INTEGRANTE 3 - CONSULTAS, TRANSFERENCIAS Y REGISTROS
# =============================================================================
#
# Este archivo contiene ÚNICAMENTE las funciones que me corresponden como
# Integrante 3. Está pensado para pegarse dentro del archivo integrado del
# grupo, a continuación de las secciones de Integrante 1 (login) e
# Integrante 2 (transacciones).
#
# DEPENDENCIAS de este módulo (ya definidas por mis compañeras, no
# duplicar):
#   - Diccionario "usuarios"            -> definido en la Sección 1
#   - registrar_operacion(dni, tipo, monto) -> función de Ana Paula (Integrante 2),
#     se usa acá para dejar registro permanente de cada transferencia.
#
# Para que este archivo también pueda probarse SOLO (sin el resto del
# proyecto), más abajo incluyo una copia mínima del diccionario "usuarios"
# y de "registrar_operacion". Al integrar todo, esas partes NO se duplican,
# se usan las que ya están en el archivo principal.
# =============================================================================


# -----------------------------------------------------------------------------
# Bloque de prueba standalone (usuarios + registrar_operacion)
# Al integrar con el resto del grupo, ESTE BLOQUE SE ELIMINA porque ya
# existe en las secciones de Pilar y Ana Paula.
# -----------------------------------------------------------------------------
usuarios = {
    "48399733": {"pin": "1234", "nombre": "Pilar Verón Romero", "saldo": 150000.00,
                 "intentos": 0, "bloqueado": False, "operaciones": []},
    "87654321": {"pin": "4321", "nombre": "Mauro Benitez",       "saldo": 75500.50,
                 "intentos": 0, "bloqueado": False, "operaciones": []},
    "11223344": {"pin": "0000", "nombre": "Ana Paula Verón",     "saldo": 200000.00,
                 "intentos": 0, "bloqueado": False, "operaciones": []},
    "29032008": {"pin": "5678", "nombre": "Milena Sosa",         "saldo": 3000.00,
                 "intentos": 0, "bloqueado": False, "operaciones": []}
}


def registrar_operacion(dni, tipo, monto):
    """(Función de Ana Paula - se incluye acá solo para poder probar sola esta parte)."""
    registro = {
        "tipo":             tipo,
        "monto":            monto,
        "saldo_resultante": usuarios[dni]["saldo"]
    }
    usuarios[dni]["operaciones"].append(registro)
# -----------------------------------------------------------------------------
# FIN del bloque de prueba standalone
# -----------------------------------------------------------------------------


# =============================================================================
# MI PARTE: variables globales para el registro de la sesión
# (contadores / acumuladores, tal como pide la consigna)
# =============================================================================
historial_sesion      = []     # Lista con cada movimiento realizado en esta sesión
contador_operaciones  = 0      # Acumulador: cantidad total de operaciones realizadas
total_extraido        = 0.0    # Acumulador: total extraído en la sesión
total_depositado       = 0.0   # Acumulador: total depositado en la sesión
total_transferido      = 0.0   # Acumulador: total transferido (enviado) en la sesión


def reiniciar_sesion():
    """
    Reinicia el historial y los acumuladores de sesión.

    IMPORTANTE ("efecto memoria"): como historial_sesion, contador_operaciones,
    total_extraido, total_depositado y total_transferido son variables
    globales, si el cajero corre en un bucle atendiendo a varios usuarios uno
    tras otro, estas variables NO se borran solas entre un usuario y el
    siguiente. Sin este reinicio, el segundo usuario vería mezclados los
    movimientos y totales de la sesión del usuario anterior con los suyos.

    Por eso esta función debe llamarse SIEMPRE al principio de menu(dni),
    es decir, apenas arranca cada sesión nueva (antes de mostrar el menú).
    """
    global historial_sesion, contador_operaciones
    global total_extraido, total_depositado, total_transferido

    historial_sesion     = []
    contador_operaciones = 0
    total_extraido        = 0.0
    total_depositado      = 0.0
    total_transferido     = 0.0


def registrar_movimiento_sesion(tipo, monto):
    """
    Registra un movimiento en el historial de la SESIÓN ACTUAL y actualiza
    los acumuladores correspondientes según el tipo de operación.

    Esta función debe llamarse también desde extraer() y depositar()
    (funciones de Ana Paula) para que el historial de sesión quede completo,
    no solo con las transferencias.

    Parámetros:
        tipo  (str)  : "Extracción", "Depósito", "Transferencia enviada"
                       o "Transferencia recibida".
        monto (float): monto de la operación (negativo si es un débito).
    """
    global contador_operaciones, total_extraido, total_depositado, total_transferido

    contador_operaciones += 1

    historial_sesion.append({
        "nro":   contador_operaciones,
        "tipo":  tipo,
        "monto": monto
    })

    if tipo == "Extracción":
        total_extraido += abs(monto)
    elif tipo == "Depósito":
        total_depositado += monto
    elif tipo == "Transferencia enviada":
        total_transferido += abs(monto)
    # "Transferencia recibida" queda en el historial, pero no suma a
    # total_transferido (ese acumulador es solo para lo que el usuario envía).


def ver_historial_sesion():
    """
    Muestra por pantalla todos los movimientos realizados durante la sesión
    actual, junto con los totales acumulados por tipo de operación.
    """
    print("\n" + "-" * 40)
    print("      HISTORIAL DE LA SESIÓN ACTUAL")
    print("-" * 40)

    if contador_operaciones == 0:
        print("  Aún no realizó ninguna operación en esta sesión.")
    else:
        for mov in historial_sesion:
            signo = "+" if mov["monto"] >= 0 else "-"
            print(f"  {mov['nro']}. {mov['tipo']:<22} $ {signo}{abs(mov['monto']):,.2f}")

        print("-" * 40)
        print(f"  Total de operaciones     : {contador_operaciones}")
        print(f"  Total extraído           : $ {total_extraido:,.2f}")
        print(f"  Total depositado         : $ {total_depositado:,.2f}")
        print(f"  Total transferido        : $ {total_transferido:,.2f}")

    print("-" * 40)


def transferir(dni_origen):
    """
    Transfiere dinero desde la cuenta del usuario activo (dni_origen) hacia
    otra cuenta existente en el sistema.

    Validaciones:
      - La cuenta destino debe existir y no puede ser la misma que la de origen.
      - El monto debe tener formato numérico válido y ser mayor a cero.
      - Debe haber saldo suficiente en la cuenta de origen.

    Retorna:
        True  si la transferencia se realizó con éxito.
        False si fue cancelada o no pudo completarse.
    """
    print("\n" + "-" * 40)
    print("             TRANSFERENCIA")
    print("-" * 40)
    print(f"  Saldo disponible: $ {usuarios[dni_origen]['saldo']:,.2f}")

    # --- Paso 1: solicitar y validar la cuenta destino ---
    while True:
        dni_destino = input("\n  DNI de la cuenta destino (0 para cancelar): ").strip()

        if dni_destino == "0":
            print("  Operación cancelada.")
            return False

        if len(dni_destino) != 8 or not dni_destino.isdigit():
            print("  [!] El DNI debe tener exactamente 8 dígitos numéricos.")
            continue

        if dni_destino not in usuarios:
            print("  [!] La cuenta destino no existe en el sistema.")
            continue

        if dni_destino == dni_origen:
            print("  [!] No puede transferirse dinero a su propia cuenta.")
            continue

        break  # DNI destino válido

    # --- Paso 2: solicitar y validar el monto ---
    while True:
        entrada = input("  Monto a transferir (0 para cancelar): $ ").strip()

        try:
            monto = float(entrada)
        except ValueError:
            print("  [!] Error: ingrese un valor numérico válido.")
            continue

        if monto == 0:
            print("  Operación cancelada.")
            return False

        if monto < 0:
            print("  [!] Error: el monto debe ser mayor a cero.")
            continue

        if monto > usuarios[dni_origen]["saldo"]:
            print(f"  [!] Error: saldo insuficiente. Su saldo es $ {usuarios[dni_origen]['saldo']:,.2f}.")
            continue

        break  # Monto válido

    # --- Paso 3: ejecutar la transferencia ---
    usuarios[dni_origen]["saldo"]  -= monto
    usuarios[dni_destino]["saldo"] += monto

    # Registro en el historial permanente de cada cuenta (función de Ana Paula)
    registrar_operacion(dni_origen,  "Transferencia enviada",  -monto)
    registrar_operacion(dni_destino, "Transferencia recibida", +monto)

    # Registro en el historial de la sesión (solo afecta al usuario logueado)
    registrar_movimiento_sesion("Transferencia enviada", -monto)

    print(f"\n  ✔ Transferencia exitosa de $ {monto:,.2f}")
    print(f"  Destinatario : {usuarios[dni_destino]['nombre']}")
    print(f"  Nuevo saldo  : $ {usuarios[dni_origen]['saldo']:,.2f}")
    return True


# =============================================================================
# Prueba rápida standalone de mi parte (se elimina al integrar con el grupo)
#
# Simulo DOS sesiones seguidas (como en el cajero real) para comprobar que,
# gracias a reiniciar_sesion(), el historial de un usuario NO se mezcla
# con el del siguiente.
# =============================================================================
if __name__ == "__main__":
    print("=== SESIÓN 1: Pilar transfiere $5000 a Mauro ===")
    reiniciar_sesion()          # <-- se llama al empezar CADA sesión
    transferir("48399733")
    ver_historial_sesion()

    print("\n\n=== SESIÓN 2: entra Mauro (no hizo nada todavía) ===")
    reiniciar_sesion()          # <-- reinicia antes de que opere el siguiente usuario
    ver_historial_sesion()      # debería estar vacío, NO mostrar la transferencia de Pilar
