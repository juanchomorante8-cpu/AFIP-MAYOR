import gspread
from google.oauth2.service_account import Credentials

# ========= CONFIG =========
from config import CLIENTES_ID, HOJA_CLIENTES, MAYOR_ID, HOJA_MAYOR, ARCA_ID, HOJA_ARCA



# ========= CONEXIÓN =========
def conectar():
    creds = Credentials.from_service_account_file(RUTA_CREDENCIALES, scopes=SCOPES)
    cliente = gspread.authorize(creds)
    return cliente


# ========= LECTURA ROBUSTA =========
import re
from datetime import datetime

def leer_datos(ws):
    """
    Lee todas las filas de una worksheet, ignorando encabezados y vacías.
    Retorna solo las que tienen datos válidos: CUIT (10 dígitos), Cliente (5 dígitos) y fecha.
    """
    datos = []
    filas = ws.get_all_values()

    for fila in filas:
        # Evitar filas vacías
        if not any(fila):
            continue

        try:
            cuit = fila[0].strip() if len(fila) > 0 else ""
            cliente = fila[1].strip() if len(fila) > 1 else ""
            fecha = fila[2].strip() if len(fila) > 2 else ""

            # Validar CUIT (10 dígitos numéricos)
            if not re.fullmatch(r"\d{10}", cuit):
                continue

            # Validar Cliente (5 dígitos numéricos)
            if not re.fullmatch(r"\d{5}", cliente):
                continue

            # Validar Fecha
            try:
                fecha_valida = datetime.strptime(fecha, "%d/%m/%Y")
            except ValueError:
                continue

            # Si pasa todo, lo guardamos
            datos.append({
                "cuit": cuit,
                "cliente": cliente,
                "fecha": fecha_valida
            })

        except Exception as e:
            # Ignoramos errores y seguimos con la siguiente fila
            continue

    return datos


# ========= MAIN =========
def main():
    cliente = conectar()

    # --- Clientes ---
    hoja_clientes = cliente.open_by_key(LISTADO_CLIENTES_ID).worksheet(HOJA_CLIENTES)
    clientes = leer_datos(hoja_clientes)
    print(f"Clientes cargados: {len(clientes)} filas")

    # --- Mayor ---
    hoja_mayor = cliente.open_by_key(RETENCIONES_MAYOR_ID).worksheet(HOJA_MAYOR)
    mayor = leer_datos(hoja_mayor)
    print(f"Mayor cargado: {len(mayor)} filas")

    # --- Arca ---
    hoja_arca = cliente.open_by_key(RETENCIONES_ARCA_ID).worksheet(HOJA_ARCA)
    arca = leer_datos(hoja_arca)
    print(f"Arca cargado: {len(arca)} filas")

    print("✅ Conexión establecida y datos extraídos correctamente.")


if __name__ == "__main__":
    main()
