
"""
# problemas que presenta la version 2
-No ordena por valor atención (mes,dia,hora)
-No valida cédulas duplicadas
-No valida cédulas duplicadas
-No normaliza los nombres
-No valida longitud mínima de teléfono (10 digitos)
-No hay opción de ver solo clientes urgentes,o cita normal
-eliminar clientes registrado

"""



# Versión 2 
# Programa para consultorio odontológico

import datetime


# CONFIGURACIÓN DE PRECIOS


# Tablas de precios
precios_cita = { "Particular": 80000,"EPS": 5000,"Prepagada": 30000 }

precios_atencion = {
    "Particular": {"Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
    "EPS": {"Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0},
    "Prepagada": {"Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0}
}

# Lista para almacenar clientes
clientes = []

# FUNCIONES DE VALIDACIÓN

def validar_opcion(mensaje, min_op, max_op):
    """Valida que la opción ingresada esté dentro del rango permitido"""
    while True:
        try:
            op = int(input(mensaje))
            if min_op <= op <= max_op:
                return op
            print(f"Opción inválida. Debe ser entre {min_op} y {max_op}")
        except ValueError:
            print("Error: Debe ingresar un número")

def validar_cantidad(mensaje):
    """Valida que la cantidad sea un número positivo"""
    while True:
        try:
            cantidad = int(input(mensaje))
            if cantidad > 0:
                return cantidad
            print("La cantidad debe ser mayor a 0")
        except ValueError:
            print("Error: Debe ingresar un número")

def validar_nombre(mensaje):
    """Valida que el nombre no contenga números"""
    while True:
        nombre = input(mensaje).strip()
        if not nombre:
            print("El nombre no puede estar vacío")
            continue
        
        # Verificar que no tenga números
        if any(caracter.isdigit() for caracter in nombre):
            print("Error: El nombre no debe contener números")
            continue
        
        return nombre

def validar_fecha(mensaje):
    """
    Valida que la fecha sea posterior o igual a la fecha actual
    Formato esperado: DD/MM/AAAA
    """
    while True:
        fecha_str = input(mensaje)
        try:
            dia, mes, anio = map(int, fecha_str.split('/'))
            fecha_ingresada = datetime.date(anio, mes, dia)
            fecha_actual = datetime.date.today()
            
            if fecha_ingresada < fecha_actual:
                print("Error: La fecha no puede ser menor al día actual")
                continue
            
            return fecha_str
        except ValueError:
            print("Error: Formato inválido. Use DD/MM/AAAA")

def validar_telefono(mensaje):
    """Valida que el teléfono solo contenga números"""
    while True:
        telefono = input(mensaje).strip()
        if not telefono:
            print("El teléfono no puede estar vacío")
            continue
        
        if not telefono.isdigit():
            print("Error: El teléfono solo debe contener números")
            continue
        
        return telefono

def validar_cedula(mensaje):
    """Valida que la cédula solo contenga números"""
    while True:
        cedula = input(mensaje).strip()
        if not cedula:
            print("La cédula no puede estar vacía")
            continue
        
        if not cedula.isdigit():
            print("Error: La cédula solo debe contener números")
            continue
        
        return cedula


# FUNCIÓN DE CAPTURA DE CLIENTE


def capturar_cliente():
    """
    Captura los datos de un cliente y calcula el valor a pagar
    """
    print("\n" + "="*50)
    print("REGISTRO DE NUEVO CLIENTE")
    print("="*50)
    
    # Datos básicos con validaciones
    cedula = validar_cedula("Cédula: ")
    nombre = validar_nombre("Nombre completo: ")
    telefono = validar_telefono("Teléfono: ")
    
    # Tipo de cliente
    print("\n--- Tipo de Cliente ---")
    print("1. Particular")
    print("2. EPS")
    print("3. Prepagada")
    tipo_op = validar_opcion("Seleccione: ", 1, 3)
    tipos = ["", "Particular", "EPS", "Prepagada"]
    tipo = tipos[tipo_op]
    
    # Tipo de atención
    print("\n--- Tipo de Atención ---")
    print("1. Limpieza")
    print("2. Calzas")
    print("3. Extracción")
    print("4. Diagnóstico")
    atencion_op = validar_opcion("Seleccione: ", 1, 4)
    atenciones = ["", "Limpieza", "Calzas", "Extracción", "Diagnóstico"]
    atencion = atenciones[atencion_op]
    
    # Cantidad (según tipo de atención)
    if atencion in ["Limpieza", "Diagnóstico"]:
        cantidad = 1
        print(f"Cantidad: {cantidad} (valor fijo para {atencion})")
    else:
        cantidad = validar_cantidad("Cantidad: ")
    
    # Prioridad
    print("\n--- Prioridad ---")
    print("1. Normal")
    print("2. Urgente")
    prioridad_op = validar_opcion("Seleccione: ", 1, 2)
    prioridades = ["", "Normal", "Urgente"]
    prioridad = prioridades[prioridad_op]
    
    # Fecha con validación (no menor al día actual)
    fecha = validar_fecha("Fecha de la cita (DD/MM/AAAA): ")
    
    # Cálculo del valor
    valor_cita = precios_cita[tipo]
    valor_atencion = precios_atencion[tipo][atencion]
    total_pagar = valor_cita + (valor_atencion * cantidad)
    
    # Mostrar resumen
    print("\n" + "-"*30)
    print(f"Valor de la cita: ${valor_cita:,.0f}")
    print(f"Valor de atención: ${valor_atencion:,.0f} x {cantidad}")
    print(f"TOTAL A PAGAR: ${total_pagar:,.0f}")
    print("-"*30)
    
    # Retornar diccionario con todos los datos
    return {
        "cedula": cedula,
        "nombre": nombre,
        "telefono": telefono,
        "tipo": tipo,
        "atencion": atencion,
        "cantidad": cantidad,
        "prioridad": prioridad,
        "fecha": fecha,
        "valor_cita": valor_cita,
        "valor_atencion": valor_atencion,
        "total": total_pagar
    }


# FUNCIONES DE ESTADÍSTICAS Y LISTADO


def mostrar_estadisticas():
    """Muestra las estadísticas requeridas"""
    if len(clientes) == 0:
        print("\n⚠️ No hay clientes registrados")
        return
    
    total_clientes = len(clientes)
    ingresos_totales = sum(c["total"] for c in clientes)
    extracciones = sum(1 for c in clientes if c["atencion"] == "Extracción")
    
    print("\n" + "="*50)
    print("ESTADÍSTICAS DEL CONSULTORIO")
    print("="*50)
    print(f"📊 Total Clientes: {total_clientes}")
    print(f"💰 Ingresos totales: ${ingresos_totales:,.0f}")
    print(f"🦷 Clientes para extracción: {extracciones}")
    print("="*50)

def mostrar_lista_clientes():
    """Muestra todos los clientes registrados en formato tabla"""
    if len(clientes) == 0:
        print("\n⚠️ No hay clientes registrados")
        return
    
    print("\n" + "="*90)
    print("LISTA DE CLIENTES REGISTRADOS")
    print("="*90)
    print(f"{'Cédula':<12} {'Nombre':<25} {'Atención':<12} {'Fecha':<12} {'Total':>12}")
    print("-"*90)
    
    for c in clientes:
        print(f"{c['cedula']:<12} {c['nombre']:<25} {c['atencion']:<12} {c['fecha']:<12} ${c['total']:>10,.0f}")
    
    print("="*90)

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

print("\n" + "="*50)
print("BIENVENIDO AL CONSULTORIO ODONTOLÓGICO")
print("="*50)

# Solicitar número de clientes a registrar
while True:
    try:
        n = int(input("\n¿Cuántos clientes desea registrar? "))
        if n > 0:
            break
        print("Debe registrar al menos 1 cliente")
    except ValueError:
        print("Error: Debe ingresar un número válido")

# Registrar clientes
for i in range(n):
    print(f"\n--- Cliente {i+1} de {n} ---")
    clientes.append(capturar_cliente())
    print(f"\n✓ Cliente {i+1} registrado exitosamente")

# Mostrar estadísticas
mostrar_estadisticas()

# Mostrar lista completa
mostrar_lista_clientes()

# ==========================================
# MENÚ PARA AGREGAR MÁS CLIENTES
# ==========================================

print("\n" + "="*50)
print("MENÚ ADICIONAL")
print("="*50)
print("1. Agregar más clientes")
print("2. Salir")

op = validar_opcion("Seleccione: ", 1, 2)

if op == 1:
    while True:
        try:
            n2 = int(input("\n¿Cuántos clientes más desea registrar? "))
            if n2 > 0:
                for i in range(n2):
                    clientes.append(capturar_cliente())
                break
            print("Debe registrar al menos 1 cliente")
        except ValueError:
            print("Error: Debe ingresar un número válido")

# Mostrar estadísticas actualizadas
mostrar_estadisticas()
mostrar_lista_clientes()

# ==========================================
# FIN DEL PROGRAMA
# ==========================================

print("\n" + "="*50)
print("PROGRAMA FINALIZADO")
print(f"Total clientes registrados: {len(clientes)}")
print(f"Ingresos totales: ${sum(c['total'] for c in clientes):,.0f}")
print("="*50)

