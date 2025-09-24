import gspread
from google.oauth2 import service_account
from config import SCOPES, CREDENTIALS_FILE, LISTADO_CLIENTES_ID, HOJA_CLIENTES, RETENCIONES_PHYSIS_ID, HOJA_PHYSIS, RETENCIONES_ARCA_ID, HOJA_ARCA

def conectar():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client

def leer_archivo(sheet_id, hoja):
    client = conectar()
    ws = client.open_by_key(sheet_id).worksheet(hoja)
    datos = ws.get_all_values()
    return datos

if __name__ == "__main__":
    print("Extrayendo datos...")

    clientes = leer_archivo(LISTADO_CLIENTES_ID, HOJA_CLIENTES)
    print(f"🟩 Clientes: {len(clientes)} filas")

    physis = leer_archivo(RETENCIONES_PHYSIS_ID, HOJA_PHYSIS)
    print(f"🟨 Retenciones Physis: {len(physis)} filas")

    arca = leer_archivo(RETENCIONES_ARCA_ID, HOJA_ARCA)
    print(f"🟧 Retenciones Arca: {len(arca)} filas")

    print("✅ Conexión establecida y datos extraídos.")
