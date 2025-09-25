import time
from config import conectar, CLIENTES_ID, CLIENTES_HOJA, MAYOR_ID, MAYOR_HOJA, ARCA_ID, ARCA_HOJA
from lector import leer_clientes, leer_mayor, leer_arca
import gspread
from gspread_formatting import CellFormat, Color, format_cell_range

# =========================
# Normalizador de importes
# =========================
def normalizar_importe(importe):
    if not importe:
        return 0.0
    try:
        limpio = importe.strip().replace(".", "").replace(",", ".")
        return float(limpio)
    except (ValueError, AttributeError):
        return 0.0

# =========================
# Función para pintar coincidencias
# =========================
def pintar_fila(hoja, fila_idx, color=Color(1, 1, 0)):
    """Pinta toda la fila hasta la última columna usada."""
    try:
        num_cols = len(hoja.row_values(1))  # número de columnas según encabezado
        rango = f"A{fila_idx}:{chr(64+num_cols)}{fila_idx}"
        formato = CellFormat(backgroundColor=color)
        format_cell_range(hoja, rango, formato)
    except Exception as e:
        print(f"⚠️ Error pintando fila {fila_idx}: {e}")

# =========================
# Función principal
# =========================
def main():
    inicio_total = time.perf_counter()
    cliente = conectar()

    # ---- Leer CLIENTES ----
    print("📂 Leyendo CLIENTES...")
    t0 = time.perf_counter()
    clientes = leer_clientes(cliente)
    print(f"   → {len(clientes)} registros obtenidos en {time.perf_counter()-t0:.2f} seg")

    # ---- Leer MAYOR ----
    print("📂 Leyendo MAYOR...")
    t0 = time.perf_counter()
    mayor = leer_mayor(cliente)
    print(f"   → {len(mayor)} registros obtenidos en {time.perf_counter()-t0:.2f} seg")

    # ---- Leer ARCA ----
    print("📂 Leyendo ARCA...")
    t0 = time.perf_counter()
    arca = leer_arca(cliente)
    print(f"   → {len(arca)} registros obtenidos en {time.perf_counter()-t0:.2f} seg")

    # ---- Vincular CLIENTES + MAYOR ----
    print("\n🔎 Buscando coincidencias CLIENTES + MAYOR...")
    clientes_mayor = []
    for c in clientes:
        for m in mayor:
            if c["numero"] == m["numero"]:
                clientes_mayor.append({
                    "numero": c["numero"],
                    "cuit": c["cuit"],
                    "fecha": m["fecha"],
                    "importe": m["importe"]
                })
    print(f"   → {len(clientes_mayor)} coincidencias CLIENTES+MAYOR")

    # ---- Comparar con ARCA ----
    print("\n🔎 Buscando coincidencias finales con ARCA...")
    coincidencias_finales = []
    for cm in clientes_mayor:
        for a in arca:
            if cm["cuit"] == a["cuit"]:
                # Comparar mes/año de la fecha
                mes_cm, anio_cm = cm["fecha"].split("/")[1], cm["fecha"].split("/")[2]
                mes_a, anio_a = a["fecha"].split("/")[1], a["fecha"].split("/")[2]

                if mes_cm == mes_a and anio_cm == anio_a:
                    imp_cm = normalizar_importe(cm.get("importe"))
                    imp_a = normalizar_importe(a.get("importe"))

                    if abs(imp_cm - imp_a) <= 1:
                        coincidencias_finales.append((cm, a))

    print(f"✅ Coincidencias finales encontradas: {len(coincidencias_finales)}")

    # ---- Pintar coincidencias ----
    print("\n🎨 Pintando coincidencias en las hojas...")
    hoja_mayor = cliente.open_by_key(MAYOR_ID).worksheet(MAYOR_HOJA)
    hoja_arca = cliente.open_by_key(ARCA_ID).worksheet(ARCA_HOJA)

    for idx, (cm, a) in enumerate(coincidencias_finales, start=1):
        try:
            # Pintar en MAYOR
            for i, fila in enumerate(hoja_mayor.get_all_values(), start=1):
                if cm["fecha"] in fila and str(cm["numero"]) in fila:
                    pintar_fila(hoja_mayor, i)

            # Pintar en ARCA
            for j, fila in enumerate(hoja_arca.get_all_values(), start=1):
                if a["cuit"] in fila and a["fecha"] in fila:
                    pintar_fila(hoja_arca, j)

            if idx % 10 == 0:  # cada 10 coincidencias
                print(f"   → {idx} coincidencias pintadas...")
                time.sleep(1)  # para no saturar la API
        except Exception as e:
            print(f"⚠️ Error pintando coincidencia {idx}: {e}")

    print("\n📌 Proceso completado en "
          f"{(time.perf_counter()-inicio_total)/60:.2f} minutos.")

if __name__ == "__main__":
    main()
