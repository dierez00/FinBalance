import ollama
from pymongo import MongoClient

# Conectar a MongoDB
uri = 'mongodb+srv://admin:admin@cluster0.pwumu.mongodb.net/'
client = MongoClient(uri)
db = client["FinBalanceDB"]
collection = db["tu_coleccion"]  # Cambia "tu_coleccion" por el nombre correcto

# Obtener el último registro
ultimo_documento = collection.find_one(sort=[('_id', -1)])  # Consulta el último registro según el ID

# Extraer los valores de ingreso mensual y gasto
ingreso_mensual = ultimo_documento.get('ingreso_mensual', 0)
gasto_mensual = ultimo_documento.get('gasto', 0)

# Preparar el mensaje con los valores obtenidos
message = {
    'role': 'user',
    'content': f'Imagine you are a successful and renowned financial advisor. You have the following data: monthly income: {ingreso_mensual}, monthly expense: {gasto_mensual}. Your task is to analyze and give an opinion on how they can improve their finances (in 100 words or less, answer in english).'
}

# Llamada al modelo
response = ollama.chat(model='llama3.1:8b', messages=[message])

# Mostrar la respuesta
print(response['message']['content'])