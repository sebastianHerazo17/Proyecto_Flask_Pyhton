from flask import Flask, render_template, request, redirect, session, after_this_request, jsonify
import mysql.connector
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
import csv
import os
from werkzeug.utils import secure_filename
from flask_login import LoginManager, current_user
from functools import wraps
from flask import url_for
import secrets
import time

app = Flask(__name__)

# Generar una clave secreta aleatoria
secret_key = secrets.token_hex(16)

# Configurar la clave secreta en la aplicación Flask
app.secret_key = secret_key

config = {
            'user': 'root',
            'password': '**',
            'host': 'localhost',
            'database': '**',
            }

def validate_user(username, password):
    try:
        # Establece una conexión a la base de datos
        conn = mysql.connector.connect(**config)

        # Crea un cursor para ejecutar consultas
        cursor = conn.cursor()

        # Ejecuta la consulta para verificar las credenciales del usuario
        query = "SELECT * FROM customuser WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        # Obtiene el resultado de la consulta
        result = cursor.fetchone()

        # Cierra el cursor y la conexión a la base de datos
        cursor.close()
        conn.close()

        # Si se encontró un resultado, las credenciales son válidas
        return result is not None

    except mysql.connector.Error as error:
        # Maneja cualquier error de la base de datos
        print('Error al validar el usuario:', error)
        return False


@app.route('/')
def home():
    session.pop('authenticated', None)
    return render_template('index.html')


def get_user_role(username):
    try:
        # Establece una conexión a la base de datos
        conn = mysql.connector.connect(**config)

        # Crea un cursor para ejecutar consultas
        cursor = conn.cursor()

        # Ejecuta la consulta para obtener el rol del usuario
        query = """
        SELECT r.nombre
        FROM rol r
        INNER JOIN customuser_roles cu_r ON r.id = cu_r.rol_id
        INNER JOIN customuser cu ON cu.id = cu_r.customuser_id
        WHERE cu.username = %s
        """
        cursor.execute(query, (username,))

        # Obtiene el resultado de la consulta
        result = cursor.fetchone()

        # Cierra el cursor y la conexión a la base de datos
        cursor.close()
        conn.close()

        # Si se encontró un resultado, retorna el rol del usuario
        if result:
            return result[0]

    except mysql.connector.Error as error:
        # Maneja cualquier error de la base de datos
        print('Error al obtener el rol del usuario:', error)

    return None




@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('authenticated', None)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if validate_user(username, password):
            session['authenticated'] = True
            session['username'] = username
            session['role'] = get_user_role(username)  # Obtener el rol del usuario

            return redirect(url_for('dashboard'))  # Redirigir al dashboard
        else:
            error = 'Credenciales inválidas. Por favor, intenta nuevamente.'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if 'authenticated' in session:
            # El usuario está autenticado, se permite acceder a la vista
            return view_func(*args, **kwargs)
        else:
            # Redirigir al formulario de inicio de sesión si no está autenticado
            return redirect(url_for('login'))
    return wrapper


@app.route('/dashboard')
@login_required
def dashboard():
    # Verificar si el usuario está autenticado y tiene un rol válido
    if 'authenticated' in session and session['authenticated'] and 'username' in session and 'role' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado o no tiene un rol válido





