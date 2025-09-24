from config import (
    conectar,
    LISTADO_CLIENTES_ID, HOJA_CLIENTES,
    RETENCIONES_MAYOR_ID, HOJA_MAYOR,
    RETENCIONES_ARCA_ID, HOJA_ARCA
)

def buscar_coincidencias():
    cliente = conectar()

    clientes = cliente.open_by_key(LISTADO_CLIENTES_ID).worksheet(HOJA_CLIENTES).get_all_records()
    mayor = cliente.open_by_key(RETENCIONES_MAYOR_ID).worksheet(HOJA_MAYOR).get_all_records()
    arca = cliente.open_by_key(RETENCIONES_ARCA_ID).worksheet(HOJA_ARCA).get_all_records()

    # 🔹 Ejemplo: comparar por campo "CUIT"
    coincidencias = []
    for cli in clientes:
        for mov in mayor:
            if cli["CUIT"] == mov["CUIT"]:
                coincidencias.append(cli)

    print("Coincidencias encontradas:", len(coincidencias))

if __name__ == "__main__":
    buscar_coincidencias()
