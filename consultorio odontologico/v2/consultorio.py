

"""
# problemas que presenta la version 2
 
-No calcula Totalidad de Clientes 
-No calcula Ingresos totales
-No calcula clientes por procedimientos 
-No busca por cédula 


"""
## Programa para consultorio odontológico version 2

from datetime import datetime, timedelta
import re

# Tablas de precios
precios_cita = { "Particular": 80000, "EPS": 5000, "Prepagada": 30000 }

precios_atencion = { 
"Particular": {"Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
"EPS": {"Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0},
"Prepagada": {"Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0}}

# Horarios disponibles (cada hora en punto)
horarios_disponibles = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]

# Base de datos de citas (simulada en memoria)
citas_agendadas = {}  # Formato: {"DD/MM/AAAA HH:MM": cedula}

def validar_cedula(cedula):
    """Valida que la cédula contenga solo números"""
    return cedula.isdigit()

def validar_nombre(nombre):
    """Valida que el nombre no contenga números"""
    return not any(char.isdigit() for char in nombre) and nombre.strip() != ""

def validar_telefono(telefono):
    """Valida teléfono: solo números, mínimo 7, máximo 10 dígitos"""
    return telefono.isdigit() and 7 <= len(telefono) <= 10

def validar_fecha(fecha_str):
    """Valida que la fecha no sea anterior al día actual"""
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        fecha_actual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return fecha >= fecha_actual
    except ValueError:
        return False

def obtener_horarios_disponibles(fecha):
    """Retorna lista de horarios disponibles para una fecha específica"""
    disponibles = []
    for hora in horarios_disponibles:
        clave = f"{fecha} {hora}"
        if clave not in citas_agendadas:
            disponibles.append(hora)
    return disponibles

def agendar_cita(fecha, hora, cedula):
    """Agenda una cita en la fecha y hora especificada"""
    clave = f"{fecha} {hora}"
    citas_agendadas[clave] = cedula

def validar_opcion_menu(opcion, min_op, max_op):
    """Valida que la opción esté dentro del rango permitido"""
    try:
        opcion_int = int(opcion)
        return min_op <= opcion_int <= max_op, opcion_int
    except ValueError:
        return False, None

def registrar_cita():
    """Función principal para registrar una nueva cita"""
    print("\n" + "="*50)
    print("REGISTRO DE NUEVA CITA")
    print("="*50)
    
    # Validar cédula
    while True:
        cedula = input("Cédula: ")
        if validar_cedula(cedula):
            break
        print("❌ Error: La cédula solo debe contener números. Intente nuevamente.")
    
    # Validar nombre
    while True:
        nombre = input("Nombre: ")
        if validar_nombre(nombre):
            break
        print("❌ Error: El nombre no debe contener números. Intente nuevamente.")
    
    # Validar teléfono
    while True:
        telefono = input("Teléfono: ")
        if validar_telefono(telefono):
            break
        print("❌ Error: El teléfono debe tener entre 7 y 10 dígitos numéricos. Intente nuevamente.")
    
    # Validar tipo de cliente
    while True:
        print("\nTipo Cliente:")
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
        print("❌ Error: Opción inválida. Seleccione 1, 2 o 3.")
    
    # Validar tipo de atención
    while True:
        print("\nTipo de Atención:")
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
        print("❌ Error: Opción inválida. Seleccione 1, 2, 3 o 4.")
    
    # Cantidad (solo para ciertos tratamientos)
    if atencion in ["Limpieza", "Diagnóstico"]:
        cantidad = 1
        print(f"Cantidad: {cantidad} (valor fijo para {atencion})")
    else:
        while True:
            try:
                cantidad = int(input("Cantidad: "))
                if cantidad > 0:
                    break
                print("❌ Error: La cantidad debe ser mayor a 0.")
            except ValueError:
                print("❌ Error: Ingrese un número válido.")
    
    # Validar prioridad
    while True:
        print("\nPrioridad:")
        print("1. Normal")
        print("2. Urgente")
        opcion = input("Opción: ")
        valida, prioridad_opcion = validar_opcion_menu(opcion, 1, 2)
        if valida:
            prioridad = "Normal" if prioridad_opcion == 1 else "Urgente"
            break
        print("❌ Error: Opción inválida. Seleccione 1 o 2.")
    
    # Validar fecha
    while True:
        fecha = input("Fecha de la Cita (DD/MM/AAAA): ")
        if validar_fecha(fecha):
            break
        print("❌ Error: Fecha inválida o anterior al día actual. Intente nuevamente.")
    
    # Validar horario disponible
    while True:
        horarios_disp = obtener_horarios_disponibles(fecha)
        if not horarios_disp:
            print(f"❌ No hay horarios disponibles para la fecha {fecha}.")
            print("Por favor, seleccione otra fecha.")
            while True:
                fecha = input("Nueva fecha (DD/MM/AAAA): ")
                if validar_fecha(fecha):
                    break
                print("❌ Error: Fecha inválida o anterior al día actual.")
            continue
        
        print(f"\nHorarios disponibles para {fecha}:")
        for i, hora in enumerate(horarios_disp, 1):
            print(f"{i}. {hora}")
        
        try:
            opcion_horario = int(input("Seleccione el horario (número): "))
            if 1 <= opcion_horario <= len(horarios_disp):
                hora_seleccionada = horarios_disp[opcion_horario - 1]
                break
            print(f"❌ Error: Seleccione un número entre 1 y {len(horarios_disp)}.")
        except ValueError:
            print("❌ Error: Ingrese un número válido.")
    
    # Calcular valor
    valor_cita = precios_cita[tipo]
    valor_atencion = precios_atencion[tipo][atencion]
    total_pagar = valor_cita + (valor_atencion * cantidad)
    
    # Guardar cita
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
    
    # Agendar en el sistema
    agendar_cita(fecha, hora_seleccionada, cedula)
    
    # Mostrar resultado
    print("\n" + "="*50)
    print("✅ CITA REGISTRADA EXITOSAMENTE")
    print("="*50)
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
    print("="*50)
    
    return cliente

def consultar_citas():
    """Muestra todas las citas agendadas"""
    if not citas_agendadas:
        print("\n📅 No hay citas agendadas actualmente.")
        return
    
    print("\n" + "="*50)
    print("CITAS AGENDADAS")
    print("="*50)
    for fecha_hora, cedula in sorted(citas_agendadas.items()):
        print(f"📌 {fecha_hora} - Cédula: {cedula}")
    print("="*50)

def menu_principal():
    """Menú interactivo principal"""
    while True:
        print("\n" + "="*50)
        print("CONSULTORIO ODONTOLÓGICO")
        print("="*50)
        print("1. Registrar nueva cita")
        print("2. Ver citas agendadas")
        print("3. Salir")
        print("="*50)
        
        opcion = input("Seleccione una opción: ")
        valida, opcion_num = validar_opcion_menu(opcion, 1, 3)
        
        if not valida:
            print("❌ Error: Opción inválida. Seleccione 1, 2 o 3.")
            continue
        
        if opcion_num == 1:
            registrar_cita()
        elif opcion_num == 2:
            consultar_citas()
        elif opcion_num == 3:
            print("\n👋 ¡Gracias por usar el sistema! Hasta luego.")
            break

# Ejecutar el programa
if __name__ == "__main__":
    menu_principal()