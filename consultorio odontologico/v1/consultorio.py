
"""
# problemas que presenta la version 1

-menú interactivo
-No tiene validación de datos: entrada sin control. 
-ajustar un horario de cita (no se puede repetir hora a otro cliente); deben salir las opciones de los horarios disponibles.
Cédula (no pueden ser letras); solo debe contener números. 
-nombres (no puede ser número) 
Números telefónicos (no pueden ser letras); solo deben contener números, máximo 10 dígitos, mínimo 7 dígitos.
-tipo de cliente (solo debe ser las 3 opciones); debe arrojar error en caso de escribir otra opción diferente. 
- Tipo de atención: (solo debe ser las 4 opciones); debe arrojar error en caso de escribir otra opción diferente. 
-Prioridad: (solo debe ser las 2 opciones); debe arrojar error en caso de escribir otra opción diferente. 
-Fecha de la cita: (no puede ser días, meses, años anteriores al presente)

"""

## Programa para consultorio odontológico version 1

# Tablas de precios

precios_cita = { "Particular": 80000,"EPS": 5000,"Prepagada": 30000 }

precios_atencion = {
"Particular": {"Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
"EPS": {"Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0},
"Prepagada": {"Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0}}

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

# Mostrar resultado
print("\n=== RESUMEN DE CITA ===")
print(f"Cliente: {nombre}")
print(f"Tipo: {tipo}")
print(f"Atención: {atencion}")
print(f"Cantidad: {cantidad}")
print(f"Valor a pagar: ${total_pagar:,.0f}")