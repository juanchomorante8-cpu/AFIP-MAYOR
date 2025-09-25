import gspread
from google.oauth2.service_account import Credentials

# ==============================
# CONFIGURACIÓN DE CREDENCIALES
# ==============================
RUTA_CREDENCIALES = "credenciales.json"  # Asegúrate de que está en la raíz
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def conectar():
    creds = Credentials.from_service_account_file(RUTA_CREDENCIALES, scopes=SCOPES)
    cliente = gspread.authorize(creds)
    return cliente

# ==============================
# CONFIGURACIÓN DE HOJAS
# ==============================

# CLIENTES
CLIENTES_ID = "1JP-tMfcKmN7zxIB8ukXsr3OUu3bGwZwfqE86QI_dhME"
CLIENTES_HOJA = "Cuentas Auxiliares con Datos d"

# MAYOR
MAYOR_ID = "1jHHubxFvCGZcQPrUciSq7uIVI-WYoJtzSEcQ2lfaGNI"
MAYOR_HOJA = "Del_01_05_2024_Al_30_04_2025"

# ARCA
ARCA_ID = "1POWukhgzQQCCvPNNXSXZ9F7nsSOL9WdKmwa8SjpATQk"
ARCA_HOJA = "Retenciones Impositivas"
