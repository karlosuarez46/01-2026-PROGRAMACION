
"""
# problemas que presenta la version 1

-Solo registra un cliente - No permite múltiples clientes en arreglo
-No tiene validación de datos - Entrada sin control 
-Validación de cantidad > 0
Menú para agregar más clientes	
-No calcula Total Clientes 
-No calcula Ingresos totales
-No calcula clientes para extracción 
-No ordena clientes - Requisito obligatorio
-No busca por cédula - Requisito obligatorio
-No almacena en arreglo - Usa variable simple
-No tiene validación de datos - Entrada sin control
-No permite capturar varios clientes - Solo uno
"""


# Versión 1 
# Programa para consultorio odontológico

# Tablas de precios
precios_cita = { "Particular": 80000,"EPS": 5000,"Prepagada": 30000 }

precios_atencion = {
    "Particular": {"Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
    "EPS": {"Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0},
    "Prepagada": {"Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0}
}



# Capturar datos de un cliente
print("=== CONSULTORIO ODONTOLÓGICO ===")
cedula = input("Cédula: ")
nombre = input("Nombre: ")
telefono = input("Teléfono: ")

print("Tipo Cliente: 1=Particular, 2=EPS, 3=Prepagada")
tipo_opcion = int(input("Opción: "))
if tipo_opcion == 1:
    tipo = "Particular"
elif tipo_opcion == 2:
    tipo = "EPS"
else:
    tipo = "Prepagada"

print("Tipo Atención: 1=Limpieza, 2=Calzas, 3=Extracción, 4=Diagnóstico")
atencion_opcion = int(input("Opción: "))
if atencion_opcion == 1:
    atencion = "Limpieza"
elif atencion_opcion == 2:
    atencion = "Calzas"
elif atencion_opcion == 3:
    atencion = "Extracción"
else:
    atencion = "Diagnóstico"

# Cantidad
if atencion in ["Limpieza", "Diagnóstico"]:
    cantidad = 1
else:
    cantidad = int(input("Cantidad: "))

print("Prioridad: 1=Normal, 2=Urgente")
prioridad_opcion = int(input("Opción: "))
prioridad = "Normal" if prioridad_opcion == 1 else "Urgente"

fecha = input("Fecha de la Cita (DD/MM/AAAA): ")

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
    "total": total_pagar
}
clientes.append(cliente)

# Mostrar resultado
print("\n=== RESUMEN DE CITA ===")
print(f"Cliente: {nombre}")
print(f"Tipo: {tipo}")
print(f"Atención: {atencion}")
print(f"Cantidad: {cantidad}")
print(f"Valor a pagar: ${total_pagar:,.0f}")