


# Versión 3 - Completa con eliminación de clientes
# Programa para consultorio odontológico
# Horarios: 7am,8am,9am,10am,11am,12pm,2pm,3pm,4pm,5pm,6pm
# TELÉFONO: EXACTAMENTE 10 DÍGITOS
# ELIMINAR CLIENTES - OPCIONES SIMPLIFICADAS

import datetime
import re

# ==========================================
# CONSTANTES Y CONFIGURACIÓN
# ==========================================

# Precios base por tipo de cliente
PRECIOS_CITA = {
    "Particular": 80000,
    "EPS": 5000,
    "Prepagada": 30000
}

# Precios de atención por tipo de cliente y procedimiento
PRECIOS_ATENCION = {
    "Particular": {
        "Limpieza": 60000,
        "Calzas": 80000,
        "Extracción": 100000,
        "Diagnóstico": 50000
    },
    "EPS": {
        "Limpieza": 0,
        "Calzas": 40000,
        "Extracción": 40000,
        "Diagnóstico": 0
    },
    "Prepagada": {
        "Limpieza": 0,
        "Calzas": 10000,
        "Extracción": 10000,
        "Diagnóstico": 0
    }
}

# Horarios disponibles según la imagen
HORARIOS_DISPONIBLES = [
    "7:00am",
    "8:00am",
    "9:00am",
    "10:00am",
    "11:00am",
    "12:00pm",
    "14:00pm",
    "15:00pm",
    "16:00pm",
    "17:00pm",
    "18:00pm"
]

# Mapeo de horarios a formato 24h para almacenamiento
HORARIO_FORMATO_24H = {
    "7:00am": "07:00",
    "8:00am": "08:00",
    "9:00am": "09:00",
    "10:00am": "10:00",
    "11:00am": "11:00",
    "12:00pm": "12:00",
    "14:00pm": "14:00",
    "15:00pm": "15:00",
    "16:00pm": "16:00",
    "17:00pm": "17:00",
    "18:00pm": "18:00"
}

# Duración de cada atención en horas
DURACION_ATENCION = 1

# Días feriados fijos en Colombia (mes, día)
FERIADOS = [
    (1, 1),   # Año nuevo
    (5, 1),   # Día del trabajo
    (7, 20),  # Independencia
    (8, 7),   # Batalla de Boyacá
    (10, 12), # Día de la raza
    (11, 1),  # Día de todos los santos
    (12, 8),  # Inmaculada concepción
    (12, 25)  # Navidad
]

# Lista para almacenar todos los clientes
clientes = []

# Diccionario para almacenar citas ocupadas por fecha y hora
citas_ocupadas = {}  # Formato: {"DD/MM/AAAA HH:MM": True}

# ==========================================
# FUNCIONES DE VALIDACIÓN
# ==========================================

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

def normalizar_nombre(nombre):
    """
    Normaliza el nombre:
    - Elimina espacios extras
    - Convierte a título (primera letra mayúscula)
    """
    nombre = nombre.strip()
    nombre = re.sub(r'\s+', ' ', nombre)  # Espacios múltiples a uno solo
    return nombre.title()  # Juan Perez

def validar_nombre(mensaje):
    """Valida que el nombre no contenga números y lo normaliza"""
    while True:
        nombre = input(mensaje).strip()
        if not nombre:
            print("El nombre no puede estar vacío")
            continue
        
        # Verificar que no tenga números
        if any(caracter.isdigit() for caracter in nombre):
            print("Error: El nombre no debe contener números")
            continue
        
        # Normalizar nombre
        nombre_normalizado = normalizar_nombre(nombre)
        
        return nombre_normalizado

def validar_telefono(mensaje):
    """
    Valida que el teléfono tenga EXACTAMENTE 10 dígitos y solo números
    Estándar colombiano: 10 dígitos (ej: 3123456789)
    """
    while True:
        telefono = input(mensaje).strip()
        
        # Validar que no esté vacío
        if not telefono:
            print("Error: El teléfono no puede estar vacío")
            continue
        
        # Validar que solo contenga números
        if not telefono.isdigit():
            print("Error: El teléfono solo debe contener números (sin espacios, guiones ni símbolos)")
            continue
        
        # Validar longitud exacta de 10 dígitos
        if len(telefono) != 10:
            print(f"Error: El teléfono debe tener EXACTAMENTE 10 dígitos")
            print(f"        Usted ingresó {len(telefono)} dígito(s): {telefono}")
            print(f"        Ejemplo válido: 3123456789")
            continue
        
        # Validar que no comience con 0
        if telefono[0] == '0':
            print("Error: El teléfono no puede comenzar con 0")
            print("        Ejemplo válido: 3123456789")
            continue
        
        # Validar formato colombiano
        primer_digito = int(telefono[0])
        if primer_digito not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print(f"Error: El teléfono debe comenzar con un dígito válido (1-8)")
            print("        Colombia: 3 para móvil, 1-8 para fijo")
            continue
        
        # Formatear para mejor presentación
        telefono_formateado = f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}"
        print(f"✓ Teléfono válido: {telefono_formateado}")
        
        return telefono