@app.route('/formulario', methods=['GET', 'POST'])
def calculadora():
    """Esta función muestra un formulario y realiza la predicción en base a los datos ingresados."""
    # Verificar si se enviaron datos a través del formulario
    if request.method == 'POST':
        # Obtener los datos ingresados por el usuario
        angular = int(request.form.get('angular'))
        aws = int(request.form.get('aws'))
        basesDeDatos=int(request.form.get('basesDeDatos'))
        csharp = int(request.form.get('csharp'))
        cplusplus = int(request.form.get('cplusplus'))
        capacidadDeAnalisis = int(request.form.get('capacidadDeAnalisis'))
        cienciaDeDatos = int(request.form.get('cienciaDeDatos'))
        colaboracion = int(request.form.get('colaboracion'))
        comunicacion = int(request.form.get('comunicacion'))
        desarrolloFrontEnd = int(request.form.get('desarrolloFrontEnd'))
        desarrolloWebBackEnd = int(request.form.get('desarrolloWebBackEnd'))
        css = int(request.form.get('css'))
        html5 = int(request.form.get('html5'))
        inglesB1 = int(request.form.get('inglesB1'))
        java = int(request.form.get('java'))
        javascript = int(request.form.get('javascript'))
        json = int(request.form.get('json'))
        liderazgo = int(request.form.get('liderazgo'))
        metodologiasAgiles = int(request.form.get('metodologiasAgiles'))
        nodejs = int(request.form.get('nodejs'))
        php = int(request.form.get('php'))
        proactividad = int(request.form.get('proactividad'))
        python = int(request.form.get('python'))
        reactjs = int(request.form.get('reactjs'))
        trabajoEnEquipo = int(request.form.get('trabajoEnEquipo'))

        # Conectarse a la base de datos
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Obtener los datos de la base de datos
        cursor.execute("SELECT `Angular`, `AWS`, `Bases de datos`, `C#`, `C++`, `Capacidad de análisis`, `Ciencia de datos`, `Colaboración`, `Comunicación`, `Desarrollo front end`, `Desarrollo web back end`, `Hojas de estilos en cascada (CSS)`, `HTML5`, `Inglés B1 o más`, `Java`, `JavaScript`, `Json`, `Liderazgo`, `Metodologías Agiles`, `Node.js`, `PHP`, `Proactividad`, `Python`, `React.js`, `Trabajo en equipo`, `empleo` FROM datos")
        data = cursor.fetchall()
        X = np.array([row[:-1] for row in data])
        y = np.array([row[-1] for row in data])

        # Crear el modelo y entrenarlo
        modelo = LogisticRegression()
        modelo.fit(X, y)

        # Realizar la predicción con los datos ingresados
        X_nuevo = np.array([[angular, aws, basesDeDatos, csharp, cplusplus, capacidadDeAnalisis, cienciaDeDatos, colaboracion, comunicacion, desarrolloFrontEnd, desarrolloWebBackEnd, css, html5, inglesB1, java, javascript, json, liderazgo, metodologiasAgiles, nodejs, php, proactividad, python, reactjs, trabajoEnEquipo]])
        prediccion = modelo.predict_proba(X_nuevo)[0][1]  # Obtener la probabilidad de la clase 1

        # Determinar el mensaje según la salida del modelo
        if prediccion  < 0.3:
            mensaje = "Baja probabilidad de aplicar y ser contratado. Para tener mayor probabilidad recuerda que las habilidades más solicitas son Uso y manejo de bases de datos, Python, C#, Desarrollo web back end o front end manejar buen ingles y por ultimo, capacidad de trabajo en equipo."
        elif prediccion < 0.7:
            mensaje = "Probabilidad moderada de aplicar y ser contratado, sin embargo puedes aumentar la probabilidad, fortaleciendo las habilidades blandas y ampliando tu portafolio de conocimientos."
        else:
            mensaje = "Puedes aplicar a una empresa y de manejar lo anteriormente seleccionado con gran capacidad, facilmente serías contratado"

        # Pasar el mensaje al contexto de la plantilla
        contexto = {'mensaje': mensaje}

        # Cerrar la conexión y el cursor
        cursor.close()
        conn.close()

        # Renderizar la plantilla HTML con el mensaje
        return render_template('prediccion.html', **contexto)

    # Si no se enviaron datos a través del formulario, mostrar el formulario vacío
    return render_template('formulario.html')






ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para cargar el archivo CSV
@app.route('/cargar_csv', methods=['GET', 'POST'])
@login_required
def cargar_csv():
    habilidades = [
        'Administración de sistemas Linux',
        'ADO.NET',
        'Análisis forense',
        'Analítica',
        'Angular',
        'Aseguramiento de la calidad',
        'ASP.NET',
        'Autenticación',
        'Automatización',
        'AWS',
        'Backbone.js',
        'Bases de datos',
        'Blockchain',
        'Bootstrap',
        'Business Apps',
        'C#',
        'C++',
        'CakePHP',
        'Capacidad de análisis',
        'Ciencia de datos',
        'Ciencias de la computación',
        'Colaboración',
        'Comunicación',
        'Criptografía',
        'Desarrollo de aplicaciones',
        'Desarrollo de SOAP',
        'Desarrollo de software',
        'Desarrollo front end',
        'Desarrollo web back end',
        'DevOps',
        'Diseño web adaptable',
        'Django',
        'Doctrine',
        'Documentación técnica',
        'Express.js',
        'GitHub',
        'Go',
        'GoldenGate',
        'Google Cloud',
        'Hibernate',
        'Hojas de estilos en cascada (CSS)',
        'HTML5',
        'HTTP',
        'Inglés B1 o más',
        'Inteligencia artificial',
        'Investigación',
        'Jakarta EE',
        'Jasmine Framework',
        'Java',
        'JavaScript',
        'Jest',
        'Jmeter',
        'jQuery',
        'JSON',
        'Karma',
        'Laravel',
        'Liderazgo',
        'Linux',
        'Maven',
        'metedologias SCRUM',
        'Metodologías Agiles',
        'microservicios',
        'Microsoft Azure',
        'Microsoft Dynamics',
        'Microsoft SQL Server',
        'Mocha',
        'MongoDB',
        'MVC',
        'MVVM',
        'MySQL',
        'Next.js',
        'Node.js',
        'Objective-C',
        'Oracle Database',
        'Pandas',
        'PHP',
        'PostgreSQL',
        'Proactividad',
        'Programación en C',
        'Pruebas de software',
        'Python',
        'React.JS',
        'Redux.js',
        'Resource Acquisition',
        'RMAN',
        'SAP Controlling (CO)',
        'SCADA',
        'Servicios web',
        'Sockets',
        'Software CRM',
        'Solidity',
        'Soluciones de software',
        'SPL',
        'Spring Framework',
        'Spring MVC',
        'SQL',
        'Swift',
        'Tolerancia a la presión',
        'Trabajo en equipo',
        'TypeScript',
        'WebdriverIO',
        'Webpack',
        'XML',
        'Yii',
        'empleo'
    ]
    if request.method == 'POST':
        # Verificar si se seleccionó un archivo
        if 'csv_file' not in request.files:
            error = 'No se ha seleccionado ningún archivo CSV.'
            return render_template('cargar_csv.html', error=error)
        
        csv_file = request.files['csv_file']
        
        # Verificar si se seleccionó un archivo válido
        if csv_file.filename == '':
            error = 'No se ha seleccionado ningún archivo CSV.'
            return render_template('cargar_csv.html', error=error)
        
        if csv_file and allowed_file(csv_file.filename):
            try:
                # Conectar a la base de datos
                connection = mysql.connector.connect(**config)
                
                # Crear un cursor para ejecutar consultas
                cursor = connection.cursor()

                # Leer el archivo CSV
                csv_data = csv_file.read().decode('latin-1').splitlines()
                csv_reader = csv.reader(csv_data, delimiter=';')

                # Saltar la primera línea (encabezados)
                next(csv_reader)

                # Insertar los datos en la tabla
                for row in csv_reader:
                    # Obtener los valores de cada columna
                    nombre = row[0]
                    habilidades_values = [int(value) if value else 0 for value in row[1:]]

                    # Construir la lista de columnas de habilidades en la consulta
                    habilidades_columns = ', '.join(['`' + habilidad.replace(' ', ' ') + '`' for habilidad in habilidades])


                    # Construir la lista de valores de habilidades en la consulta
                    habilidades_values_placeholder = ', '.join(['%s' for _ in habilidades_values])

                    # Construir la lista de valores a insertar en la consulta
                    values = [nombre] + habilidades_values

                    # Insertar los datos en la tabla 'datos'
                    query_datos = f"INSERT INTO datos (nombre, {habilidades_columns}) VALUES (%s, {habilidades_values_placeholder})"
                    cursor.execute(query_datos, values)

                # Hacer commit para guardar los cambios
                connection.commit()

                # Cerrar el cursor y la conexión
                cursor.close()
                connection.close()

                mensaje = 'Los datos se han cargado exitosamente.'
                return render_template('cargar_csv.html', mensaje=mensaje)

            except Exception as e:
                error = f'Error al cargar el archivo CSV: {str(e)}'
                return render_template('cargar_csv.html', error=error)

        else:
            error = 'El archivo seleccionado no es un archivo CSV válido.'
            return render_template('cargar_csv.html', error=error)

    return render_template('cargar_csv.html')


