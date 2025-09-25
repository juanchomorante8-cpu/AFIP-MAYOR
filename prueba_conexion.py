from config import conectar, CLIENTES_ID, CLIENTES_HOJA, MAYOR_ID, MAYOR_HOJA, ARCA_ID, ARCA_HOJA

# Conexión
cliente = conectar()
print("✅ Conectado a Google Sheets")

# Probar CLIENTES
clientes = cliente.open_by_key(CLIENTES_ID).worksheet(CLIENTES_HOJA)
print("Primera fila CLIENTES:", clientes.row_values(1))

# Probar MAYOR
mayor = cliente.open_by_key(MAYOR_ID).worksheet(MAYOR_HOJA)
print("Primera fila MAYOR:", mayor.row_values(1))

# Probar ARCA
arca = cliente.open_by_key(ARCA_ID).worksheet(ARCA_HOJA)
print("Primera fila ARCA:", arca.row_values(1))