def validar_cedula_unica(mensaje, clientes_existentes, cedula_actual=None):
    """Valida que la cédula no esté duplicada y solo contenga números"""
    while True:
        cedula = input(mensaje).strip()
        if not cedula:
            print("La cédula no puede estar vacía")
            continue
        
        if not cedula.isdigit():
            print("Error: La cédula solo debe contener números")
            continue
        
        # Validar longitud de cédula colombiana (6-10 dígitos)
        if len(cedula) < 6 or len(cedula) > 10:
            print("Error: La cédula debe tener entre 6 y 10 dígitos")
            continue
        
        # Verificar duplicado
        duplicado = False
        for cliente in clientes_existentes:
            if cliente["cedula"] == cedula:
                if cedula_actual is None or cedula_actual != cedula:
                    print(f"Error: La cédula {cedula} ya está registrada")
                    print(f"       Cliente asociado: {cliente['nombre']}")
                    duplicado = True
                    break
        
        if not duplicado:
            return cedula

def es_feriado(dia, mes, anio):
    """Verifica si una fecha es feriado"""
    for f_mes, f_dia in FERIADOS:
        if mes == f_mes and dia == f_dia:
            return True
    return False

def es_domingo(anio, mes, dia):
    """Verifica si una fecha es domingo"""
    fecha = datetime.date(anio, mes, dia)
    return fecha.weekday() == 6  # 6 = domingo

