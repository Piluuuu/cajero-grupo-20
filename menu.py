# =============================================================================
#  SIMULADOR DE CAJERO AUTOMÁTICO — UTN FRRE | Algoritmos y Estructuras 2026
#  INTEGRANTE 4: Benítez Mauro Dante
#  Módulo: Menú principal, gestión de errores y calidad
# ============================================================================= 

# Importaciones de los módulos de los demás integrantes
from autenticacion import login                          # Integrante 1 - Veron Romero Pilar
from transacciones import depositar, extraer            # Integrante 2 - Veron Ana Paula
from consultas import consultar_saldo, realizar_transferencia, mostrar_historial_sesion  # Integrante 3 -  Sosa Lopez Milena


# =============================================================================
#  FUNCIONES DE MENSAJES ESTANDARIZADOS
#  Garantizan que todo el sistema use el mismo formato de alertas al usuario.
# =============================================================================

def mostrar_separador(titulo=""):
    """Imprime un separador visual con título opcional."""
    ancho = 48
    print()
    print("  " + "=" * ancho)
    if titulo:
        print(f"  {titulo.center(ancho)}")
        print("  " + "=" * ancho)

def mostrar_error(mensaje):
    """Alerta de error estandarizada para todo el sistema."""
    print(f"\n  [ERROR] {mensaje}")

def mostrar_advertencia(mensaje):
    """Alerta de advertencia estandarizada para todo el sistema."""
    print(f"\n  [ATENCION] {mensaje}")

def mostrar_exito(mensaje):
    """Mensaje de operación exitosa estandarizado para todo el sistema."""
    print(f"\n  [OK] {mensaje}")


# =============================================================================
#  MENÚ PRINCIPAL INTERACTIVO
# =============================================================================

def mostrar_opciones_menu():
    """Imprime las opciones disponibles del menú."""
    mostrar_separador("MENU PRINCIPAL")
    print("  1. Consultar saldo")
    print("  2. Depositar")
    print("  3. Extraer")
    print("  4. Transferir")
    print("  5. Ver historial de operaciones")
    print("  6. Cerrar sesion")
    print("  " + "-" * 48)

def menu_principal(usuario_activo):
    """
    Bucle principal del cajero para el usuario autenticado.
    Conecta las funciones de los cuatro integrantes.
    Permanece activo hasta que el usuario elige cerrar sesion.
    """
    while True:
        mostrar_opciones_menu()

        opcion = input("  Seleccione una opcion (1-6): ").strip()

        if opcion == "1":
            consultar_saldo(usuario_activo)          # Integrante 3 - Milena

        elif opcion == "2":
            depositar(usuario_activo)                # Integrante 2 - Ana Paula

        elif opcion == "3":
            extraer(usuario_activo)                  # Integrante 2 - Ana Paula

        elif opcion == "4":
            realizar_transferencia(usuario_activo)   # Integrante 3 - Milena

        elif opcion == "5":
            mostrar_historial_sesion(usuario_activo) # Integrante 3 - Milena

        elif opcion == "6":
            mostrar_historial_sesion(usuario_activo)
            mostrar_separador("CIERRE DE SESION")
            mostrar_exito("Sesion cerrada correctamente. Hasta pronto.")
            break

        else:
            mostrar_advertencia("Opcion invalida. Ingrese un numero del 1 al 6.")


# =============================================================================
#  PANTALLA DE BIENVENIDA Y FLUJO GENERAL
# =============================================================================

def pantalla_bienvenida():
    """Muestra la pantalla de inicio del sistema."""
    print()
    print("  +--------------------------------------------------+")
    print("  |     SIMULADOR DE CAJERO AUTOMATICO               |")
    print("  |     UTN - Facultad Regional Resistencia          |")
    print("  |     Algoritmos y Estructuras de Datos - 2026     |")
    print("  |     Comision ISI B K1.2  -  Grupo N 20           |")
    print("  +--------------------------------------------------+")
    print()

def main():
    """
    Funcion principal del sistema.
    Controla el flujo general: bienvenida -> login -> menu -> cierre.
    Permite iniciar una nueva sesion sin cerrar el programa.
    """
    pantalla_bienvenida()

    while True:
        # Login a cargo del Integrante 1 - Pilar
        usuario_activo = login()

        if usuario_activo:
            menu_principal(usuario_activo)
        else:
            mostrar_error("No se pudo iniciar sesion.")

        # Opcion de nueva sesion al terminar
        print()
        continuar = input("  Desea iniciar una nueva sesion? (s/n): ").strip().lower()
        if continuar != "s":
            mostrar_separador()
            print("  Gracias por usar nuestro cajero. Hasta pronto.")
            print()
            break


if __name__ == "__main__":
    main()
