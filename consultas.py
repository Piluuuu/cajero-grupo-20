# =============================================================================
# INTEGRANTE 3: Milena Sosa - Módulo: Consultas, Transferencias y Registros
# =============================================================================

from cajero import usuarios
from transacciones import registrar_operacion
from menu import mostrar_error, mostrar_exito, mostrar_advertencia, mostrar_separador

# Historial de la sesión activa en memoria volatil (pedido en su consigna)
historial_sesion = []

def reiniciar_sesion():
    """Limpia el historial de la sesión al cambiar de usuario."""
    global historial_sesion
    historial_sesion = []

def registrar_movimiento_sesion(tipo, monto):
    """Guarda localmente las acciones de la sesión actual."""
    historial_sesion.append({"tipo": tipo, "monto": monto})

def consultar_saldo(dni_activo):
    mostrar_separador("SALDO DISPONIBLE")
    print(f"  Titular: {usuarios[dni_activo]['nombre']}")
    print(f"  Saldo actual: $ {usuarios[dni_activo]['saldo']:,.2f}")
    registrar_movimiento_sesion("Consulta de saldo", 0)

def realizar_transferencia(dni_origen):
    print("\n  --- OPERACIÓN: TRANSFERENCIA ---")
    dni_destino = input("  Ingrese el DNI de la cuenta destino (8 dígitos): ").strip()

    if dni_destino not in usuarios:
        mostrar_error("La cuenta destino no existe en el sistema.")
        return

    if dni_destino == dni_origen:
        mostrar_advertencia("No puede transferir dinero a su propia cuenta.")
        return

    monto_ingresado = input("  Ingrese el monto a transferir: $ ").strip()
    if not monto_ingresado.isdigit() or float(monto_ingresado) <= 0:
        mostrar_error("Monto inválido.")
        return

    monto = float(monto_ingresado)

    if monto > usuarios[dni_origen]["saldo"]:
        mostrar_error("Saldo insuficiente para realizar la transferencia.")
        return

    # Realizar el traspaso de dinero
    usuarios[dni_origen]["saldo"] -= monto
    usuarios[dni_destino]["saldo"] += monto

    # Registros permanentes (módulo Ana Paula)# Corrección en consultas.py:
    registrar_operacion(dni_origen, "Transferencia enviada", -monto) # Descuento al origen
    registrar_operacion(dni_destino, "Transferencia recibida", monto) # <-- CAMBIAR "-monto" POR "monto" (positivo para el destino)

    # Registro de sesión (módulo Milena)
    registrar_movimiento_sesion("Transferencia enviada", -monto)

    mostrar_exito(f"Transferencia exitosa de $ {monto:,.2f} a {usuarios[dni_destino]['nombre']}")

def mostrar_historial_sesion(dni_activo):
    mostrar_separador("HISTORIAL DE ESTA SESIÓN")
    
    if not historial_sesion:
        print("  No se registraron movimientos en esta sesión.")
        return

    for i, mov in enumerate(historial_sesion, 1):
        if mov["monto"] == 0:
            print(f"  {i}. {mov['tipo']}")
        else:
            print(f"  {i}. {mov['tipo']}: $ {mov['monto']:,.2f}")