def validar_fecha(mensaje):
    """
    Valida que la fecha sea posterior o igual a la fecha actual
    No incluye domingos ni feriados
    """
    while True:
        fecha_str = input(mensaje)
        try:
            dia, mes, anio = map(int, fecha_str.split('/'))
            
            # Validar rango de día y mes
            if mes < 1 or mes > 12:
                print("Error: Mes inválido (1-12)")
                continue
            
            # Validar días según mes
            dias_por_mes = [31, 29 if (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0) else 28, 
                          31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            
            if dia < 1 or dia > dias_por_mes[mes-1]:
                print(f"Error: Día inválido para el mes {mes}")
                continue
            
            fecha_ingresada = datetime.date(anio, mes, dia)
            fecha_actual = datetime.date.today()
            
            # Validar que no sea menor a la fecha actual
            if fecha_ingresada < fecha_actual:
                print("Error: La fecha no puede ser menor al día actual")
                continue
            
            # Validar que no sea domingo
            if es_domingo(anio, mes, dia):
                print("Error: No se agendan citas los domingos")
                continue
            
            # Validar que no sea feriado
            if es_feriado(dia, mes, anio):
                print("Error: No se agendan citas en días feriados")
                continue
            
            return fecha_str
            
        except ValueError:
            print("Error: Formato inválido. Use DD/MM/AAAA")

def generar_horas_disponibles(fecha_str):
    """
    Genera lista de horas disponibles para una fecha específica
    Usa los horarios predefinidos de la imagen
    """
    horas_disponibles = []
    
    for horario in HORARIOS_DISPONIBLES:
        hora_24 = HORARIO_FORMATO_24H[horario]
        clave_cita = f"{fecha_str} {hora_24}"
        
        # Verificar si la cita ya está ocupada
        if clave_cita not in citas_ocupadas:
            horas_disponibles.append(horario)
    
    return horas_disponibles

def validar_horario_con_menu(fecha_str):
    """
    Muestra un menú con las horas disponibles para la fecha seleccionada
    Permite al usuario escoger una hora
    """
    while True:
        horas_disponibles = generar_horas_disponibles(fecha_str)
        
        if not horas_disponibles:
            print("\n" + "="*50)
            print("❌ NO HAY HORAS DISPONIBLES PARA ESTA FECHA")
            print("="*50)
            print("Todas las horas están ocupadas o no hay horarios disponibles")
            print("Por favor, seleccione otra fecha")
            print("="*50)
            return None
        
        print("\n" + "="*50)
        print("HORARIOS DISPONIBLES PARA LA CITA")
        print("="*50)
        
        for i, hora in enumerate(horas_disponibles, 1):
            print(f"{i:2d}. {hora}")
        
        print(f"{len(horas_disponibles) + 1:2d}. Volver a seleccionar fecha")
        print("="*50)
        
        opcion = validar_opcion("\nSeleccione una hora: ", 1, len(horas_disponibles) + 1)
        
        if opcion == len(horas_disponibles) + 1:
            return None  # Volver a seleccionar fecha
        
        hora_seleccionada = horas_disponibles[opcion - 1]
        hora_24 = HORARIO_FORMATO_24H[hora_seleccionada]
        
        # Confirmar hora
        print(f"\n✓ Hora seleccionada: {hora_seleccionada}")
        confirmar = input("¿Confirmar esta hora? (s/n): ").lower()
        
        if confirmar == 's':
            # Marcar la cita como ocupada
            clave_cita = f"{fecha_str} {hora_24}"
            citas_ocupadas[clave_cita] = True
            return hora_24  # Retornar en formato 24h para almacenar

# ==========================================
# FUNCIONES DE ORDENAMIENTO Y BÚSQUEDA
# ==========================================

def ordenar_por_valor_atencion(lista_clientes):
    """
    Ordena los clientes por valor de atención de mayor a menor
    Retorna una nueva lista ordenada
    """
    return sorted(lista_clientes, key=lambda x: x["valor_atencion"], reverse=True)

def buscar_por_cedula(lista_ordenada, cedula):
    """
    Búsqueda binaria en lista ordenada por cédula
    """
    # Ordenar por cédula para búsqueda binaria
    lista_por_cedula = sorted(lista_ordenada, key=lambda x: x["cedula"])
    
    izquierda, derecha = 0, len(lista_por_cedula) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        cedula_medio = lista_por_cedula[medio]["cedula"]
        
        if cedula_medio == cedula:
            return lista_por_cedula[medio]
        elif cedula_medio < cedula:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    
    return None

# ==========================================
# FUNCIONES DE GESTIÓN DE CLIENTES
# ==========================================

def eliminar_cliente():
    """
    Elimina un cliente registrado por su cédula
    """
    if len(clientes) == 0:
        print("\n⚠️ No hay clientes registrados para eliminar")
        return False
    
    print("\n" + "="*50)
    print("ELIMINAR CLIENTE")
    print("="*50)
    
    # Mostrar lista de clientes
    print("\n--- CLIENTES REGISTRADOS ---")
    for i, c in enumerate(clientes, 1):
        telefono_formateado = f"{c['telefono'][:3]} {c['telefono'][3:6]} {c['telefono'][6:]}"
        print(f"{i:2d}. {c['cedula']} - {c['nombre']} - {telefono_formateado} - {c['fecha']} {c['hora']}")
    
    print("\n" + "-"*50)
    
    # Solicitar cédula a eliminar
    cedula_eliminar = input("Ingrese la cédula del cliente a eliminar: ").strip()
    
    # Buscar el cliente
    cliente_encontrado = None
    indice_encontrado = -1
    
    for i, cliente in enumerate(clientes):
        if cliente["cedula"] == cedula_eliminar:
            cliente_encontrado = cliente
            indice_encontrado = i
            break
    
    if cliente_encontrado is None:
        print(f"\n❌ No se encontró ningún cliente con cédula {cedula_eliminar}")
        return False
    
    # Mostrar información del cliente a eliminar
    telefono_formateado = f"{cliente_encontrado['telefono'][:3]} {cliente_encontrado['telefono'][3:6]} {cliente_encontrado['telefono'][6:]}"
    
    print("\n" + "-"*40)
    print("CLIENTE A ELIMINAR:")
    print("-"*40)
    print(f"Cédula:          {cliente_encontrado['cedula']}")
    print(f"Nombre:          {cliente_encontrado['nombre']}")
    print(f"Teléfono:        {telefono_formateado}")
    print(f"Tipo cliente:    {cliente_encontrado['tipo']}")
    print(f"Atención:        {cliente_encontrado['atencion']}")
    print(f"Fecha cita:      {cliente_encontrado['fecha']}")
    print(f"Hora cita:       {cliente_encontrado['hora']}")
    print(f"Total a pagar:   ${cliente_encontrado['total']:,.0f}")
    print("-"*40)
    
    # Confirmar eliminación
    print("\n⚠️ ADVERTENCIA: Esta acción no se puede deshacer")
    confirmar = input("¿Está seguro de eliminar este cliente? (s/n): ").lower()
    
    if confirmar != 's':
        print("\n✓ Eliminación cancelada")
        return False
    
    # Liberar la hora de la cita en citas_ocupadas
    clave_cita = f"{cliente_encontrado['fecha']} {cliente_encontrado['hora_24']}"
    if clave_cita in citas_ocupadas:
        del citas_ocupadas[clave_cita]
        print("✓ Hora de cita liberada")
    
    # Eliminar cliente de la lista
    cliente_eliminado = clientes.pop(indice_encontrado)
    
    print("\n" + "="*40)
    print(f"✓ CLIENTE ELIMINADO EXITOSAMENTE")
    print("="*40)
    print(f"Cliente: {cliente_eliminado['nombre']} (Cédula: {cliente_eliminado['cedula']})")
    print("="*40)
    
    return True

def editar_cliente():
    """
    Edita los datos de un cliente existente
    """
    if len(clientes) == 0:
        print("\n⚠️ No hay clientes registrados para editar")
        return False
    
    print("\n" + "="*50)
    print("EDITAR CLIENTE")
    print("="*50)
    
    # Mostrar lista de clientes
    print("\n--- CLIENTES REGISTRADOS ---")
    for i, c in enumerate(clientes, 1):
        telefono_formateado = f"{c['telefono'][:3]} {c['telefono'][3:6]} {c['telefono'][6:]}"
        print(f"{i:2d}. {c['cedula']} - {c['nombre']} - {telefono_formateado}")
    
    print("\n" + "-"*50)
    
    # Solicitar cédula a editar
    cedula_editar = input("Ingrese la cédula del cliente a editar: ").strip()
    
    # Buscar el cliente
    cliente_encontrado = None
    indice_encontrado = -1
    
    for i, cliente in enumerate(clientes):
        if cliente["cedula"] == cedula_editar:
            cliente_encontrado = cliente
            indice_encontrado = i
            break
    
    if cliente_encontrado is None:
        print(f"\n❌ No se encontró ningún cliente con cédula {cedula_editar}")
        return False
    
    print("\n" + "="*40)
    print("EDITANDO CLIENTE:")
    print("="*40)
    print(f"Cédula: {cliente_encontrado['cedula']}")
    print(f"Nombre actual: {cliente_encontrado['nombre']}")
    print("="*40)
    
    # Liberar la hora actual antes de editar
    clave_cita_actual = f"{cliente_encontrado['fecha']} {cliente_encontrado['hora_24']}"
    if clave_cita_actual in citas_ocupadas:
        del citas_ocupadas[clave_cita_actual]
    
    # Capturar nuevos datos
    print("\n--- INGRESE LOS NUEVOS DATOS ---")
    print("(Deje en blanco para mantener el valor actual)")
    
    # Nombre
    nuevo_nombre = input(f"Nombre [{cliente_encontrado['nombre']}]: ").strip()
    if nuevo_nombre:
        nombre = validar_nombre("Nombre completo: ")
    else:
        nombre = cliente_encontrado['nombre']
    
    # Teléfono
    nuevo_telefono = input(f"Teléfono [{cliente_encontrado['telefono']}]: ").strip()
    if nuevo_telefono:
        telefono = validar_telefono("Teléfono (10 dígitos): ")
    else:
        telefono = cliente_encontrado['telefono']
    
    # Tipo de cliente
    print("\n--- Tipo de Cliente ---")
    print("1. Particular")
    print("2. EPS")
    print("3. Prepagada")
    print(f"Actual: {cliente_encontrado['tipo']}")
    cambiar_tipo = input("¿Cambiar tipo de cliente? (s/n): ").lower()
    if cambiar_tipo == 's':
        tipo_op = validar_opcion("Seleccione: ", 1, 3)
        tipos = ["", "Particular", "EPS", "Prepagada"]
        tipo = tipos[tipo_op]
    else:
        tipo = cliente_encontrado['tipo']
    
    # Tipo de atención
    print("\n--- Tipo de Atención ---")
    print("1. Limpieza")
    print("2. Calzas")
    print("3. Extracción")
    print("4. Diagnóstico")
    print(f"Actual: {cliente_encontrado['atencion']}")
    cambiar_atencion = input("¿Cambiar tipo de atención? (s/n): ").lower()
    if cambiar_atencion == 's':
        atencion_op = validar_opcion("Seleccione: ", 1, 4)
        atenciones = ["", "Limpieza", "Calzas", "Extracción", "Diagnóstico"]
        atencion = atenciones[atencion_op]
        
        # Cantidad (según tipo de atención)
        if atencion in ["Limpieza", "Diagnóstico"]:
            cantidad = 1
            print(f"Cantidad: {cantidad} (valor fijo para {atencion})")
        else:
            cantidad = validar_cantidad("Cantidad: ")
    else:
        atencion = cliente_encontrado['atencion']
        cantidad = cliente_encontrado['cantidad']
    
    # Prioridad
    print("\n--- Prioridad ---")
    print("1. Normal")
    print("2. Urgente")
    print(f"Actual: {cliente_encontrado['prioridad']}")
    cambiar_prioridad = input("¿Cambiar prioridad? (s/n): ").lower()
    if cambiar_prioridad == 's':
        prioridad_op = validar_opcion("Seleccione: ", 1, 2)
        prioridades = ["", "Normal", "Urgente"]
        prioridad = prioridades[prioridad_op]
    else:
        prioridad = cliente_encontrado['prioridad']
    
    # Fecha y hora
    print(f"\nFecha actual: {cliente_encontrado['fecha']}")
    print(f"Hora actual: {cliente_encontrado['hora']}")
    cambiar_fecha = input("¿Cambiar fecha/hora de cita? (s/n): ").lower()
    
    if cambiar_fecha == 's':
        while True:
            fecha = validar_fecha("Fecha de la cita (DD/MM/AAAA): ")
            hora = validar_horario_con_menu(fecha)
            if hora:
                break
    else:
        fecha = cliente_encontrado['fecha']
        hora = cliente_encontrado['hora_24']
    
    # Convertir hora a formato am/pm para mostrar
    hora_mostrar = None
    for key, value in HORARIO_FORMATO_24H.items():
        if value == hora:
            hora_mostrar = key
            break
    
    # Cálculo del valor
    valor_cita = PRECIOS_CITA[tipo]
    valor_atencion = PRECIOS_ATENCION[tipo][atencion]
    total_pagar = valor_cita + (valor_atencion * cantidad)
    
    # Actualizar cliente
    clientes[indice_encontrado] = {
        "cedula": cedula_editar,
        "nombre": nombre,
        "telefono": telefono,
        "tipo": tipo,
        "atencion": atencion,
        "cantidad": cantidad,
        "prioridad": prioridad,
        "fecha": fecha,
        "hora": hora_mostrar,
        "hora_24": hora,
        "valor_cita": valor_cita,
        "valor_atencion": valor_atencion,
        "total": total_pagar
    }
    
    print("\n" + "="*40)
    print("✓ CLIENTE EDITADO EXITOSAMENTE")
    print("="*40)
    
    return True

# ==========================================
# FUNCIÓN DE CAPTURA DE CLIENTE
# ==========================================

def capturar_cliente(clientes_existentes, cedula_editar=None):
    """
    Captura los datos de un cliente y calcula el valor a pagar
    """
    print("\n" + "="*50)
    print("REGISTRO DE NUEVO CLIENTE" if cedula_editar is None else "EDITAR CLIENTE")
    print("="*50)
    
    # Datos básicos con validaciones
    while True:
        cedula = validar_cedula_unica("Cédula: ", clientes_existentes, cedula_editar)
        if cedula:
            break
        print("Por favor, ingrese una cédula diferente")
    
    nombre = validar_nombre("Nombre completo: ")
    telefono = validar_telefono("Teléfono (10 dígitos): ")
    
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
    
    # Fecha y hora (con selección interactiva)
    while True:
        fecha = validar_fecha("Fecha de la cita (DD/MM/AAAA): ")
        hora = validar_horario_con_menu(fecha)
        if hora:
            break
    
    # Convertir hora a formato am/pm para mostrar
    hora_mostrar = None
    for key, value in HORARIO_FORMATO_24H.items():
        if value == hora:
            hora_mostrar = key
            break
    
    # Cálculo del valor
    valor_cita = PRECIOS_CITA[tipo]
    valor_atencion = PRECIOS_ATENCION[tipo][atencion]
    total_pagar = valor_cita + (valor_atencion * cantidad)
    
    # Mostrar resumen
    print("\n" + "-"*40)
    print("RESUMEN DE LA CITA")
    print("-"*40)
    print(f"Fecha:             {fecha}")
    print(f"Hora:              {hora_mostrar}")
    print(f"Tipo cliente:      {tipo}")
    print(f"Atención:          {atencion}")
    print(f"Cantidad:          {cantidad}")
    print(f"Prioridad:         {prioridad}")
    print("-"*40)
    print(f"Valor de la cita:  ${valor_cita:>10,.0f}")
    print(f"Valor de atención: ${valor_atencion:>10,.0f} x {cantidad}")
    print(f"TOTAL A PAGAR:     ${total_pagar:>10,.0f}")
    print("-"*40)
    
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
        "hora": hora_mostrar,
        "hora_24": hora,
        "valor_cita": valor_cita,
        "valor_atencion": valor_atencion,
        "total": total_pagar
    }

