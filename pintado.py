from config import MAYOR_ID, MAYOR_HOJA, ARCA_ID, ARCA_HOJA

def pintar_coincidencias(cliente, coincidencias):
    """
    Marca en amarillo las coincidencias tanto en MAYOR como en ARCA.
    """

    # Abrir hojas
    hoja_mayor = cliente.open_by_key(MAYOR_ID).worksheet(MAYOR_HOJA)
    hoja_arca = cliente.open_by_key(ARCA_ID).worksheet(ARCA_HOJA)

    # Traer todos los datos
    datos_mayor = hoja_mayor.get_all_values()
    datos_arca = hoja_arca.get_all_values()

    # Iterar coincidencias
    for c in coincidencias:
        # Buscar en MAYOR (columna I: cliente, columna M: importe)
        for idx, fila in enumerate(datos_mayor, start=1):
            if (c["numero"] in fila[8]  # columna I contiene el número cliente
                and fila[12].replace(".", "").replace(",", ".") == c["importe_mayor"].replace(".", "").replace(",", ".")):
                hoja_mayor.format(f"A{idx}:N{idx}", {"backgroundColor": {"red": 1, "green": 1, "blue": 0}})
        
        # Buscar en ARCA (columna A: cuit, columna J: importe)
        for idx, fila in enumerate(datos_arca, start=1):
            if (c["cuit"] in fila[0]
                and fila[9].replace(".", "").replace(",", ".") == c["importe_arca"].replace(".", "").replace(",", ".")):
                hoja_arca.format(f"A{idx}:K{idx}", {"backgroundColor": {"red": 1, "green": 1, "blue": 0}})

    print("✅ Pintado completado en MAYOR y ARCA")
