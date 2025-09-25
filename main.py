from config import conectar, CLIENTES_ID, CLIENTES_HOJA, MAYOR_ID, MAYOR_HOJA, ARCA_ID, ARCA_HOJA
from lector import leer_clientes, leer_mayor, leer_arca
from pintar import pintar_coincidencias

def main():
    cliente = conectar()

    # Lectura de datos
    clientes = leer_clientes(cliente)
    mayor = leer_mayor(cliente)
    arca = leer_arca(cliente)

    print("=== CLIENTES ===", clientes[:5])
    print("=== MAYOR ===", mayor[:5])
    print("=== ARCA ===", arca[:5])

    # Vincular clientes con mayor (para obtener CUIT + movimientos)
    clientes_dict = {c["numero"]: c["cuit"] for c in clientes}
    clientes_mayor = []
    for m in mayor:
        if m["numero"] in clientes_dict:
            clientes_mayor.append({
                "numero": m["numero"],
                "cuit": clientes_dict[m["numero"]],
                "fecha": m["fecha"],
                "importe": m["importe"]
            })

    print("\n=== CLIENTES + MAYOR ===")
    for cm in clientes_mayor[:5]:
        print(cm)

    # Coincidencias con ARCA
    filas_mayor = []
    filas_arca = []

    for idx_cm, cm in enumerate(clientes_mayor, start=2):  # +2 por encabezado
        for idx_a, a in enumerate(arca, start=2):
            mismo_cuit = cm["cuit"] == a["cuit"]

            # Comparar mes/año de la fecha
            mes_cm, anio_cm = cm["fecha"][3:10], cm["fecha"][-4:]
            mes_a, anio_a = a["fecha"][3:10], a["fecha"][-4:]
            misma_fecha = (mes_cm == mes_a) and (anio_cm == anio_a)

            # Diferencia de importe tolerada
            misma_plata = abs(cm["importe"] - a["importe"]) <= 1.0

            if mismo_cuit and misma_fecha and misma_plata:
                print(f"✅ Coincidencia: {cm} <-> {a}")
                filas_mayor.append(idx_cm)
                filas_arca.append(idx_a)

    # Pintar coincidencias en ambas hojas
    pintar_coincidencias(cliente, MAYOR_ID, MAYOR_HOJA, filas_mayor)
    pintar_coincidencias(cliente, ARCA_ID, ARCA_HOJA, filas_arca)


if __name__ == "__main__":
    main()