# ==========================================
# FUNCIONES DE ESTADÍSTICAS Y LISTADO
# ==========================================

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
    print(f"📊 Total Clientes:        {total_clientes}")
    print(f"💰 Ingresos totales:      ${ingresos_totales:>12,.0f}")
    print(f"🦷 Clientes extracción:   {extracciones}")
    print("="*50)

def mostrar_lista_clientes(filtro_prioridad=None):
    """
    Muestra los clientes registrados en formato tabla
    filtro_prioridad: "Normal", "Urgente" o None para todos
    """
    if len(clientes) == 0:
        print("\n⚠️ No hay clientes registrados")
        return
    
    # Aplicar filtro si existe
    if filtro_prioridad:
        clientes_filtrados = [c for c in clientes if c["prioridad"] == filtro_prioridad]
        if len(clientes_filtrados) == 0:
            print(f"\n⚠️ No hay clientes con prioridad {filtro_prioridad}")
            return
        titulo = f"LISTA DE CLIENTES - PRIORIDAD: {filtro_prioridad}"
    else:
        clientes_filtrados = clientes
        titulo = "LISTA DE TODOS LOS CLIENTES"
    
    print("\n" + "="*130)
    print(titulo)
    print("="*130)
    print(f"{'Cédula':<12} {'Nombre':<25} {'Teléfono':<12} {'Atención':<12} {'Prioridad':<10} {'Fecha':<12} {'Hora':<10} {'Valor At':>12} {'Total':>12}")
    print("-"*130)
    
    for c in clientes_filtrados:
        # Formatear teléfono para mostrar
        telefono_formateado = f"{c['telefono'][:3]} {c['telefono'][3:6]} {c['telefono'][6:]}"
        print(f"{c['cedula']:<12} {c['nombre']:<25} {telefono_formateado:<12} {c['atencion']:<12} {c['prioridad']:<10} {c['fecha']:<12} {c['hora']:<10} ${c['valor_atencion']:>10,.0f} ${c['total']:>10,.0f}")
    
    print("="*130)

