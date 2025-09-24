import gspread
from google.oauth2.service_account import Credentials

# Ruta a las credenciales
RUTA_CREDENCIALES = "credenciales.json"

# Alcances para Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# IDs de Dlas hojas de cálculo (ajusta según tu setup real)
CLIENTES_ID = "1JP-tMfcKmN7zxIB8ukXsr3OUu3bGwZwfqE86QI_dhME" 
HOJA_CLIENTES = "Cuentas Auxiliares con Datos d"

MAYOR_ID = "1jHHubxFvCGZcQPrUciSq7uIVI-WYoJtzSEcQ2lfaGNI" 
HOJA_MAYOR = "Del_01_05_2024_Al_30_04_2025" 

ARCA_ID ="1POWukhgzQQCCvPNNXSXZ9F7nsSOL9WdKmwa8SjpATQk" 
HOJA_ARCA = "Retenciones Impositivas"



def conectar():
    creds = Credentials.from_service_account_file(RUTA_CREDENCIALES, scopes=SCOPES)
    cliente = gspread.authorize(creds)
    return cliente
