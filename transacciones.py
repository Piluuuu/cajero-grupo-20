# =============================================================================
# INTEGRANTE 2: Ana Paula Verón - Módulo: Transacciones Monetarias
# =============================================================================

from cajero import usuarios
from menu import mostrar_error, mostrar_exito, mostrar_advertencia

def registrar_operacion(dni, tipo_operacion, monto):
    """Registra la transacción en la lista de operaciones del usuario."""
    usuarios[dni]["operaciones"].append({
        "tipo": tipo_operacion,
        "monto": monto
    })

def depositar(dni_activo):
    print("\n  --- OPERACIÓN: DEPÓSITO ---")
    monto_ingresado = input("  Ingrese el monto a depositar: $ ").strip()

    if not monto_ingresado.isdigit() or float(monto_ingresado) <= 0:
        mostrar_error("Monto inválido. Ingrese un valor numérico mayor a cero.")
        return

    monto = float(monto_ingresado)
    usuarios[dni_activo]["saldo"] += monto
    registrar_operacion(dni_activo, "Depósito", monto)
    
    mostrar_exito(f"Depósito exitoso. Nuevo saldo: $ {usuarios[dni_activo]['saldo']:,.2f}")

def extraer(dni_activo):
    print("\n  --- OPERACIÓN: EXTRACCIÓN ---")
    monto_ingresado = input("  Ingrese el monto a extraer: $ ").strip()

    if not monto_ingresado.isdigit() or float(monto_ingresado) <= 0:
        mostrar_error("Monto inválido. Ingrese un valor numérico mayor a cero.")
        return

    monto = float(monto_ingresado)

    LIMITE_CAJERO = 50000.00
    if monto > LIMITE_CAJERO:
        mostrar_advertencia(f"El límite máximo de extracción por operación es de $ {LIMITE_CAJERO:,.2f}")
        return

    if monto > usuarios[dni_activo]["saldo"]:
        mostrar_error("Saldo insuficiente para realizar la extracción.")
        return

    usuarios[dni_activo]["saldo"] -= monto
    registrar_operacion(dni_activo, "Extracción", monto)
    
    mostrar_exito(f"Retire su dinero. Saldo restante: $ {usuarios[dni_activo]['saldo']:,.2f}")