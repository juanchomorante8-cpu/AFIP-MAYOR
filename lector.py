import re
from config import (
    conectar,
    CLIENTES_ID, CLIENTES_HOJA,
    MAYOR_ID, MAYOR_HOJA,
    ARCA_ID, ARCA_HOJA
)

# ==============================
# FUNCIONES AUXILIARES
# ==============================
def limpiar_importe(importe_str):
    """
    Convierte un importe en formato latino (1.234.567,89)
    a float en formato Python (1234567.89).
    """
    try:
        limpio = importe_str.strip().replace(".", "").replace(",", ".")
        return float(limpio)
    except:
        return None

# ==============================
# LECTORES
# ==============================
def leer_clientes(cliente):
    hoja = cliente.open_by_key(CLIENTES_ID).worksheet(CLIENTES_HOJA)
    datos = hoja.get_all_values()

    clientes = []
    for i, fila in enumerate(datos[1:], start=2):  # arranca en fila 2
        try:
            numero = fila[1][-5:].zfill(5)  # últimos 5 dígitos de columna B
            cuit = re.search(r"\d{11}", fila[3])  # columna D
            if cuit:
                clientes.append({
                    "numero": numero,
                    "cuit": cuit.group(),
                    "fila": i
                })
        except IndexError:
            continue

    return clientes


def leer_mayor(cliente):
    hoja = cliente.open_by_key(MAYOR_ID).worksheet(MAYOR_HOJA)
    datos = hoja.get_all_values()

    mayor = []
    for i, fila in enumerate(datos[1:], start=2):  # arranca en fila 2
        try:
            texto = fila[8]  # Columna I
            match_cliente = re.search(r"\((\d{5})\)", texto)   # nro cliente
            match_fecha = re.search(r"(\d{2}/\d{2}/\d{4})$", texto)  # fecha

            if match_cliente and match_fecha:
                importe = limpiar_importe(fila[12])  # Columna M
                if importe is not None:
                    mayor.append({
                        "numero": match_cliente.group(1),
                        "fecha": match_fecha.group(1),
                        "importe": importe,
                        "fila": i
                    })
        except IndexError:
            continue

    return mayor


def leer_arca(cliente):
    hoja = cliente.open_by_key(ARCA_ID).worksheet(ARCA_HOJA)
    datos = hoja.get_all_values()

    arca = []
    for i, fila in enumerate(datos[1:], start=2):  # arranca en fila 2
        try:
            cuit = re.search(r"\d{11}", fila[0])  # Columna A
            fecha = fila[6]  # Columna G
            importe = limpiar_importe(fila[9])  # Columna J

            if cuit and fecha and importe is not None:
                arca.append({
                    "cuit": cuit.group(),
                    "fecha": fecha,
                    "importe": importe,
                    "fila": i
                })
        except IndexError:
            continue

    return arca