def mostrar_clientes_ordenados():
    """Muestra los clientes ordenados por valor de atención (mayor a menor)"""
    if len(clientes) == 0:
        print("\n⚠️ No hay clientes registrados")
        return
    
    clientes_ordenados = ordenar_por_valor_atencion(clientes)
    
    print("\n" + "="*120)
    print("CLIENTES ORDENADOS POR VALOR DE ATENCIÓN (MAYOR A MENOR)")
    print("="*120)
    print(f"{'Cédula':<12} {'Nombre':<25} {'Atención':<12} {'Prioridad':<10} {'Valor Atención':>15} {'Total':>12}")
    print("-"*120)
    
    for c in clientes_ordenados:
        print(f"{c['cedula']:<12} {c['nombre']:<25} {c['atencion']:<12} {c['prioridad']:<10} ${c['valor_atencion']:>12,.0f} ${c['total']:>10,.0f}")
    
    print("="*120)
    return clientes_ordenados

def buscar_cliente_por_cedula():
    """Busca un cliente por cédula en la lista ordenada por valor de atención"""
    if len(clientes) == 0:
        print("\n⚠️ No hay clientes registrados")
        return
    
    # Primero ordenamos por valor de atención (requisito)
    clientes_ordenados = ordenar_por_valor_atencion(clientes)
    
    cedula_buscar = input("\nIngrese la cédula a buscar: ")
    
    # Buscar en la lista ordenada
    encontrado =