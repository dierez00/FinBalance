from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

uri = 'mongodb+srv://admin:admin@cluster0.pwumu.mongodb.net/'

try:
    client = MongoClient(uri)

    db = client["FinBalanceDB"]

    collection = db["FinBalance"]

    monthly_expense = float(input("Ingrese el total de sus gastos mensuales: "))

    current_month = 1

    monthly_data = {
    "ingreso": monthly_expense,
    "month": current_month
    }

    result = collection.insert_one(monthly_data)

    print("Gasto mensual registrado con éxito. ID del documento insertado:", result.inserted_id)
    
except ServerSelectionTimeoutError as e:
    print("No se pudo conectar a MongoDB. Error:", e)
except Exception as e:
    print("Error inesperado:", e)