@app.route('/tabla_habilidades')
@login_required
def tabla_habilidades():
    # Establecer conexión con la base de datos
    connection = mysql.connector.connect(**config)

    # Crear un cursor para ejecutar consultas
    cursor = connection.cursor()

    # Lista de habilidades
    habilidades = [
        'Administración de sistemas Linux',
        'ADO.NET',
        'Análisis forense',
        'Analítica',
        'Angular',
        'Aseguramiento de la calidad',
        'ASP.NET',
        'Autenticación',
        'Automatización',
        'AWS',
        'Backbone.js',
        'Bases de datos',
        'Blockchain',
        'Bootstrap',
        'Business Apps',
        'C#',
        'C++',
        'CakePHP',
        'Capacidad de análisis',
        'Ciencia de datos',
        'Ciencias de la computación',
        'Colaboración',
        'Comunicación',
        'Criptografía',
        'Desarrollo de aplicaciones',
        'Desarrollo de SOAP',
        'Desarrollo de software',
        'Desarrollo front end',
        'Desarrollo web back end',
        'DevOps',
        'Diseño web adaptable',
        'Django',
        'Doctrine',
        'Documentación técnica',
        'Express.js',
        'GitHub',
        'Go',
        'GoldenGate',
        'Google Cloud',
        'Hibernate',
        'Hojas de estilos en cascada (CSS)',
        'HTML5',
        'HTTP',
        'Inglés B1 o más',
        'Inteligencia artificial',
        'Investigación',
        'Jakarta EE',
        'Jasmine Framework',
        'Java',
        'JavaScript',
        'Jest',
        'Jmeter',
        'jQuery',
        'JSON',
        'Karma',
        'Laravel',
        'Liderazgo',
        'Linux',
        'Maven',
        'metedologias SCRUM',
        'Metodologías Agiles',
        'microservicios',
        'Microsoft Azure',
        'Microsoft Dynamics',
        'Microsoft SQL Server',
        'Mocha',
        'MongoDB',
        'MVC',
        'MVVM',
        'MySQL',
        'Next.js',
        'Node.js',
        'Objective-C',
        'Oracle Database',
        'Pandas',
        'PHP',
        'PostgreSQL',
        'Proactividad',
        'Programación en C',
        'Pruebas de software',
        'Python',
        'React.JS',
        'Redux.js',
        'Resource Acquisition',
        'RMAN',
        'SAP Controlling (CO)',
        'SCADA',
        'Servicios web',
        'Sockets',
        'Software CRM',
        'Solidity',
        'Soluciones de software',
        'SPL',
        'Spring Framework',
        'Spring MVC',
        'SQL',
        'Swift',
        'Tolerancia a la presión',
        'Trabajo en equipo',
        'TypeScript',
        'WebdriverIO',
        'Webpack',
        'XML',
        'Yii',
    ]

    # Diccionario para almacenar los resultados
    resultados = {}

    # Consultar la cantidad de personas con cada habilidad
    for habilidad in habilidades:
        # Consultar la cantidad de personas que saben la habilidad
        query_personas = f"SELECT COUNT(*) FROM datos WHERE `{habilidad}` = 1"
        cursor.execute(query_personas)
        cantidad_personas = cursor.fetchone()[0]


        # Consultar la cantidad de veces que la habilidad es solicitada en las vacantes
        query_vacantes = f"SELECT cantidad FROM habilidades_vacantes WHERE habilidad = '{habilidad}'"
        cursor.execute(query_vacantes)
        resultado_vacantes = cursor.fetchone()

        if resultado_vacantes is not None:
            cantidad_vacantes = resultado_vacantes[0]
        else:
            cantidad_vacantes = 0
        
        deficit = cantidad_vacantes - cantidad_personas


        resultados[habilidad] = {'personas': cantidad_personas, 'vacantes': cantidad_vacantes, 'deficit': deficit}
    # Cerrar el cursor y la conexión
    cursor.close()
    connection.close()

    # Renderizar la plantilla HTML con los resultados
    return render_template('tabla_habilidades.html', resultados=resultados)



