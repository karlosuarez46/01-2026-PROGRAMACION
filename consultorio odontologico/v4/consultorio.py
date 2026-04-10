
## Programa para consultorio odontológico version 4

from datetime import datetime

# Tablas de precios
precios_cita = { "Particular": 80000, "EPS": 5000, "Prepagada": 30000 }

precios_atencion = { 
    "Particular": {"Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
    "EPS": {"Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0},
    "Prepagada": {"Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0}
}

# Horarios disponibles
horarios_disponibles = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]

# Base de datos
clientes_registrados = []  # Arreglo para almacenar todos los clientes
citas_agendadas = {}  # Control de horarios

# ==================== FUNCIONES DE VALIDACIÓN ====================

def validar_cedula(cedula):
    return cedula.isdigit() and len(cedula) > 0

def validar_cedula_unica(cedula):
    """Verifica que la cédula no esté ya registrada"""
    for cliente in clientes_registrados:
        if cliente["cedula"] == cedula:
            return False
    return True

def validar_nombre(nombre):
    return not any(char.isdigit() for char in nombre) and nombre.strip() != ""

def validar_telefono(telefono):
    return telefono.isdigit() and 7 <= len(telefono) <= 10

def validar_fecha_y_hora(fecha_str, hora_str=None):
    """
    Valida que la fecha sea válida y no sea anterior al día actual.
    Si se proporciona hora, valida que no sea una hora ya pasada para el día actual.
    """
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        fecha_actual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Validar que la fecha no sea anterior a hoy
        if fecha < fecha_actual:
            return False, "La fecha no puede ser anterior al día actual"
        
        # Si la fecha es hoy y se proporcionó hora, validar que la hora no haya pasado
        if fecha == fecha_actual and hora_str:
            hora_actual = datetime.now().strftime("%H:%M")
            if hora_str < hora_actual:
                return False, f"No se pueden agendar citas para una hora ya pasada ({hora_actual} actual)"
        
        return True, "OK"
    except ValueError:
        return False, "Formato de fecha inválido. Use DD/MM/AAAA"

def validar_fecha(fecha_str):
    """Versión simplificada para validar solo fecha (sin hora)"""
    valida, _ = validar_fecha_y_hora(fecha_str)
    return valida

def validar_opcion_menu(opcion, min_op, max_op):
    try:
        opcion_int = int(opcion)
        return min_op <= opcion_int <= max_op, opcion_int
    except ValueError:
        return False, None

def obtener_horarios_disponibles(fecha):
    """Obtiene horarios disponibles para una fecha específica, considerando la hora actual si es hoy"""
    disponibles = []
    
    for hora in horarios_disponibles:
        clave = f"{fecha} {hora}"
        
        # Verificar si el horario ya está ocupado
        if clave in citas_agendadas:
            continue
        
        # Si la fecha es hoy, verificar que la hora no haya pasado
        valida, mensaje = validar_fecha_y_hora(fecha, hora)
        if not valida and "hora ya pasada" in mensaje:
            continue
            
        disponibles.append(hora)
    
    return disponibles

def agendar_cita(fecha, hora, cedula):
    """Agenda una cita verificando que no esté ocupada"""
    clave = f"{fecha} {hora}"
    
    # Verificar si ya está ocupado (doble verificación por seguridad)
    if clave in citas_agendadas:
        return False, "El horario ya está ocupado"
    
    citas_agendadas[clave] = cedula
    return True, "Cita agendada exitosamente"

def cancelar_cita(fecha, hora):
    """Cancela una cita existente"""
    clave = f"{fecha} {hora}"
    if clave in citas_agendadas:
        del citas_agendadas[clave]
        return True
    return False

# ==================== FUNCIONES DE REGISTRO ====================

def registrar_cita():
    """Registrar una nueva cita"""
    print("\n" + "="*60)
    print("REGISTRO DE NUEVA CITA")
    print("="*60)
    
    # Validar cédula (única)
    while True:
        cedula = input("Cédula: ")
        if not validar_cedula(cedula):
            print("❌ Error: La cédula solo debe contener números.")
            continue
        
        if not validar_cedula_unica(cedula):
            print(f"❌ Error: La cédula {cedula} ya está registrada en el sistema.")
            opcion = input("¿Desea buscar este cliente? (s/n): ").lower()
            if opcion == 's':
                cliente = buscar_cliente_por_cedula(cedula)
                if cliente:
                    print(f"\n✅ Cliente encontrado: {cliente['nombre']}")
                    print("Puede registrar una nueva cita para este cliente.")
                else:
                    print("⚠️ Cliente no encontrado. Verifique la cédula.")
            continue
        
        break
    
    # Validar nombre
    while True:
        nombre = input("Nombre : ")
        if validar_nombre(nombre):
            break
        print("❌ Error: El nombre no debe contener números.")
    
    # Validar teléfono
    while True:
        telefono = input("Teléfono : ")
        if validar_telefono(telefono):
            break
        print("❌ Error: El teléfono debe tener entre 7 y 10 dígitos numéricos.")
    
    # Validar tipo de cliente
    while True:
        print("\nTIPO DE CLIENTE:")
        print("1. Particular")
        print("2. EPS")
        print("3. Prepagada")
        opcion = input("Opción: ")
        valida, tipo_opcion = validar_opcion_menu(opcion, 1, 3)
        if valida:
            if tipo_opcion == 1:
                tipo = "Particular"
            elif tipo_opcion == 2:
                tipo = "EPS"
            else:
                tipo = "Prepagada"
            break
        print("❌ Error: Opción inválida.")
    
    # Validar tipo de atención
    while True:
        print("\nTIPO DE ATENCIÓN:")
        print("1. Limpieza")
        print("2. Calzas")
        print("3. Extracción")
        print("4. Diagnóstico")
        opcion = input("Opción: ")
        valida, atencion_opcion = validar_opcion_menu(opcion, 1, 4)
        if valida:
            if atencion_opcion == 1:
                atencion = "Limpieza"
            elif atencion_opcion == 2:
                atencion = "Calzas"
            elif atencion_opcion == 3:
                atencion = "Extracción"
            else:
                atencion = "Diagnóstico"
            break
        print("❌ Error: Opción inválida.")
    
    # Cantidad
    if atencion in ["Limpieza", "Diagnóstico"]:
        cantidad = 1
        print(f"\nCantidad: {cantidad} (fijo para {atencion})")
    else:
        while True:
            try:
                cantidad = int(input(f"\nCantidad de {atencion.lower()}: "))
                if cantidad > 0:
                    break
                print("❌ Error: La cantidad debe ser mayor a 0.")
            except ValueError:
                print("❌ Error: Ingrese un número válido.")
    
    # Validar prioridad
    while True:
        print("\nPRIORIDAD:")
        print("1. Normal")
        print("2. Urgente")
        opcion = input("Opción: ")
        valida, prioridad_opcion = validar_opcion_menu(opcion, 1, 2)
        if valida:
            prioridad = "Normal" if prioridad_opcion == 1 else "Urgente"
            break
        print("❌ Error: Opción inválida.")
    
    # Validar fecha y hora
    while True:
        while True:
            fecha = input("\nFecha de la Cita (DD/MM/AAAA): ")
            valida, mensaje = validar_fecha_y_hora(fecha)
            if valida:
                break
            print(f"❌ Error: {mensaje}")
        
        # Obtener horarios disponibles
        horarios_disp = obtener_horarios_disponibles(fecha)
        
        if not horarios_disp:
            print(f"\n❌ No hay horarios disponibles para {fecha}")
            continue
        
        print(f"\nHorarios disponibles para {fecha}:")
        for i, hora in enumerate(horarios_disp, 1):
            print(f"{i}. {hora}")
        
        try:
            opcion_horario = int(input("Seleccione horario: "))
            if 1 <= opcion_horario <= len(horarios_disp):
                hora_seleccionada = horarios_disp[opcion_horario - 1]
                break
            else:
                print("❌ Error: Opción fuera de rango.")
        except ValueError:
            print("❌ Error: Ingrese un número válido.")
    
    # Calcular valor
    valor_cita = precios_cita[tipo]
    valor_atencion = precios_atencion[tipo][atencion]
    total_pagar = valor_cita + (valor_atencion * cantidad)
    
    # Guardar cliente
    cliente = {
        "cedula": cedula,
        "nombre": nombre,
        "telefono": telefono,
        "tipo": tipo,
        "atencion": atencion,
        "cantidad": cantidad,
        "prioridad": prioridad,
        "fecha": fecha,
        "hora": hora_seleccionada,
        "total": total_pagar
    }
    
    clientes_registrados.append(cliente)
    exito, mensaje = agendar_cita(fecha, hora_seleccionada, cedula)
    
    if not exito:
        print(f"\n❌ Error: {mensaje}")
        return None
    
    print("\n" + "="*60)
    print("✅ CITA REGISTRADA EXITOSAMENTE")
    print("="*60)
    print(f"Cliente: {nombre}")
    print(f"Cédula: {cedula}")
    print(f"Teléfono: {telefono}")
    print(f"Tipo: {tipo}")
    print(f"Atención: {atencion}")
    print(f"Cantidad: {cantidad}")
    print(f"Prioridad: {prioridad}")
    print(f"Fecha: {fecha}")
    print(f"Hora: {hora_seleccionada}")
    print(f"Valor a pagar: ${total_pagar:,.0f}")
    print("="*60)
    
    return cliente

# ==================== FUNCIONES DE BÚSQUEDA ====================

def buscar_cliente_por_cedula(cedula):
    """Busca un cliente por su cédula"""
    for cliente in clientes_registrados:
        if cliente["cedula"] == cedula:
            return cliente
    return None

def buscar_por_cedula_interactivo():
    """Función interactiva para buscar cliente por cédula"""
    if not clientes_registrados:
        print("\n📋 No hay clientes registrados.")
        input("\nPresione Enter para continuar...")
        return
    
    print("\n" + "="*60)
    print("BUSCAR CLIENTE POR CÉDULA")
    print("="*60)
    
    cedula = input("Ingrese la cédula a buscar: ")
    cliente = buscar_cliente_por_cedula(cedula)
    
    if cliente:
        print("\n" + "="*60)
        print("✅ CLIENTE ENCONTRADO")
        print("="*60)
        print(f"Nombre:     {cliente['nombre']}")
        print(f"Cédula:     {cliente['cedula']}")
        print(f"Teléfono:   {cliente['telefono']}")
        print(f"Tipo:       {cliente['tipo']}")
        print(f"Atención:   {cliente['atencion']}")
        print(f"Cantidad:   {cliente['cantidad']}")
        print(f"Prioridad:  {cliente['prioridad']}")
        print(f"Fecha:      {cliente['fecha']}")
        print(f"Hora:       {cliente['hora']}")
        print(f"Valor:      ${cliente['total']:,.0f}")
        print("="*60)
    else:
        print(f"\n❌ No se encontró ningún cliente con cédula {cedula}")
    
    input("\nPresione Enter para continuar...")

def buscar_clientes_por_prioridad():
    """Busca y muestra clientes por prioridad"""
    if not clientes_registrados:
        print("\n📋 No hay clientes registrados.")
        input("\nPresione Enter para continuar...")
        return
    
    print("\n" + "="*60)
    print("BUSCAR CLIENTES POR PRIORIDAD")
    print("="*60)
    print("1. Normal")
    print("2. Urgente")
    
    opcion = input("Seleccione prioridad: ")
    valida, prioridad_opcion = validar_opcion_menu(opcion, 1, 2)
    
    if not valida:
        print("❌ Opción inválida.")
        input("\nPresione Enter para continuar...")
        return
    
    prioridad_buscar = "Normal" if prioridad_opcion == 1 else "Urgente"
    clientes_filtrados = [c for c in clientes_registrados if c["prioridad"] == prioridad_buscar]
    
    if not clientes_filtrados:
        print(f"\n📋 No hay clientes con prioridad {prioridad_buscar}.")
    else:
        # Ordenar por fecha y hora también en la búsqueda por prioridad
        clientes_filtrados = sorted(clientes_filtrados, 
                                   key=lambda c: (datetime.strptime(c['fecha'], "%d/%m/%Y"), c['hora']))
        
        print(f"\n📋 CLIENTES CON PRIORIDAD {prioridad_buscar.upper()}:")
        print("="*60)
        for i, cliente in enumerate(clientes_filtrados, 1):
            print(f"\n{i}. {cliente['nombre']} - Cédula: {cliente['cedula']}")
            print(f"   Teléfono: {cliente['telefono']}")
            print(f"   Atención: {cliente['atencion']}")
            print(f"   Fecha: {cliente['fecha']} - Hora: {cliente['hora']}")
            print(f"   Valor: ${cliente['total']:,.0f}")
        print("="*60)
    
    input("\nPresione Enter para continuar...")

# ==================== FUNCIONES DE LISTADO Y ESTADÍSTICAS ====================

def listar_todos_clientes():
    """Muestra todos los clientes registrados ordenados por fecha y hora"""
    print("\n" + "="*60)
    print("📋 LISTADO COMPLETO DE CLIENTES")
    print("="*60)
    
    if not clientes_registrados:
        print("\n📋 No hay clientes registrados en el sistema.")
        print("Por favor, registre al menos un cliente primero.")
    else:
        # ✅ CORRECCIÓN PRINCIPAL: Ordenar por fecha y hora
        clientes_ordenados = sorted(clientes_registrados, 
                                   key=lambda c: (datetime.strptime(c['fecha'], "%d/%m/%Y"), c['hora']))
        
        print(f"\n✅ Total de clientes registrados: {len(clientes_registrados)}\n")
        
        for i, cliente in enumerate(clientes_ordenados, 1):
            print(f"\n--- CLIENTE {i} ---")
            print(f"  Nombre:     {cliente['nombre']}")
            print(f"  Cédula:     {cliente['cedula']}")
            print(f"  Teléfono:   {cliente['telefono']}")
            print(f"  Tipo:       {cliente['tipo']}")
            print(f"  Atención:   {cliente['atencion']}")
            print(f"  Cantidad:   {cliente['cantidad']}")
            print(f"  Prioridad:  {cliente['prioridad']}")
            print(f"  Fecha:      {cliente['fecha']}")
            print(f"  Hora:       {cliente['hora']}")
            print(f"  Valor:      ${cliente['total']:,.0f}")
            
            # No mostrar separador después del último cliente
            if i < len(clientes_ordenados):
                print("-"*60)
    
    input("\nPresione Enter para continuar...")

def mostrar_estadisticas():
    """Muestra estadísticas completas mejoradas"""
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DEL CONSULTORIO")
    print("="*60)
    
    if not clientes_registrados:
        print("\n📋 No hay clientes registrados para mostrar estadísticas.")
        print("Por favor, registre al menos un cliente primero.")
    else:
        # 1. Total de clientes
        total_clientes = len(clientes_registrados)
        print(f"\n✅ TOTAL DE CLIENTES ATENDIDOS: {total_clientes}")
        
        # 2. Ingresos totales recibidos
        ingresos_totales = sum(cliente["total"] for cliente in clientes_registrados)
        print(f"\n💰 INGRESOS TOTALES RECIBIDOS: ${ingresos_totales:,.0f}")
        
        # 3. Clientes para extracción de dientes
        clientes_extraccion = [c for c in clientes_registrados if c["atencion"] == "Extracción"]
        total_extraccion = len(clientes_extraccion)
        print(f"\n🦷 CLIENTES PARA EXTRACCIÓN DE DIENTES: {total_extraccion}")
        
        # 4. ✅ NUEVA ESTADÍSTICA: Promedio de ingresos por día
        fechas_unicas = set(c["fecha"] for c in clientes_registrados)
        if fechas_unicas:
            promedio_por_dia = ingresos_totales / len(fechas_unicas)
            print(f"\n📈 PROMEDIO DE INGRESOS POR DÍA: ${promedio_por_dia:,.0f}")
        
        # 5. ✅ NUEVA ESTADÍSTICA: Horario más solicitado
        horarios = {}
        for cliente in clientes_registrados:
            hora = cliente["hora"]
            horarios[hora] = horarios.get(hora, 0) + 1
        
        if horarios:
            horario_mas_solicitado = max(horarios, key=horarios.get)
            print(f"\n⏰ HORARIO MÁS SOLICITADO: {horario_mas_solicitado} ({horarios[horario_mas_solicitado]} citas)")
        
        # 6. ✅ NUEVA ESTADÍSTICA: Día con más citas
        citas_por_fecha = {}
        for cliente in clientes_registrados:
            fecha = cliente["fecha"]
            citas_por_fecha[fecha] = citas_por_fecha.get(fecha, 0) + 1
        
        if citas_por_fecha:
            dia_mas_citas = max(citas_por_fecha, key=citas_por_fecha.get)
            print(f"\n📅 DÍA CON MÁS CITAS: {dia_mas_citas} ({citas_por_fecha[dia_mas_citas]} citas)")
        
        # 7. ✅ NUEVA ESTADÍSTICA: Porcentaje de urgencias vs normales
        prioridad_normal = sum(1 for c in clientes_registrados if c["prioridad"] == "Normal")
        prioridad_urgente = sum(1 for c in clientes_registrados if c["prioridad"] == "Urgente")
        
        if total_clientes > 0:
            porcentaje_normal = (prioridad_normal / total_clientes) * 100
            porcentaje_urgente = (prioridad_urgente / total_clientes) * 100
            print(f"\n📊 DISTRIBUCIÓN POR PRIORIDAD:")
            print(f"   • Normal: {prioridad_normal} ({porcentaje_normal:.1f}%)")
            print(f"   • Urgente: {prioridad_urgente} ({porcentaje_urgente:.1f}%)")
        
        # Información adicional
        print("\n" + "-"*60)
        print("📈 DESGLOSE ADICIONAL:")
        print("-"*60)
        
        # Por tipo de cliente
        print("\n📌 Por tipo de cliente:")
        for tipo in ["Particular", "EPS", "Prepagada"]:
            count = sum(1 for c in clientes_registrados if c["tipo"] == tipo)
            if count > 0:
                porcentaje = (count / total_clientes) * 100
                print(f"   • {tipo}: {count} cliente(s) ({porcentaje:.1f}%)")
        
        # Por tipo de atención
        print("\n📌 Por tipo de atención:")
        atenciones = ["Limpieza", "Calzas", "Extracción", "Diagnóstico"]
        for atencion in atenciones:
            count = sum(1 for c in clientes_registrados if c["atencion"] == atencion)
            if count > 0:
                ingresos_atencion = sum(c["total"] for c in clientes_registrados if c["atencion"] == atencion)
                print(f"   • {atencion}: {count} cliente(s) - Ingresos: ${ingresos_atencion:,.0f}")
    
    print("\n" + "="*60)
    input("\nPresione Enter para continuar...")

# ==================== FUNCIONES ADICIONALES ====================

def cancelar_cita_interactivo():
    """Función para cancelar una cita existente"""
    if not clientes_registrados:
        print("\n📋 No hay clientes registrados.")
        input("\nPresione Enter para continuar...")
        return
    
    print("\n" + "="*60)
    print("❌ CANCELAR CITA")
    print("="*60)
    
    cedula = input("Ingrese la cédula del cliente: ")
    cliente = buscar_cliente_por_cedula(cedula)
    
    if not cliente:
        print(f"\n❌ No se encontró ningún cliente con cédula {cedula}")
        input("\nPresione Enter para continuar...")
        return
    
    print(f"\nCliente encontrado: {cliente['nombre']}")
    print(f"Cita agendada para: {cliente['fecha']} a las {cliente['hora']}")
    
    confirmar = input("\n¿Está seguro de cancelar esta cita? (s/n): ").lower()
    
    if confirmar == 's':
        # Cancelar la cita en el diccionario de horarios
        if cancelar_cita(cliente['fecha'], cliente['hora']):
            # Eliminar el cliente de la lista
            clientes_registrados.remove(cliente)
            print("\n✅ Cita cancelada exitosamente")
            print(f"El horario {cliente['fecha']} {cliente['hora']} ahora está disponible")
        else:
            print("\n❌ Error al cancelar la cita")
    else:
        print("\nOperación cancelada")
    
    input("\nPresione Enter para continuar...")

# ==================== MENÚ PRINCIPAL ====================

def menu_principal():
    """Menú interactivo principal"""
    while True:
        print("\n" + "="*60)
        print("🏥 CONSULTORIO ODONTOLÓGICO")
        print("="*60)
        print("1. ☑ Registrar nueva cita")
        print("2. 📋 Ver todos los clientes")
        print("3. 🔍 Buscar cliente por cédula")
        print("4. ⚡ Buscar clientes por prioridad")
        print("5. 📊 Ver estadísticas del consultorio")
        print("6. ❌ Cancelar cita")
        print("7. 🚪 Salir")
        print("="*60)
        
        opcion = input("Seleccione una opción (1-7): ")
        valida, opcion_num = validar_opcion_menu(opcion, 1, 7)
        
        if not valida:
            print("\n❌ Error: Opción inválida. Seleccione 1, 2, 3, 4, 5, 6 o 7.")
            input("\nPresione Enter para continuar...")
            continue
        
        if opcion_num == 1:
            registrar_cita()
        elif opcion_num == 2:
            listar_todos_clientes()
        elif opcion_num == 3:
            buscar_por_cedula_interactivo()
        elif opcion_num == 4:
            buscar_clientes_por_prioridad()
        elif opcion_num == 5:
            mostrar_estadisticas()
        elif opcion_num == 6:
            cancelar_cita_interactivo()
        elif opcion_num == 7:
            print("\n👋 ¡Gracias por usar el sistema!")
            print(f"📊 Total de clientes atendidos: {len(clientes_registrados)}")
            
            # Mostrar resumen de horarios ocupados
            if citas_agendadas:
                print(f"📅 Total de citas agendadas: {len(citas_agendadas)}")
            
            print("¡Hasta luego!")
            break

# ==================== EJECUCIÓN ====================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("BIENVENIDO AL SISTEMA DEL CONSULTORIO ODONTOLÓGICO")
    print("VERSIÓN CORREGIDA - CON ORDENAMIENTO POR FECHA Y HORA")
    print("="*60)
    menu_principal()