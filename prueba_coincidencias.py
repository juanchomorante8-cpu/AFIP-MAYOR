from config import LISTADO_CLIENTES_ID, HOJA_CLIENTES, RETENCIONES_PHYSIS_ID, HOJA_PHYSIS
from main import leer_archivo

def buscar_coincidencias():
    clientes = leer_archivo(LISTADO_CLIENTES_ID, HOJA_CLIENTES)
    physis = leer_archivo(RETENCIONES_PHYSIS_ID, HOJA_PHYSIS)

    clientes_set = set([fila[0] for fila in clientes[1:]])  # ignora cabecera
    physis_set = set([fila[0] for fila in physis[1:]])

    coincidencias = clientes_set.intersection(physis_set)
    return coincidencias

if __name__ == "__main__":
    coincidencias = buscar_coincidencias()
    print("🔎 Coincidencias encontradas:")
    for c in coincidencias:
        print(f"  - {c}")