@app.route('/analisis')
@login_required
def analisis():

    habilidades = [
            'Administración de sistemas Linux',
            'ADO.NET',
            'Análisis forense',
            'Analítica',
            'Angular',
            'Aseguramiento de la calidad',
            'ASP.NET',
            'Autenticación',
            'Automatización',
            'AWS',
            'Backbone.js',
            'Bases de datos',
            'Blockchain',
            'Bootstrap',
            'Business Apps',
            'C#',
            'C++',
            'CakePHP',
            'Capacidad de análisis',
            'Ciencia de datos',
            'Ciencias de la computación',
            'Colaboración',
            'Comunicación',
            'Criptografía',
            'Desarrollo de aplicaciones',
            'Desarrollo de SOAP',
            'Desarrollo de software',
            'Desarrollo front end',
            'Desarrollo web back end',
            'DevOps',
            'Diseño web adaptable',
            'Django',
            'Doctrine',
            'Documentación técnica',
            'Express.js',
            'GitHub',
            'Go',
            'GoldenGate',
            'Google Cloud',
            'Hibernate',
            'Hojas de estilos en cascada (CSS)',
            'HTML5',
            'HTTP',
            'Inglés B1 o más',
            'Inteligencia artificial',
            'Investigación',
            'Jakarta EE',
            'Jasmine Framework',
            'Java',
            'JavaScript',
            'Jest',
            'Jmeter',
            'jQuery',
            'JSON',
            'Karma',
            'Laravel',
            'Liderazgo',
            'Linux',
            'Maven',
            'metedologias SCRUM',
            'Metodologías Agiles',
            'microservicios',
            'Microsoft Azure',
            'Microsoft Dynamics',
            'Microsoft SQL Server',
            'Mocha',
            'MongoDB',
            'MVC',
            'MVVM',
            'MySQL',
            'Next.js',
            'Node.js',
            'Objective-C',
            'Oracle Database',
            'Pandas',
            'PHP',
            'PostgreSQL',
            'Proactividad',
            'Programación en C',
            'Pruebas de software',
            'Python',
            'React.JS',
            'Redux.js',
            'Resource Acquisition',
            'RMAN',
            'SAP Controlling (CO)',
            'SCADA',
            'Servicios web',
            'Sockets',
            'Software CRM',
            'Solidity',
            'Soluciones de software',
            'SPL',
            'Spring Framework',
            'Spring MVC',
            'SQL',
            'Swift',
            'Tolerancia a la presión',
            'Trabajo en equipo',
            'TypeScript',
            'WebdriverIO',
            'Webpack',
            'XML',
            'Yii',
        ]

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    habilidades_solicitadas = []
    habilidades_conocidas = []

    for habilidad in habilidades:
        # Obtener la cantidad de veces que la habilidad es solicitada
        cursor.execute(f"SELECT cantidad FROM habilidades_vacantes WHERE habilidad = '{habilidad}'")
        veces_solicitada = cursor.fetchone()[0]
        habilidades_solicitadas.append(veces_solicitada)

        # Obtener la cantidad de personas que saben la habilidad
        cursor.execute(f"SELECT COUNT(*) FROM datos WHERE `{habilidad}` = 1")
        cantidad_personas = cursor.fetchone()[0]
        habilidades_conocidas.append(cantidad_personas)

    cursor.close()
    cnx.close()

    # Crear el modelo de regresión lineal
    model = LinearRegression()

    # Entrenar el modelo con los datos
    X = np.array(habilidades_solicitadas).reshape(-1, 1)
    y = np.array(habilidades_conocidas)
    model.fit(X, y)

    # Predecir la cantidad de personas que saben cada habilidad dada la cantidad de veces que es solicitada
    prediccion = model.predict(X)

    # Comparar la predicción con la cantidad real de personas que saben cada habilidad
    resultados = []
    for i in range(len(habilidades)):
        if habilidades_conocidas[i] < prediccion[i]:
            resultados.append(f"La Competencia {habilidades[i]} es muy demandada y hay un déficit de personas que la saben.")
        else:
            resultados.append(f"La Competencia {habilidades[i]} no es tan demandada o hay suficientes personas que la saben.")

    return render_template('analisis.html', resultados=resultados)



if __name__ == '__main__':
    app.run(debug=True)
