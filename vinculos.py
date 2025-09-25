from datetime import datetime

def unir_clientes_mayor(clientes, mayor):
    """
    Une clientes y mayor por número de cliente.
    Devuelve lista con dicts: {numero, cuit, fecha, importe}
    """
    mapa_clientes = {c["numero"]: c["cuit"] for c in clientes}
    vinculos = []

    for m in mayor:
        numero = m["numero"]
        if numero in mapa_clientes:
            vinculos.append({
                "numero": numero,
                "cuit": mapa_clientes[numero],
                "fecha": m["fecha"],
                "importe": m["importe"]
            })

    return vinculos


def misma_fecha(fecha1, fecha2):
    """
    Devuelve True si fecha1 y fecha2 tienen mismo mes y año (día ignorado).
    """
    try:
        f1 = datetime.strptime(fecha1, "%d/%m/%Y")
        f2 = datetime.strptime(fecha2, "%d/%m/%Y")
        return f1.month == f2.month and f1.year == f2.year
    except ValueError:
        return False


def comparar_con_arca(vinculos, arca):
    """
    Compara vinculos (clientes+mayor) contra arca por CUIT, fecha y monto ±1.
    Devuelve lista de coincidencias.
    """
    coincidencias = []
    for v in vinculos:
        for a in arca:
            try:
                importe_v = float(str(v["importe"]).replace(".", "").replace(",", "."))
                importe_a = float(str(a["importe"]).replace(".", "").replace(",", "."))
            except ValueError:
                continue

            if (
                v["cuit"] == a["cuit"]
                and misma_fecha(v["fecha"], a["fecha"])
                and abs(importe_v - importe_a) <= 1
            ):
                coincidencias.append({
                    "numero": v["numero"],
                    "cuit": v["cuit"],
                    "fecha": v["fecha"],
                    "importe_v": importe_v,
                    "importe_a": importe_a
                })
                break
    return coincidencias
