from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flask import Flask, render_template, send_from_directory, abort
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import ollama
from plyer import notification
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio


app = Flask(__name__)
app.secret_key = 'admin'

class Database():
    def __init__(self):
        uri = 'mongodb+srv://mario3141230104:SzrLjAIBJKRN5gRF@cluster0.pwumu.mongodb.net/'
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client["myVirtualDatabase"]
        collection = db.test_collection
        print("inicio")

    def checar(checar):
        None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

#inicio cuando ya allas iniciado seción
@app.route('/index_user', methods=['GET', 'POST'])
def index_user():
    usuario=123456
    contrasena=123456
    user={
        "user":usuario,
        "contraseña":contrasena
    }

    return render_template('index_user.html')

@app.route('/finance_manaher', methods=['GET', 'POST'])
def finance_manaher():
    # Conectar a MongoDB
    uri = 'mongodb+srv://admin:admin@cluster0.pwumu.mongodb.net/'
    client = MongoClient(uri)
    db = client["FinBalanceDB"]
    collection = db["FinBalance"]

    # Obtener los IDs únicos de la colección
    ids = collection.distinct('_id')

    # Crear una lista para almacenar los gráficos
    graficos = []

    for id in ids:
        # Filtrar los documentos por ID
        documentos = list(collection.find({'_id': id}))
        
        # Inicializar variables para sumar gastos y obtener el ingreso total
        total_gastos = 0
        ingreso_total = 0

        if documentos:
            # Usar el ingreso mensual del primer documento
            ingreso_total = documentos[0].get('Ingreso_mensual', 0)

            # Sumar los gastos
            for documento in documentos:
                total_gastos += documento.get('Gasto_mensual', 0)

            # Calcular el sobrante
            sobrante = ingreso_total - total_gastos

            # Datos para el gráfico de pastel
            categorias = ['Gastos', 'Ahorrado']
            valores = [total_gastos, sobrante]

            # Crear la gráfica de pastel
            fig = go.Figure(data=[go.Pie(labels=categorias, values=valores)])

            # Obtener el HTML del gráfico
            grafico_html = pio.to_html(fig, full_html=False)
            graficos.append({'id': str(id), 'grafico': grafico_html})

    # Renderizar el template y pasar los gráficos a la plantilla
    return render_template('finbalance1.html', graficos=graficos)



@app.route('/data_center', methods=['GET', 'POST'])
def data_center():
    return render_template('finbalance2.html')

@app.route('/money_register', methods=['GET', 'POST'])
def money_register():
    return render_template('finbalance3.html')

@app.route('/financing_IA', methods=['GET', 'POST'])
def financing_IA():
    uri = 'mongodb+srv://admin:admin@cluster0.pwumu.mongodb.net/'
    client = MongoClient(uri)
    db = client["FinBalanceDB"]
    collection = db["FinBalance"]  # Cambia "tu_coleccion" por el nombre correcto

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

    respuesta = ollama.chat(model='llama3.1:8b', messages=[message])
    
    # Extraer el contenido de la respuesta
    contenido_respuesta = respuesta['message']['content']
    
    # Renderizar el template y pasar la respuesta al template
    return render_template('finbalance4.html', respuesta=contenido_respuesta)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        gasto_mensual = float(request.form['gasto_mensual'])
        ganancia_menusul = float(request.form['ganancia_menusul'])
        uri = 'mongodb+srv://admin:admin@cluster0.pwumu.mongodb.net/'
        client = MongoClient(uri)
        db = client["FinBalanceDB"]
        collection = db["FinBalance"]
        monthly_data = {
            "Ingreso_mensual": ganancia_menusul,
            "Gasto_mensual": gasto_mensual
        }
        collection.insert_one(monthly_data)
        return render_template('menu.html')
    
    return render_template('menu.html')
    


@app.route('/css/<path:filename>')
def custom_static(filename):
    try:
        return send_from_directory('templates/css', filename)
    except Exception as e:
        app.logger.error(f"Error al servir el archivo CSS: {e}")
        abort(404)  # Cambia el error a 404 si el archivo no se encuentra

@app.route('/imagenes/<path:filename>')
def custom_static_imagenes(filename):
    try:
        return send_from_directory('templates/imagenes', filename)
    except Exception as e:
        app.logger.error(f"Error al servir la imagen: {e}")


if __name__ == '__main__':
    app.run(debug=True)