# Simulador de Cajero Automático

**Trabajo Final Integrador — Laboratorio de Python**  
**Algoritmos y Estructuras de Datos | UTN - Facultad Regional Resistencia | Ciclo 2026**

---

## Integrantes del grupo

| N° | Nombre | Módulo desarrollado |
|----|--------|---------------------|
| 1 | Veron Romero Pilar | Autenticación, seguridad y datos iniciales |
| 2 | Veron Ana Paula | Transacciones monetarias (extracción y depósito) |
| 3 | Sosa Lopez Milena| Consultas, transferencias e historial de operaciones |
| 4 | Benítez Mauro Dante | Menú principal, gestión de errores y calidad |

---

## Comisión

**ISI B K1.2 — Grupo N° 20**

---

## Descripción general del sistema

El sistema simula el funcionamiento básico de un cajero automático por consola. Permite a los usuarios autenticarse con DNI y PIN, y acceder a un menú interactivo desde el cual pueden:

- Consultar el saldo disponible en su cuenta
- Depositar dinero
- Extraer dinero, con control de saldo insuficiente y límite máximo por operación
- Transferir fondos a otras cuentas registradas en el sistema
- Ver el historial de operaciones realizadas durante la sesión

El sistema incluye bloqueo de cuenta tras 3 intentos fallidos de PIN, mensajes de error estandarizados y un registro de movimientos con contadores y acumuladores.

---

## Instrucciones de ejecución

### Requisitos previos

- Tener instalado **Python 3.8 o superior**
- No se requieren librerías externas

### Pasos para ejecutar

1. Clonar el repositorio o descargar todos los archivos `.py` en una misma carpeta
2. Abrir una terminal en esa carpeta
3. Ejecutar el archivo principal con el siguiente comando:

```bash
python menu.py
```

> En algunos sistemas puede ser necesario usar `python3` en lugar de `python`.

## Cuentas de prueba (DNI y PIN)

Para evaluar el correcto funcionamiento del simulador, se encuentran precargadas las siguientes cuentas en el sistema:

| Titular (Integrante) | DNI de acceso | PIN de seguridad | Saldo Inicial |
|-----------------------|---------------|------------------|---------------|
| Pilar Verón Romero    | `48399733`    | `1234`           | $ 150,000.00  |
| Ana Paula Verón       | `11223344`    | `0000`           | $ 120,000.00  |
| Milena Sosa           | `29032008`    | `1000`           | $ 100,000.00  |
| Mauro Benitez         | `87654321`    | `4321`           | $ 200,000.00  |

---

## Registro de uso de Inteligencia Artificial

### Integrante 1 — Pilar | Herramienta: Claude AI

**Estructuración inicial:**  
Se utilizó Claude AI para proponer la estructura de datos lógica (diccionario de diccionarios) para almacenar los usuarios del cajero con sus contraseñas y saldos iniciales.

**Lógica de bucles:**  
Se utilizó para diseñar el flujo del bucle `while` que controla el límite estricto de 3 intentos del PIN antes de bloquear la cuenta.

**Validación:**  
Se utilizó para asegurar que el programa verifique correctamente si el DNI ingresado existe en el sistema antes de solicitar la contraseña.

**Adaptación realizada:**  
El código generado por la IA fue adaptado para que la función `login()` retorne el DNI del usuario activo como un string, permitiendo que los módulos de los demás integrantes (extracción, depósito, transferencias) identifiquen correctamente qué cuenta está operando, sin necesidad de usar clases u objetos avanzados.

---

### Integrante 2 — Ana Paula | Herramienta: Claude AI

**Estructuración inicial:**  
Se utilizó Claude AI para proponer la estructura de datos del diccionario `usuarios`, que almacena PIN, nombre, saldo, intentos fallidos, estado de bloqueo e historial de operaciones de cada cuenta.

**Lógica de bucles:**  
Se utilizó para diseñar el flujo del bucle `while` en la función `login()` que controla el límite de 3 intentos fallidos comparando contra la constante `MAX_INTENTOS`.

**Validación:**  
Se utilizó para estructurar las funciones `validar_dni()` y `validar_pin()`, asegurando que verifiquen la cantidad de dígitos correcta y que sean numéricos mediante `.isdigit()`, además de comprobar si el DNI existe en el sistema antes de pedir la contraseña.

**Adaptación realizada:**  
El código generado por la IA fue adaptado para que la función `login()` retorne el DNI como string (o `None` si falla), de manera que el menú principal reciba ese valor y se lo pase como parámetro a las funciones `consultar_saldo`, `extraer` y `depositar`, identificando correctamente qué cuenta está operando sin necesidad de variables globales ni estructuras avanzadas.

---

### Integrante 3 — Milena | Herramienta: Claude AI

> •Estructuración inicial: Para estructurar un sistema de control local mediante variables globales de seguimiento (⁠historial_movimientos⁠ como lista, contadores enteros para consultas y transferencias, y un acumulador de tipo float para el total de dinero transferido).

 •Lógica de bucles: Para diseñar el recorrido del historial mediante un bucle ⁠for⁠ que itera sobre la lista de movimientos de la sesión, imprimiendo de manera secuencial cada operación registrada.

 •Validación: Para asegurar que la transferencia sea blindada mediante condicionales ⁠if⁠ que verifican que la cuenta destino exista en la base de datos simulada, que el usuario no intente transferirse a sí mismo, y que el monto ingresado sea un número flotante válido mayor a cero y no supere el saldo disponible.
 
 •Adaptación: Se adaptó el código para interactuar directamente con la estructura de almacenamiento actualizando los saldos de forma simultánea (restando al usuario activo y sumando a la cuenta destino), registrando tanto las operaciones exitosas como los intentos fallidos en el historial antes de actualizar los acumuladores de control.

---

### Integrante 4 — Benítez Mauro Dante | Herramienta: Claude AI

**Diseño del menú principal:**  
Se utilizó Claude AI para proponer la estructura del menú interactivo con bucle `while` y condicionales `if/elif`, que conecta las funciones de los cuatro módulos y mantiene la sesión activa hasta que el usuario decide cerrarla.

**Adaptación realizada:**  
El código sugerido fue adaptado para que el menú reciba el DNI del usuario activo como parámetro (retornado por `login()`) y lo pase a cada función de los otros módulos, en lugar de usar una variable global. Esto permite que todas las operaciones trabajen sobre la cuenta correcta de forma ordenada y modular.

**Estandarización de mensajes:**  
Se utilizó la IA para proponer las funciones `mostrar_error()`, `mostrar_advertencia()` y `mostrar_exito()` como funciones centralizadas de formato.

**Adaptación realizada:**  
Se ajustaron los prefijos y el formato de los mensajes para que sean claros, coherentes y reconocibles en toda la consola (`[ERROR]`, `[ATENCION]`, `[OK]`), reemplazando las versiones con símbolos especiales que no se visualizan correctamente en todas las terminales.

---

## Estructura del repositorio

```
/
├── menu.py          # Módulo 4: Menú principal y flujo general (Mauro)
├── autenticacion.py # Módulo 1: Login y seguridad (Pilar)
├── transacciones.py # Módulo 2: Depósito y extracción (Ana Paula)
├── consultas.py     # Módulo 3: Saldo, transferencias e historial (Milena)
└── README.md        # Este archivo
```

---

*Trabajo desarrollado con fines académicos — UTN FRRE 2026*
